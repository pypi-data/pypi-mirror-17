import sys
import os
import multiprocessing
import shutil
import traceback
import time
import logging


import h5py
import numpy as np
import pandas as pd
from scipy import signal, stats

from .ndfconverter import NdfFile
from .h5loader import H5File
from .feature_extractor import FeatureExtractor
from .utils import filterArray

if sys.version_info < (3,):
    range = xrange


ERROR_FLAG = False

import logging
#loggers = {}

#from make_pdfs import plot_traces_hdf5, plot_traces
class DataHandler():
    '''
    Class to handle all ingesting of data and outputing it in a format for the Classifier Handler

    TODO:
     - Generate training/seizure library using ndfs and df (bundle directly - many datasets??)
     - generate single channel folders for predictions, pass in dates, and print out files you skipped

     - use the h5file and ndfFile class to clean up the code (use indexing for future compat with h5 or ndf)

    To think about
    - handle the unix timestamps better in general
    - enable feature extraction to be better handled
    - filtering and pre processing
    - remeber when defining maxshape = (None, data_array.shape[1])) - to allow h5 to gorwp

    for faster conversion/datawrting?!:
    have main save, the rest calculate

    import multiprocessing as mp
    import time

    def foo_pool(x):
        time.sleep(2)
        return x*x

    result_list = []
    def log_result(result):
        # This is called whenever foo_pool(i) returns a result.
        # result_list is modified only by the main process, not the pool workers.
        result_list.append(result)

    def apply_async_with_callback():
        pool = mp.Pool(4)
        for i in range(10):
        pool.imap(foo_pool, args = (i, ), callback = log_result)
        pool.close()
        pool.join()
        print(result_list)


apply_async_with_callback()

    '''

    def __init__(self, logpath = os.getcwd()):

        self.parallel_savedir = None
        #print(os.getcwd())
        #global loggers
        #if loggers.get(name):
        #    return loggers.get(name)
        #else:

    def add_features_seizure_library(self,
                                    libary_path,
                                    filter_window = 7,
                                    filter_order = 3,
                                    overwrite = False):
        global ERROR_FLAG
        logging.info('Adding features to '+ libary_path + ' with filter settings: ' +str(filter_window)+', '+str(filter_order))

        with h5py.File(libary_path, 'r+') as f:

            timewindow = f.attrs['timewindow']
            fs         = f.attrs['fs']

            seizure_datasets = [f[group] for group in list(f.keys())]
            l = len(seizure_datasets)-1
            self.printProgress(0,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
            for i, group in enumerate(seizure_datasets):
                logging.debug('Loading group: '+ str(group))
                try:
                    if not overwrite:
                        features = group['features']
                        logging.info(str(group)+' already has features, skipping')
                    if overwrite:
                        raise
                except:
                    data_array = group['data'][:]
                    assert len(data_array.shape) > 1

                    fdata = filterArray(data_array, window_size= filter_window, order= filter_order)
                    #fndata = self._normalise(fdata)
                    fndata = fdata
                    if fndata is not None:
                        extractor = FeatureExtractor(fndata, fs = group.attrs['fs'], verbose_flag = False)
                        features = extractor.feature_array

                        try:
                            del group['features']
                            logging.debug('Deleted old features')
                        except:
                            pass
                        group.create_dataset('features', data = features, compression = 'gzip', dtype = 'f4')
                        logging.info('Added features to ' + str(group) + ', shape:' + str(features.shape))
                        self.printProgress(i,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
                    else:
                        logging.warning("Didn't add features to file: "+str(group))
                        ERROR_FLAG = True
                        return 0
        if ERROR_FLAG:
            print ('Errors occurred: please check the log file (search for error!)')
            ERROR_FLAG = False

    def add_predicition_features_to_h5_file(self,
                                            h5_file_path,
                                            timewindow = 5,
                                            filter_window = 7,
                                            filter_order = 3):
        '''
        Have the stucture of:

        M1445612etc / tid1
                    / tid2
                    / tid3  / data
                            / time
        '''
        global ERROR_FLAG
        with h5py.File(h5_file_path, 'r+') as f:
            tids    = list(f.attrs['t_ids'])
            tid_to_fs_dict = f.attrs['fs_dict']

            mcodes = [f[group] for group in list(f.keys())]
            assert len(mcodes) == 1
            mcode = mcodes[0]

            tids = [mcode[tid] for tid in list(mcode.keys())]

            for tid in tids: # loop through groups which are tids for predicition h5s

                data_array = tid['data'][:]
                if len(data_array.shape) == 1:
                    logging.debug('Reshaping data from '+str(data_array.shape)+ ' using '+str(tid.attrs['fs']) +' fs' +
                                  ' and timewindow of '+ str(timewindow)  )
                    data_array = self._make_array_from_data(data_array, fs = tid.attrs['fs'], timewindow = timewindow)

                try:
                    assert data_array.shape[0] == int(3600/timewindow)
                except:
                    print('Warning: Data file does not contain, full data: ' + str(os.path.basename(h5_file_path)) + str(data_array.shape))
                    if data_array.shape[0] == 0:
                        print('Data file does not contain any data. Exiting: ')
                        return 0

                fdata = filterArray(data_array, window_size= filter_window, order= filter_order)
                fndata = self._normalise(fdata)
                if fndata is not None:
                    extractor = FeatureExtractor(fndata,tid.attrs['fs'], verbose_flag = False)
                    features = extractor.feature_array

                    try:
                        del tid['features']
                        logging.debug('Deleted old features')
                    except:
                        pass
                    tid.create_dataset('features', data = features, compression = 'gzip')
                    logging.debug('Added features to ' + str(os.path.basename(h5_file_path)) + ', shape:' + str(features.shape))
                else:
                    logging.error("Didn't add features to group: "+ str(tid))
                    ERROR_FLAG = True

        if ERROR_FLAG:
            print ('Errors occurred: please check the log file (search for error!)')
            ERROR_FLAG = False

    def parallel_add_prediction_features(self, h5py_folder, n_cores = -1):
        '''
        # NEED TO ADD SETTINGS HERE FOR THE TIMEWINDOW ETC
        :param h5py_folder:
        :return:
        '''
        global ERROR_FLAG
        files_to_add_features = [os.path.join(h5py_folder, fname) for fname in os.listdir(h5py_folder) if fname.startswith('M')]
        if n_cores == -1:
            n_cores = multiprocessing.cpu_count()

        pool = multiprocessing.Pool(n_cores)
        l = len(files_to_add_features)
        self.printProgress(0,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
        for i, _ in enumerate(pool.imap(self.add_predicition_features_to_h5_file, files_to_add_features), 1):
            self.printProgress(i,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)

        #pool.map(self.add_predicition_features_to_h5_file, files_to_add_features)
        pool.close()
        pool.join()

        if ERROR_FLAG:
            print ('Errors occurred: please check the log file (search for error!)')
            ERROR_FLAG = False

    def _get_annotations_from_df_datadir_matches(self, df, file_dir):
        '''
        This function matches the entries in a dataframe with files in a directory

        Returns: list of annotations stored in a list
        '''
        abs_filenames = [os.path.join(file_dir, f) for f in os.listdir(file_dir)]
        data_filenames = [f for f in os.listdir(file_dir) if f.startswith('M')]
        mcodes = [os.path.split(f)[1][:11] for f in os.listdir(file_dir) if f.startswith('M')]
        n_files = len(data_filenames)

        # now loop through matching the tid to datafile in the annotations
        df.columns = [label.lower() for label in df.columns]
        reference_count = 0
        annotation_dicts = []
        for row in df.iterrows():
            # annotation name is bad, but will ultimately be the library h5 dataset name
            annotation_name = str(row[1]['name']).split('.')[0]+'_tid_'+str(int(row[1]['transmitter']))
            for datafile in data_filenames:
                if datafile.startswith(annotation_name.split('_')[0]):
                    start = row[1]['start']
                    end = row[1]['end']
                    annotation_dicts.append({'fname': os.path.join(file_dir, datafile),
                                             'start': start,
                                             'end': end,
                                             'dataset_name': annotation_name,
                                             'tid':int(row[1]['transmitter'])})
                    reference_count += 1

        print('Of the '+str(n_files)+' ndfs in directory, '+str(reference_count)+' references to seizures were found in the passed dataframe')
        return annotation_dicts

    def make_seizure_library(self, df, file_dir, timewindow = 5,
                             seizure_library_name = 'seizure_library',
                             fs = 'auto',
                             verbose = False,
                             overwrite = False):
        '''
        Args:

            df : pandas dataframe. Column titles need to be "name", "start","end", "transmitter"
            file_dir: path to converted h5, or ndf directory, that contains files referenced in
                      the dataframe
            timewindow: size to chunk the data up with
            seizure_library_name: path and name of the seizure lib.
            fs: default is auto, but use freq in hz to sidestep the auto dectection
            verbose: Flag, print or not.

        Returns:
            Makes a Seizure library file

        WARNING: The annotation will be incorrect based on the time-window coarseness and the chunk that is chosen!
        Currently finding the start by start/timewindom -- end/timewindow


        TODO:
        -  How to handle files that don't have seiures, but we want to include
        -  Not sure what is going on when there are no seizures, need to have this functionality though.

        '''
        global ERROR_FLAG
        logging.info('Datahandler - creating SeizureLibrary')

        annotation_dicts = self._get_annotations_from_df_datadir_matches(df, file_dir)
        # annotations_dicts is a list of dicts with... e.g 'dataset_name': 'M1445443776_tid_9',
        # 'end': 2731.0, 'fname': 'all_ndfs/M1445443776.ndf', 'start': 2688.0,' tid': 9

        h5code = 'w' if overwrite else 'x'
        try:
            if not '/' in seizure_library_name or not "\\" in seizure_library_name:
                seizure_library_path = os.path.split(file_dir)[0]+seizure_library_name.strip('.h5')+'.h5'
            seizure_library_path = seizure_library_name.strip('.h5')+'.h5'
            print('Creating seizure library: '+ seizure_library_path)
            logging.info('Creating seizure library: '+ seizure_library_path)
            h5file = h5py.File(seizure_library_path, h5code)
            h5file.attrs['fs'] = fs
            h5file.attrs['timewindow'] = timewindow
            h5file.close()

        except Exception:
            print ('Error: Seizure library file exists! Delete it or set "overwrite" to True')
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print (traceback.print_exception(exc_type, exc_value, exc_traceback))
            return 0

        # now populate to seizure lib with data, time and labels
        # make a list
        l = len(annotation_dicts)-1
        self.printProgress(0,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
        for i, annotation in enumerate(annotation_dicts):
            self._populate_seizure_library(annotation, fs, timewindow, seizure_library_path, verbose = verbose)
            self.printProgress(i,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
        if ERROR_FLAG:
            print ('Errors occurred: please check the log file (search for error!)')
            ERROR_FLAG = False

    def append_to_seizure_library(self, df, file_dir, seizure_library_path,
                                  timewindow = 5,
                                  fs = 'auto',
                                  verbose = False,
                                  overwrite = False):
        '''
        Args:

            df : pandas dataframe. Column titles need to be "name", "start","end", "transmitter"
            file_dir: path to converted h5, or ndf directory, that contains files referenced in
                      the dataframe
            timewindow: size to chunk the data up with
            seizure_library_path: path and name of the seizure lib.
            fs: default is auto, but use freq in hz to sidestep the auto dectection
            verbose: Flag, print or not.

        Returns:
            Appends to a Seizure library file

        WARNING: The annotation will be incorrect based on the time-window coarseness and the chunk that is chosen!
        Currently finding the start by start/timewindom -- end/timewindow


        TODO:
        -  How to handle files that don't have seiures, but we want to include
        -  Not sure what is going on when there are no seizures, need to have this functionality though.

        '''
        global ERROR_FLAG
        logging.info('Appending to seizure library')
        annotation_dicts = self._get_annotations_from_df_datadir_matches(df, file_dir)
        # annotations_dicts is a list of dicts with... e.g 'dataset_name': 'M1445443776_tid_9',
        # 'end': 2731.0, 'fname': 'all_ndfs/M1445443776.ndf', 'start': 2688.0,' tid': 9

        # now add to to seizure lib with data, time and labels
        l = len(annotation_dicts)-1
        logging.info('Datahandler - creating SeizureLibrary')
        self.printProgress(0,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
        for i, annotation in enumerate(annotation_dicts):
            self._populate_seizure_library(annotation, fs, timewindow, seizure_library_path, verbose = verbose)
            self.printProgress(i,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
        if ERROR_FLAG:
            print ('Errors occurred: please check the log file (search for error!)')
            ERROR_FLAG = False

    def _populate_seizure_library(self, annotation, fs,
                                  timewindow,
                                  seizure_library_path,
                                  verbose = False):
        # decide whether ndf or h5
        logging.debug('Adding '+str(annotation['fname']))
        if annotation['fname'].endswith('.ndf'):
            file_obj = NdfFile(annotation['fname'],fs = fs)
            file_obj.load(annotation['tid'])
        elif annotation['fname'].endswith('.h5'):
            file_obj = H5File(annotation['fname'])
        else:
            print('ERROR: Unrecognised file-type')

        # add in filtering and scaling here
        fcs_data = self.highpassfilter_and_standardise(file_obj[annotation['tid']]['data'], fs)
        data_array = self._make_array_from_data(fcs_data, fs, timewindow)

        # use the start and end times to make labels
        labels = np.zeros(shape = (data_array.shape[0]))
        start_i = int(np.floor(annotation['start']/timewindow))
        end_i   = int(np.ceil(annotation['end']/timewindow))

        with h5py.File(seizure_library_path, 'r+') as f:
            if annotation['dataset_name'] in f.keys():
                logging.info(str(annotation['dataset_name'])+' has more than one seizure!')
                labels =  f[annotation['dataset_name']+'/labels']
                labels[start_i:end_i] = 1
            else:
                group = f.create_group(annotation['dataset_name'])
                group.attrs['tid'] = annotation['tid']
                group.attrs['fs']  = fs
                group.create_dataset('data', data = data_array, compression = "gzip", dtype='f4', chunks = data_array.shape)
                labels[start_i:end_i] = 1 # indexing is fine, dont need to convert to array
                group.create_dataset('labels', data = labels, compression = "gzip", dtype = 'i2', chunks = labels.shape)
            f.close()

    @staticmethod
    def highpassfilter_and_standardise(data, fs, cutoff_hz = 1, stdtw = 5,std_dec_places = 2):
        logging.debug('Highpassfiltering and standising mode std, fs: ' + str(fs))

        nyq = 0.5 * fs
        cutoff_hz = cutoff_hz/nyq
        data = data-np.mean(data)
        b, a = signal.butter(2, cutoff_hz, 'highpass', analog=False)
        filtered_data = signal.filtfilt(b,a, data, padtype=None)

        # now standardise
        reshaped = np.reshape(filtered_data, (int(3600/stdtw), int(stdtw*fs)))
        std_vector = np.round(np.std(reshaped, axis = 1),decimals=std_dec_places)
        mode_std = stats.mode(std_vector)[0]
        scaled = np.divide(data,mode_std)
        return scaled

    @staticmethod
    def _make_array_from_data(data, fs, timewindow):
        n_traces = int(data.shape[0] / (fs * timewindow))
        dp_lost =  int(data.shape[0] % (fs * timewindow))
        if dp_lost > 0:
            data_array = np.reshape(data[:-dp_lost], newshape = (n_traces, int(fs * timewindow)))
        else:
            data_array = np.reshape(data, newshape = (n_traces, int(fs * timewindow)))
        return data_array

    @staticmethod
    def _fullpath_listdir(d):
        return [os.path.join(d, f) for f in os.listdir(d) if not f.startswith('.')]

    @ staticmethod
    def _normalise(series):

        a = np.min(series, axis=1)
        b = np.max(series, axis=1)

        try:
            #assert (b-a).all() != 0.0
            result = np.divide((series - a[:, None]), (b-a)[:,None])
            return result
        except:
            logging.error('Zero div error caught, passing. Data array has items all the same')

            ERROR_flag = True
            #return None

    def convert_ndf_directory_to_h5(self, ndf_dir, tids = 'all', save_dir  = 'same_level', n_cores = -1, fs = 'auto'):
        """

        Args:
            ndf_dir: Directory to convert
            tids: transmitter ids to convert. Default is 'all'
            save_dir: optional save directory, will default to appending convertered_h5s after current ndf
            n_cores: number of cores to use
            fs :  'auto' or frequency in hz

        ndfs conversion seem to be pretty buggy...

        """
        global ERROR_FLAG
        self.fs_for_parallel_conversion = fs
        files = [f for f in self._fullpath_listdir(ndf_dir) if f.endswith('.ndf')]

        # check ids
        ndf = NdfFile(files[0])
        if not tids == 'all':
            if not hasattr(tids, '__iter__'):
                tids = [tids]
            #for tid in tids:
            #    try:
            #        assert tid in ndf.tid_set
            #    except AssertionError:
            #        print('Please enter valid tid (at least for the first!) file in directory ('+str(ndf.tid_set)+')')
            #        sys.exit()

        self.tids_for_parallel_conversion = tids
        print ('Transmitters for conversion: '+ str(self.tids_for_parallel_conversion))

        # set n_cores
        if n_cores == -1:
            n_cores = multiprocessing.cpu_count()

        # Make save directory
        if save_dir  == 'same_level':
            save_dir = ndf_dir+'_converted_h5s'
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        self.savedir_for_parallel_conversion = save_dir

        pool = multiprocessing.Pool(n_cores)
        l = len(files)
        self.printProgress(0,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
        for i, _ in enumerate(pool.imap(self._convert_ndf, files), 1):
            self.printProgress(i,l, prefix = 'Progress:', suffix = 'Complete', barLength = 50)
        pool.close()
        pool.join()
        if ERROR_FLAG:
            print ('Errors occurred: please check the log file (search for error!)')
            ERROR_FLAG = False

    def _convert_ndf(self,filename):
        global ERROR_FLAG
        savedir = self.savedir_for_parallel_conversion
        tids = self.tids_for_parallel_conversion
        fs = self.fs_for_parallel_conversion

        # convert m name
        mname = os.path.split(filename)[1]
        tstamp = float(mname.strip('M').split('.')[0])
        ndf_time = '_'+str(pd.Timestamp.fromtimestamp(tstamp)).replace(':', '_')
        ndf_time =  ndf_time.replace(' ', '_')
        start = time.time()
        try:
            ndf = NdfFile(filename, fs = fs)
            if set(tids).issubset(ndf.tid_set) or tids == 'all':
                ndf.load(tids)
                abs_savename = os.path.join(savedir, filename.split('/')[-1][:-4]+ndf_time+' tids_'+str(tids))
                ndf.save(save_file_name= abs_savename)
            else:
                logging.warning('Not all read tids:'+str(tids) +' were valid for '+str(os.path.split(filename)[1])+' skipping!')
                #print('not all tids:'+str(tids) +' were valid for '+str(os.path.split(filename)[1])+' skipping!')
                ERROR_FLAG = True
        except Exception:
            print('Something unexpected went wrong loading '+str(tids)+' from '+mname+' :')
            #print('Valid ids are:'+str(ndf.tid_set))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print (traceback.print_exception(exc_type, exc_value,exc_traceback))
        return 0 # don't think i actually this
    # Print iterations progress

    def printProgress (self, iteration, total, prefix = '', suffix = '', decimals = 2, barLength = 100):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : number of decimals in percent complete (Int)
            barLength   - Optional  : character length of bar (Int)
        """
        filledLength    = int(round(barLength * iteration / float(total)))
        percents        = round(100.00 * (iteration / float(total)), decimals)
        bar             = '█' * filledLength + '-' * (barLength - filledLength)
        sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
        sys.stdout.flush()
        if iteration == total:
            sys.stdout.write('\n')
            sys.stdout.flush()
