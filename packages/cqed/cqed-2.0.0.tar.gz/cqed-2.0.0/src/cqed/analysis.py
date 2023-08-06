#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd 
import numpy as np 
from numpy import inf
import h5py 
import os 
import re 
import matplotlib.pyplot as plt
import glob 
import easygui as eg
from IPython.display import clear_output
import datetime
import sys
import ctypes
import _ctypes
import time
import tkinter as tk
import tkinter.filedialog
import math
import csv
from tqdm.notebook import tqdm as pbar
###############################################################################################
# class: directory & cavity initial choosing GUI
class GUI:
    def __init__(self):
        self.default = self.dir_start() # default starting directory
     
    def dir_start(self):
        dir_init = 'C:\\Users\\Lab3\\Documents\\Data'
        year =  datetime.date.today().year
        directory = os.path.join(dir_init, str(year))
        return directory
            
    # function: get directory 
    # inputs: none, or a initial directory
    def dir_gui(self,*args):
        try:
            dir_from = [value for value in args if os.path.isdir(value)][0]
            directory = eg.diropenbox('Choose directory',None ,dir_from)
        except:
            directory = eg.diropenbox('Choose directory',None, self.default)
        return directory
        
    # function: choose cavity ( and return initial letter) 
    # inputs: none, or cavity name
    def cavity_initial(self,*args,**kwargs):
        try:
            cavity = [value[0].lower() for value in args 
                      if re.search('^[hv].*', value, re.IGNORECASE) and os.path.isdir(value) == False][0]
        except:
            try:
                cavity = [value[0].lower() for key,value in kwargs.items() 
                          if re.search('^(cav).*',key, re.IGNORECASE) and os.path.isdir(value) == False][0] 
            except:       
                choice = eg.buttonbox('Which cavity?', choices=['Horizontal','Vertical'])
                cavity = choice[0].lower()
        return cavity
    
###############################################################################################
# class: load specs from _spec.csv
# input: directory[optional], OR, directory = ...[oprional]
# outputs: experimental parameters as class attribute
class Specs:
    def __init__(self,*args,**kwargs):
        self.args = args
        self.kwargs = kwargs
        self.dir = self.__choose_directory()
        self.specs = self.__load_specs()
        
    def __choose_directory(self):
        try: # directory from args
            directory = [value for value in self.args if os.path.isdir(value)][0]  # string array    
        except: # directory from kwargs
            try:
                directory = [value for key,value in self.kwargs.items() 
                         if re.search('^((dir)|(path)|(folder)).*',key, re.IGNORECASE)][0]
            except:  # from GUI
                directory = GUI().dir_gui()
        return directory
    
    # load specs
    def __load_specs(self):  
        specs = {}
        file = open(os.path.join(self.dir, '_specs.csv'), mode = 'r', newline='')
        reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
        for row in reader :
            specs[row[0]] = row[1]
        file.close()
        return specs

        
###############################################################################################
# class: load, process, statistics and save experiment data from dir
# pre-requisition: initial parameters either from _specs.csv or manual inputs
# input: cavity = 'horizontal' or 'vertical', directory = optional
# outputs: saved dict file, with mean and err 
class Process:
    def __init__(self, *args, **kwargs):
        self.ti = time.time()
        self.args = args
        self.kwargs = kwargs
        self.dir = self.__choose_directory()
        self.cavity = GUI().cavity_initial(*self.args, **self.kwargs)
        self.file_path = os.path.join(self.dir, '_data_{}.h5'.format(self.cavity))
        self.__clean()
        self.__select_runs() # find successful runs
        self.__load_specs()  # load {par} to self.{par}   
        self.__define_parameters() # define cavity parameters
        self.__load_data()  # load experiment data
        self.__save_data()  # save data

    # choose directory
    def __choose_directory(self):
        try: # directory from args
            directory = [value for value in self.args if os.path.isdir(value)][0]  # string array    
        except: # directory from kwargs
            try:
                directory = [value for key,value in self.kwargs.items() 
                         if re.search('^((dir)|(path)|(folder)).*',key, re.IGNORECASE)][0]
            except:  # from GUI
                directory = GUI().dir_gui()
        return directory
    
    # clean up previous file
    def __clean(self):
        try:
            os.remove(self.file_path)
        except:
            pass
            
    # load experiment parameters to self attributes
    def __load_specs(self):
        p = Specs(self.dir).specs  # load all specs
        for key, value in p.items():
            exec("self.{} = {}".format(key, value))

    # drop failure data run
    def __select_runs(self):
        try:
            self.fail_run_list = [value for key,value in self.kwargs.items() 
                             if re.search('^((fail)|(drop)|(abandon)).*',key, re.IGNORECASE)][0]
        except:
            self.fail_run_list = []
        
    # define horizontal and vertical cavity parameters to self attributes
    def __define_parameters(self):
        # experiment name
        self.exp_name = 'probe_{}'.format(self.cavity)
        self.freq_probe_0 = eval('self.freq_eom_{}_0'.format(self.cavity))
        self.freq_probe_list= eval('self.freq_exp_list_{}'.format(self.cavity))
        self.detune_list = np.array(self.freq_probe_list) - self.freq_probe_0  # probe detuning    
        self.n_burst_probe = int(self.n_burst_probe) 
        # number of runs to analyze
        self.file_name_list = [value for value in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, value)) and 
                         re.search('(?<=({}_))\d+(?=(.h5))'.format(self.exp_name), value)]
        self.__num_run = len(self.file_name_list)   
        if bool(self.file_name_list) == False:
            print("Error: {} file doesn't exist!".format(self.exp_name))
            sys.exit()

        # pick up failed runs
        self.success_run_list = list(range(self.__num_run))  # assume all successful
        if bool(self.fail_run_list): # remove failed runs      
            for run in self.fail_run_list:
                try:
                    self.success_run_list.remove(run)
                except:
                    pass
        # create transmission dictionary without values, mean for average, err for error bars
        self.key_var_list = ['transm_h','bg_h', 'transm_hv_h','bg_hv_h', 'transm_v','bg_v', 'transm_hv_v', 'bg_hv_v']
        for key in self.key_var_list:
            # define array
            exec('self.{} = {}'.format(key,{}))
            # assign keys (detuning)
            for detuning in self.detune_list:   
                exec("self.{}['probe detuning {:.6f} MHz'] = np.array([])".format(key, detuning))
        self.key_list = []  # combining var and err
        for key in self.key_var_list:
            self.key_list.append(key)
            self.key_list.append(key + '_err')

        # actual n_burst_probe detected
        self.n_burst_probe_act_list = []
        for each_run in self.success_run_list:
            file = h5py.File(os.path.join(self.dir, self.exp_name  + '_{:04d}.h5'.format(each_run)),'r')
            # # load each probe detuning
            for detuning in self.detune_list:            
                data_all = pd.DataFrame({'t': file['probe detuning {:.6f} MHz'.format(detuning)][0],
                                         'ch':file['probe detuning {:.6f} MHz'.format(detuning)][1]})  
                time_trig= data_all[data_all['ch']==self.ch_qt_trig - 1]['t']
                self.n_burst_probe_act_list.append(len(time_trig))
            file.close()
        self.n_burst_probe_act = min(self.n_burst_probe_act_list) # pick up the smallest
        
        # experiment pulse time list
        self.time_pulse_list_h  = np.arange(self.n_burst_probe_act) * self.t0 + self.time_gate_resp + self.t0
        self.time_pulse_list_hv = np.arange(self.n_burst_probe_act) * self.t0 + self.time_gate_resp + 1/3 * self.t0
        self.time_pulse_list_v  = np.arange(self.n_burst_probe_act) * self.t0 + self.time_gate_resp + 2/3 * self.t0       
 
    ## load runs of probing experiment data
    def __load_data(self):
        self.warning = ''
        # create empty dict to append on, 0 row and self.n_burst_probe_act-1 columns
        for key in self.key_var_list:
            for detuning in self.detune_list:            
                exec("self.{}['probe detuning {:.6f} MHz'] = np.empty((0,self.n_burst_probe_act -1))".format(key, detuning))
        # # load data
        for each_run in pbar(self.success_run_list, desc='Load runs of successful {} cavity data'.format(self.cavity)):
            file = h5py.File(os.path.join(self.dir, self.exp_name  + '_{:04d}.h5'.format(each_run)),'r')
            # #  load each probe detuning
            for detuning in pbar(self.detune_list, desc='Probe detuning'):   
                data_all = pd.DataFrame({'t': file['probe detuning {:.6f} MHz'.format(detuning)][0],
                                         'ch':file['probe detuning {:.6f} MHz'.format(detuning)][1]})  
                time_trig= data_all[data_all['ch']==self.ch_qt_trig - 1]['t'][0:self.n_burst_probe_act] # equal length  
                try:
                    # pick up effective triggered data
                    data = data_all[(data_all['t'] >= min(time_trig)) & (data_all['t'] <= max(time_trig))] 
                    # find triggers for rising & falling
                    time_rise_h  = time_trig + self.time_delay_h/self.tagger_width # starting trigger, machine time
                    time_rise_v  = time_trig + self.time_delay_v/self.tagger_width
                    time_rise_hv = time_trig + self.time_delay_hv/self.tagger_width
                    time_fall_h  = time_rise_h + self.time_width/self.tagger_width  # stopping trigger, machine time
                    time_fall_v  = time_rise_v + self.time_width/self.tagger_width  
                    time_fall_hv = time_rise_hv + self.time_width/self.tagger_width 
                    # cutting edges
                    bin_edge = np.concatenate((time_rise_h,time_fall_h,time_rise_hv,time_fall_hv,time_rise_v,time_fall_v))
                    bin_edge.sort()  # order in time sequence
                    bin_edge = np.unique(bin_edge)  # remove duplicate
                    bin_edge = bin_edge[:-5]
                    # find counts, dark counts, and mean net counts [per pulse]
                    # only horizontal cavity
                    transm_h_1 = np.array(pd.cut(data[data['ch'] == self.ch_qt_h - 1]['t'], bin_edge, right=False)
                                        .value_counts(sort=False)[0::6])  
                    bg_h_1  = np.array(pd.cut(data[data['ch'] == self.ch_qt_h - 1]['t'], bin_edge, right=False)
                                        .value_counts(sort=False)[1::6])  
                    # only vertical cavity
                    transm_v_1 = np.array(pd.cut(data[data['ch'] == self.ch_qt_v - 1]['t'], bin_edge, right=False)
                                        .value_counts(sort=False)[4::6])  
                    bg_v_1  = np.array(pd.cut(data[data['ch'] == self.ch_qt_v - 1]['t'], bin_edge, right=False)
                                    .value_counts(sort=False)[5::6])  
                    # probe in both cavities, horizontal cavity output
                    transm_hv_h_1 = np.array(pd.cut(data[data['ch'] == self.ch_qt_h - 1]['t'], bin_edge, right=False)
                                        .value_counts(sort=False)[2::6])  
                    bg_hv_h_1  = np.array(pd.cut(data[data['ch'] == self.ch_qt_h - 1]['t'], bin_edge, right=False)
                                    .value_counts(sort=False)[3::6])              
                    # probe in both cavities, vertical cavity output
                    transm_hv_v_1 = np.array(pd.cut(data[data['ch'] == self.ch_qt_v - 1]['t'], bin_edge, right=False)
                                        .value_counts(sort=False)[2::6])
                    bg_hv_v_1  = np.array(pd.cut(data[data['ch'] == self.ch_qt_v - 1]['t'], bin_edge, right=False)
                                    .value_counts(sort=False)[3::6]) 
                    
                    # append to dictionary
                    for key in self.key_var_list:
                        exec("self.{}['probe detuning {:.6f} MHz'] = np.vstack((self.{}['probe detuning {:.6f} MHz'], {}_1))"
                             .format(key, detuning, key, detuning, key))
                except:
                    self.warning += '\n Alert: data at run {}, detuning {} MHz was abandoned.'.format(each_run, detuning)
                    
            ## close file
            file.close()
            print(self.warning)

    ## save data
    def __save_data(self):           
        with h5py.File(self.file_path, 'a') as file_write:
            file_write.create_dataset('probe detunings', data = self.detune_list, dtype='float32')
            file_write.create_dataset('keys', data = self.key_var_list)
            file_write.create_dataset('keys with errors', data = self.key_list)
            file_write.create_dataset('time', data = [self.time_pulse_list_h, self.time_pulse_list_hv, self.time_pulse_list_v], dtype='float64')

            # create dataset for each detuning, each dataset contains all runs
            sample_size = []
            for detuning in self.detune_list:
                file_write.create_dataset('probe detuning {:.6f} MHz'.format(detuning), data = [eval("self.{}['probe detuning {:.6f} MHz']".format(key, detuning), {'self':self}) for key in self.key_var_list], dtype = 'float64')
                sample_size.append(eval("self.transm_h['probe detuning {:.6f} MHz'].shape[0]".format(detuning)))

            # save sample sizes
            file_write.create_dataset('sample sizes', data = sample_size, dtype = 'int32')
            
###############################################################################################
# class: bin data into groups
# input[optional]: directory,cavity, bin_start, bin_stop
# outputs: binned data
class Bin:
    def __init__(self,*args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.dir = self.__choose_directory() # choose directory
        self.cavity = GUI().cavity_initial(*self.args, **self.kwargs) # cavity initial
        self.h5_input = os.path.join(self.dir, '_data_{}.h5'.format(self.cavity))
        self.__bin_specs()  # start and stop pulse 
#         self.__check_exist()  # check if binned data exists, decide
        self.__load_processed_data() # load processed data
        self.__statistics_bin()  # statistics
        
    # choose directory
    def __choose_directory(self):
        try: # directory from args
            directory = [value for value in self.args if os.path.isdir(value)][0]  # string array    
        except: # directory from kwargs
            try:
                directory = [value for key,value in self.kwargs.items() 
                         if re.search('^((dir)|(path)|(folder)).*',key, re.IGNORECASE)][0]
            except:  # from GUI
                directory = GUI().dir_gui()
        return directory
        
        
    # load processed data
    def __load_processed_data(self):

        if os.path.isfile(self.h5_input) == False:
            print("Bin() module couldn't find the processed data file '{}'".format(self.file_path))
            sys.exit()
        file = h5py.File(self.h5_input, 'r')
        
        # keys in the file
        self.keys = [key for key in file.keys()]
        
        # assign variables
        self.data = {}
        self.warning = []
        for key, value in file.items():
            try:
                self.data[key] = value[...] 
            except:
                self.warning.append('Warning: data {} is not loaded.'.format(key))
        # close file
        file.close()

    # bin specs
    def __bin_specs(self):
        # the starting and ending pulse numbers
        try: # specify pulses to be binned
            bin_start = [value for key,value in self.kwargs.items() 
                     if re.search('((begin)|(start))',key, re.IGNORECASE)][0]
            bin_stop = [value for key,value in self.kwargs.items() 
                     if re.search('((end)|(stop))',key, re.IGNORECASE)][0]
        except:  # choose the first pulse
            bin_start = 0
            bin_stop  = 1 
            
        if bin_start >= bin_stop:
            print('bin_stop needs to be larger than bin_start!')
            sys.exit()
        self.bin_start = bin_start
        self.bin_stop  = bin_stop
        self.h5_output = os.path.join(self.dir, '_data_{}_bin_start_{}_stop_{}.h5' .format(self.cavity, self.bin_start, self.bin_stop))
        self.xlsx_output = os.path.join(self.dir, '_data_{}_bin_start_{}_stop_{}.xlsx' .format(self.cavity, self.bin_start, self.bin_stop))

    # binned data exist or not
    def __check_exist(self):
        if os.path.isfile(self.h5_output) == True:
            choice = eg.buttonbox('The binned data file already exists. \n\n{}\n\nStill process raw data and generate a new binned data?'.format(self.h5_output), choices=['Go on, generate new file','Stop, use current file'])
            decision = choice[0].lower()
            
            if decision == 'g': # go on
                pass
            else:  # stop, by choice or closing box
                sys.exit()
        # no previous file
        else:
            pass            
 
    # calculate the total mean, deviation of binned data
    def __statistics_bin(self):       
        # iteration over detuning
        data = {'{}'.format(key.decode('ascii')) : [] for key in self.data['keys with errors']}
        for i_detune in pbar(range(len(self.data['probe detunings'])), desc='Binned statistics {} cavity'.format(self.cavity)):
            # detuning
            detuning = self.data['probe detunings'][i_detune]
            # successful runs
            runs = self.data['sample sizes'][i_detune]
            # pulses in the bin
            n_pulses = (self.bin_stop - self.bin_start) * runs
            # data_bin, 3D matrix
            data_select = self.data['probe detuning {:.6f} MHz'.format(detuning)][:,:,self.bin_start:self.bin_stop]
            
            # variables
            for i_key in range(len(self.data['keys'])):
                key = self.data['keys'][i_key].decode('ascii')
                # the counts
                data_var = data_select[i_key,:,:]  # 2D matrix, all
                # statistics
                mean = np.mean(data_var)
                std  = np.std(data_var)
                err_mean  = std/np.sqrt(n_pulses)
                # append to dict
                data['{}'.format(key)].append(mean)
                data['{}_err'.format(key)].append(err_mean)
        # global
        self.bin = data
        # print warnings
        if bool(self.warning):
            print(self.warning)
        
    # export data
    def export(self):
        # export, default h5
        pd.DataFrame(self.bin).to_hdf(self.h5_output, key='data', mode='w')
        
        # also export to .xlsx for fun
        pd.DataFrame(self.bin).to_excel(self.xlsx_output)


###############################################################################################
# class: load processed data and plot
# input: directory[optional]
# outputs: figure
class Plot:
    def __init__(self,*args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.warning = []
        self.dir = self.__choose_directory() # choose directory
        self.cavity = GUI().cavity_initial(*self.args, **self.kwargs) # cavity initial
        self.h5_input = os.path.join(self.dir, '_data_{}.h5'.format(self.cavity))
        self.__load_processed_specs() 
        self.__bin()  # process bin            
        self.__plot_parameters(*self.args, **self.kwargs) # set parameters for plotting
        self.plot(*self.args, **self.kwargs)


    # choose directory
    def __choose_directory(self):
        try: # directory from args
            directory = [value for value in self.args if os.path.isdir(value)][0]  # string array    
        except: # directory from kwargs
            try:
                directory = [value for key,value in self.kwargs.items() 
                         if re.search('^((dir)|(path)|(folder)).*',key, re.IGNORECASE)][0]
            except:  # from GUI
                directory = GUI().dir_gui()
        return directory
    
    # load processed data
    def __load_processed_specs(self):
        if os.path.isfile(self.h5_input) == False:
            print("Plot() module couldn't find the processed data file '{}'".format(self.h5_input))
            sys.exit()
        file = h5py.File(self.h5_input, 'r')
        
        # assign variables
        self.specs = {}
        for key, value in file.items():
            # load parameters, not raw data
            if bool(re.search('(MHz)', key)) == False:
                try:
                    self.specs[key] = value[...] 
                except:
                    pass
        # close file
        file.close()
    
    # bin data
    def __bin(self):
        # the starting and ending pulse numbers
        try: # specify pulses to be binned
            self.bin_start = [value for key,value in self.kwargs.items() 
                     if re.search('((begin)|(start))',key, re.IGNORECASE)][0]
            self.bin_stop = [value for key,value in self.kwargs.items() 
                     if re.search('((end)|(stop))',key, re.IGNORECASE)][0]
        except:  # choose the first pulse
            print('Error: Specify bin_start(stop).')
            sys.exit()
            
        # bin data
        self.data = Bin(path = self.dir, cavity = self.cavity, bin_start = self.bin_start, bin_stop = self.bin_stop).bin
        
        self.data['detune_list'] = self.specs['probe detunings']


        
        
        
        
        
#     # try folder of the month, used in __name_file() function    
#     def __dir_month(self):  
#         year = datetime.date.today().year
#         month = datetime.date.today().month
#         dir_month = os.path.join(self.dir_parent,str(year),str(month))
#         return dir_month
    
#     # file GUI
#     def __name_file(self,*args,**kwargs):
#         ## load data from args or kwargs
#         try:  # file from args
#             name_file = [value for value in args if os.path.isfile(value)][0]        
#         except:
#             try:  # file from args
#                 name_file = [value for key,value in kwargs.items() if re.search('^((path)|(file)).*',key, re.IGNORECASE)][0]
#             except:
#                 name_file = eg.fileopenbox(title='Load processed data',filetypes=['.csv','.h5'],multiple=False,default = self.__dir_month())
#         return name_file
    
#     # cavity name
#     def __name_cavity(self):
#         cavity = re.search('(?<=(_data_))[a-z]*(?=.)', self.file ,re.IGNORECASE).group()
#         return cavity
    
#     # load data from file: .csv or .h5
#     def __load_data(self):
#         if re.search('(.csv)', self.file):
#             data, warning = self.__load_csv()
#         elif re.search('(.h5)', self.file):
#             data, warning = self.__load_h5()
#         self.warning.append(warning)
#         return data

#     # if .csv file
#     def __load_csv(self):    
#         data = {}  # dict
#         warning = []  # str list
#         file = open(self.file, mode = 'r', newline='')
#         reader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC)
#         for row in reader :
#             try: # numeric variable, including numeric list
#                 exec("data['{}'] = {}".format(row[0], row[1]))
#             except:
#                 warning.append('Warning: data {} is not loaded.'.format(row[0]))
#         return data, warning
            
#     # if .h5 file
#     def __load_h5(self):
#         data = {}
#         warning = []
#         file = h5py.File(self.file, 'r')
#         for key, value in file.items():
#             try:
#                 data[key] = value[0]
#             except:
#                 warning.append('Warning: data {} is not loaded.'.format(key))
#         return data, warning
        
    # plot parameter
    def __plot_parameters(self,*args,**kwargs):
        # linestyle
        try:
            self.linestyle = [value for key,value in kwargs.items() if re.search('(linestyle)',key,re.IGNORECASE)][0]
        except:
            self.linestyle = '-'   
            
        # marker
        try:
            self.marker = [value for key,value in kwargs.items() if re.search('(marker)',key,re.IGNORECASE)][0]
        except:
            self.marker = 'o'
            
        # figsize
        try:
            self.__figsize_x = [value[0] for key,value in kwargs.items() if re.search('(size)',key,re.IGNORECASE)][0]
            self.__figsize_y = [value[1] for key,value in kwargs.items() if re.search('(size)',key,re.IGNORECASE)][0]
        except:
            self.__figsize_x = 12
            self.__figsize_y = 10   
            
        # sharex, sharey
        try:
            self.__sharex = [value for key,value in kwargs.items() if re.search('(sharex)',key,re.IGNORECASE)][0]
            self.__sharey = [value for key,value in kwargs.items() if re.search('(sharey)',key,re.IGNORECASE)][0]
        except:
            self.__sharex = False
            self.__sharey = True
            
        # constraint_layout
        try:
            self.__cnstr_lyt = [value for key,value in kwargs.items() if re.search('(constraint_layout)',key,re.IGNORECASE)][0]
        except:
            self.__cnstr_lyt = True
            
        # ylim
        try:
            self.yMax = [value[1] for key,value in kwargs.items() if re.search('(ylim)',key,re.IGNORECASE)][0]
            self.yMin = [value[0] for key,value in kwargs.items() if re.search('(ylim)',key,re.IGNORECASE)][0]
        except:
            pass
        
            
    # error bar choice, (only y)
    def __error_bar(self):
        try:
            err = [value for key,value in self.kwargs.items() if re.search('(?<=(err)).*', key, re.IGNORECASE)][0]
        except:
            err = False
        return err
    
    ## plot figures
    def plot(self,*args,**kwargs):
        # make figure
        self.fig, axes = plt.subplots(nrows=2,ncols=2,figsize=(self.__figsize_x,self.__figsize_y), sharey=self.__sharey,sharex=self.__sharex,constrained_layout=self.__cnstr_lyt)
        ax1 = axes[0,0]
        ax2 = axes[0,1]
        ax3 = axes[1,0]
        ax4 = axes[1,1]

        # plot error bar or not 
        if self.__error_bar() == True: # plot error bars
            # H input, H output 
            ax1.errorbar(self.data['detune_list'], self.data['transm_h'], yerr=self.data['transm_h_err'], linestyle=self.linestyle, marker = self.marker, label = 'Signal')
            ax1.errorbar(self.data['detune_list'], self.data['bg_h'], yerr=self.data['bg_h_err'], linestyle=self.linestyle, marker = self.marker, label = 'Background')
            # H&V input, H output
            ax2.errorbar(self.data['detune_list'], self.data['transm_hv_h'], yerr=self.data['transm_hv_h_err'], linestyle=self.linestyle, marker = self.marker, label = 'Signal')
            ax2.errorbar(self.data['detune_list'], self.data['bg_hv_h'], yerr=self.data['bg_hv_h_err'], linestyle=self.linestyle, marker = self.marker, label = 'Background')
            ## V input, V output
            ax3.errorbar(self.data['detune_list'], self.data['transm_v'], yerr=self.data['transm_v_err'], linestyle=self.linestyle, marker = self.marker, label='Signal')
            ax3.errorbar(self.data['detune_list'], self.data['bg_v'], yerr=self.data['bg_v_err'], linestyle=self.linestyle, marker = self.marker, label = 'Background')
            # H&V input, V output
            ax4.errorbar(self.data['detune_list'], self.data['transm_hv_v'], yerr=self.data['transm_hv_v_err'], linestyle=self.linestyle, marker = self.marker, label = 'Signal')
            ax4.errorbar(self.data['detune_list'], self.data['bg_hv_v'], yerr=self.data['bg_hv_v_err'], linestyle=self.linestyle, marker = self.marker, label = 'Background')
        else:  # no error bars
            # H input, H output
            ax1.plot(self.data['detune_list'], self.data['transm_h'], linestyle=self.linestyle, marker = self.marker, label = 'Signal')
            ax1.plot(self.data['detune_list'], self.data['bg_h'], linestyle=self.linestyle, marker = self.marker, label = 'Background')
            # H&V input, H output
            ax2.plot(self.data['detune_list'], self.data['transm_hv_h'], linestyle=self.linestyle, marker = self.marker, label = 'Signal')
            ax2.plot(self.data['detune_list'], self.data['bg_hv_h'], linestyle=self.linestyle, marker = self.marker, label = 'Background')
            # V input, V output
            ax3.plot(self.data['detune_list'], self.data['transm_v'], linestyle=self.linestyle, marker = self.marker, label='Signal')
            ax3.plot(self.data['detune_list'], self.data['bg_v'], linestyle=self.linestyle, marker = self.marker, label = 'Background')
            # H&V input, V output
            ax4.plot(self.data['detune_list'], self.data['transm_hv_v'], linestyle=self.linestyle, marker = self.marker, label = 'Signal')
            ax4.plot(self.data['detune_list'], self.data['bg_hv_v'], linestyle=self.linestyle, marker = self.marker, label = 'Background')
        
        # ylim
        try:
            for n in [1,2,3,4]:
                exec("ax{}.set_ylim({},{})".format(n, self.yMin, self.yMax))
        except:
            pass
        # axis labels, legends
        ax1.set_title('Horizontal Input, Horizontal Output')
    #     ax1.set_xlabel('Probe Detuning (MHz)')
        ax1.set_ylabel('Counts/Pulse')
        ax1.legend(loc = 'best')

        ax2.set_title('Both Inputs, Horizontal Output')
    #     ax2.set_xlabel('Probe Detuning (MHz)')
    #     ax2.set_ylabel('Counts/Pulse')
        ax2.legend(loc = 'best')

        ax3.set_title('Vertical Input, Vertical Output')
        ax3.legend(loc = 'best')
        ax3.set_xlabel('Probe Detuning (MHz)')
        ax3.set_ylabel('Counts/Pulse');

        ax4.set_title('Both Inputs, Vertical Output')
        ax4.set_xlabel('Probe Detuning (MHz)')
    #     ax4.set_ylabel('Counts/Pulse')
        ax4.legend(loc = 'best')

    # save figure
    def save(self):
        path = os.path.join(self.dir, '_plot_{}_start_{}_stop_{}.png'.format(self.cavity, self.bin_start, self.bin_stop))
        self.fig.savefig(path)