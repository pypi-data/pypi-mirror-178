#!/usr/bin/env python
# coding: utf-8

# In[4]:


import tkinter as tk
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import re
import numpy as np
##########################################################################################################
# class for fit two cavities
#     x_h(v) and y_h(v) are frequencies and transmissions for h(v) cavity
#     parameters = par_min_h + par_ini_h + par_max_h + par_min_v + par_ini_v + par_max_v
#     needs tk.Tk() and tk.mainloop()
class Fit2Cavity:
    def __init__(self,window,x_h,y_h,x_v,y_v,parameters):
        self.window = window
        window.title('Cavity Resonance Fitting')
        self.__freq_h   = x_h
        self.__freq_v   = x_v
        self.__transm_h = y_h
        self.__transm_v = y_v
        self.__par_list_0  = parameters
        self.__entries  = []

        # label frames for two input tables
        self.__lf_h = tk.LabelFrame(master = self.window, text = 'Horizontal Cavity', font=('Arial',18),bd=2) 
        self.__lf_h.grid(row = 0, column = 0, columnspan = 5,  padx=5, pady = 5)
        self.__lf_v = tk.LabelFrame(master = self.window, text = 'Vertical Cavity', font=('Arial',18),bd=2)
        self.__lf_v.grid(row=0, column=5, columnspan=5,  padx=5,pady=5)

        # labels for parameters
        __row_0_column_1 = tk.Label(master = self.__lf_h, text = 'Lower Limit').grid(row=0,column=2)
        __row_0_column_2 = tk.Label(master = self.__lf_h, text = 'Initial Parameters').grid(row=0,column=3)
        __row_0_column_3 = tk.Label(master = self.__lf_h, text = 'Upper Limit').grid(row=0,column=4)
        __row_0_column_4 = tk.Label(master = self.__lf_h, text = 'Optimized').grid(row=0,column=1)

        __row_0_column_6 = tk.Label(master = self.__lf_v, text = 'Lower Limit').grid(row=0,column=7)
        __row_0_column_7 = tk.Label(master = self.__lf_v, text = 'Initial Parameters').grid(row=0,column=8)
        __row_0_column_8 = tk.Label(master = self.__lf_v, text = 'Upper Limit').grid(row=0,column=9)
        __row_0_column_5 = tk.Label(master = self.__lf_v, text = 'Optimized').grid(row=0,column=6)


        __row_1_column_0 = tk.Label(master = self.__lf_h, text = 'Resonance (MHz)').grid(row=1,column=0)
        __row_2_column_0 = tk.Label(master = self.__lf_h, text = 'Linewidth (MHz)').grid(row=2,column=0)
        __row_3_column_0 = tk.Label(master = self.__lf_h, text = 'Amplitude').grid(row=3,column=0)
        __row_4_column_0 = tk.Label(master = self.__lf_h, text = 'Dark Counts').grid(row=4,column=0)
        __row_1_column_4 = tk.Label(master = self.__lf_v, text = 'Resonance (MHz)').grid(row=1,column=4)
        __row_2_column_4 = tk.Label(master = self.__lf_v, text = 'Linewidth (MHz)').grid(row=2,column=4)
        __row_3_column_4 = tk.Label(master = self.__lf_v, text = 'Amplitude').grid(row=3,column=4)
        __row_4_column_4 = tk.Label(master = self.__lf_v, text = 'Dark Counts').grid(row=4,column=4)

        # Entry: input parameters, starting from initial ones
        __i_par = 0
        # horizontal cavity fitting parameters
        for j in [2,3,4]:
            for i in [1,2,3,4]:
                __entry = tk.Entry(master = self.__lf_h, relief=tk.GROOVE, width=10)
                __entry.grid(row=i, column=j, pady=2.5) #  sticky=NSEW,
                __entry.insert(tk.END, self.__par_list_0[__i_par])
                self.__entries.append(__entry)
                __i_par = __i_par + 1
        # vertical cavity fitting parameters
        for j in [7,8,9]:
            for i in [1,2,3,4]:
                __entry = tk.Entry(master = self.__lf_v, relief=tk.GROOVE, width=10)
                __entry.grid(row=i, column=j, pady=2.5) #  sticky=NSEW,
                __entry.insert(tk.END, self.__par_list_0[__i_par])
                self.__entries.append(__entry)
                __i_par = __i_par + 1

        # engage initial fitting
        self.button_save()
        self.button_display('horizontal')
        self.button_display('vertical')

        # button frames 
        __button_frame = tk.Frame(master=self.window)
        __button_frame.grid(row=5, column=0, columnspan=10)
        # button for fit
        __button_1 = tk.Button(master=__button_frame,text='Save & Fit',
                     command=lambda:[self.button_save(),
                                     self.button_display('horizontal'),
                                     self.button_display('vertical')],
                     font=('Arial',15), width=20,height=2,relief=tk.RAISED,bd=3)
        __button_1.pack(side=tk.LEFT)
        # button for close
        __button_2 = tk.Button(master=__button_frame, text='Close',command=self.button_close,
                             font=('Arial',15), width=20,height=2, relief=tk.RAISED,bd=3)
        __button_2.pack(side=tk.LEFT)

    # choose which cavity to assign fitted parameters
    def __save_par_fit(self,cavity):
        if re.search('^h.*',cavity,re.IGNORECASE) != None:
            self.__par_fit_h = self.__par_fit
        elif re.search('^v.*',cavity,re.IGNORECASE) != None:
            self.__par_fit_v = self.__par_fit
       
    # optimized fitting parameters
    def parameters(self, cavity): 
        if re.search('^h.*',cavity,re.IGNORECASE) != None:
            return self.__par_fit_h
        elif re.search('^v.*',cavity,re.IGNORECASE) != None:
            return self.__par_fit_v  
    # resonance
    def resonance(self, cavity):
        return self.parameters(cavity)[0]
    # linewidth
    def linewidth(self, cavity):
        return self.parameters(cavity)[1]
    # dark counts
    def amplitude(self, cavity):
        return self.parameters(cavity)[2]
    # dark counts
    def background(self, cavity):
        return self.parameters(cavity)[3] 
    # lorentzian
    def lorentz(self,x,x0,fwhm,a,b):   # a - amplitude, k - linewidth, x0-center, b - background
        self.value = a * (fwhm/2)**2 / ( (fwhm/2)**2 + (x - x0)**2 ) + b
        return self.value

            
    # button to save input fitting parameters
    def button_save(self):
#         self.figure.savefig('fit_two_cavity.png')
        self.__par_list = []
        __i_par = 0   # index
        for j in [2,3,4,7,8,9]:
            for i in [1,2,3,4]:
                self.__par_list.append(float(self.__entries[__i_par].get()))
                __i_par = __i_par + 1
        return self.__par_list
    # button to display fitted value
    def button_display(self,cavity):
        if re.search('^h.*',cavity,re.IGNORECASE) != None:
            __master = self.__lf_h
            __col    = 0
            __par_in = self.__par_list[0:12]    
#             __x      = x_h
#             __y      = y_h
            __x      = self.__freq_h
            __y      = self.__transm_h
            __title  = 'Horizontal Cavity'
            __cavity = 'horizontal'
        elif re.search('^v.*',cavity,re.IGNORECASE) != None:
            __master = self.__lf_v
            __col    = 5
            __par_in = self.__par_list[12:24]        
#             __x      = x_v
#             __y      = y_v
            __x      = self.__freq_v
            __y      = self.__transm_v
            __title  = 'Vertical Cavity'
            __cavity = 'vertical'

        # fit curves, display fitted parameters & curves
        self.tk_plot(__x,__y,6,__col,title=__title,parameter=__par_in, cavity=__cavity)
        self.__save_par_fit(__cavity)
        # display optimized parameters
        for i in [1,2]:  # read only display fitted parameters, resonance & linewidth
            __par_show   = tk.StringVar()
            __entry = tk.Entry(master = __master, textvariable=__par_show, relief=tk.RIDGE, width=10, 
                               state = tk.DISABLED, disabledforeground="black") #, disabledbackground="#1E6FBA"
            __par_show.set('{:.1f}'.format(self.__par_fit[i-1]))
            __entry.grid(row=i, column=__col+1, pady=2.5) #  sticky=NSEW,
        for i in [3,4]:  # read only display of fitted parameters, Counts
            __par_show   = tk.StringVar()
            __entry = tk.Entry(master = __master, textvariable=__par_show, relief=tk.RIDGE, width=10, 
                               state = tk.DISABLED, disabledforeground="black")#, justify='center'
            __par_show.set('{:.3e}'.format(self.__par_fit[i-1]))
            __entry.grid(row=i, column=__col+1, pady=2.5) #  sticky=NSEW,


    # button for close window
    def button_close(self):
        self.window.destroy()
#         self.window.quit()

    # plot fitting in tkinter window
    def tk_plot(self,x,y,row,col,**kwargs):  # arg: []
        # the figure that will contain the plot
        __fig = Figure(figsize = (5, 4), dpi = 100)
        __subplot = __fig.add_subplot(1,1,1)
#         __subplot.plot(x,y,'go-.')
        __subplot.plot(x,y,'.')

        __txt = ['Data']
        # title
        if 'title' in kwargs:
            __subplot.set_title('{}'.format(kwargs['title']))
        # xlabel, default = 'MHz'
        if 'xlabel' in kwargs:
            __subplot.set_xlabel('{}'.format(kwargs['xlabel']))
        else:
            __subplot.set_xlabel('MHz')
        # ylabel, default = 'title'
        if 'ylabel' in kwargs:
            __subplot.set_ylabel('{}'.format(kwargs['ylabel']))
        else:
            __subplot.set_ylabel('Counts')
            
        # fit, only if parameters are provided
        if any(re.search('^(par).*',key,re.IGNORECASE) for key in kwargs):
            # find the parameter
            for key in kwargs:
                if re.search('^(par).*',key,re.IGNORECASE):
                    __par_list = kwargs[key]
            # (x, amplitude=1.0, center=0.0, sigma=1.0)
            self.__par_fit, self.__par_fit_cov = curve_fit(self.lorentz, x, y, 
                                                 p0=__par_list[4:8], 
                                                 bounds=(__par_list[0:4],__par_list[8:12]))
#             __subplot.plot(x,self.lorentz(x,*__par_fit),'r-')
            __subplot.plot(x,self.lorentz(x,*self.__par_fit))
            __txt.append('Fit')
        __subplot.legend(__txt,fontsize = 'small')        
        
        # creating the Tkinter canvas containing the Matplotlib figure
        __canvas = FigureCanvasTkAgg(__fig, master = self.window)  
        __canvas.draw()
        __canvas.get_tk_widget().grid(row=row,column=col,columnspan=5)

        # creating the Matplotlib toolbar
        __toolbar_frame = tk.Frame(master=self.window)
        __toolbar_frame.grid(row=row+1, column=col, columnspan=5)
        __toolbar = NavigationToolbar2Tk(__canvas, __toolbar_frame)
        __toolbar.update()
        
        # global figure
        self.figure = __fig


        
class FitCavity:
    def __init__(self,window,x_h,y_h,parameters):
        self.window = window
        window.title('Cavity Resonance Fitting')
        self.__freq_h   = x_h
        self.__transm_h = y_h
        self.__par_list_0  = parameters
        self.__entries  = []

        # label frames for the input table
        self.__lf_h = tk.LabelFrame(master = self.window, text = 'Fitting Parameters', font=('Arial',18),bd=2) 
        self.__lf_h.grid(row = 0, column = 0, columnspan = 5,  padx=5, pady = 5)

        # labels for parameters
        __row_0_column_1 = tk.Label(master = self.__lf_h, text = 'Lower Limit').grid(row=0,column=2)
        __row_0_column_2 = tk.Label(master = self.__lf_h, text = 'Initial Parameters').grid(row=0,column=3)
        __row_0_column_3 = tk.Label(master = self.__lf_h, text = 'Upper Limit').grid(row=0,column=4)
        __row_0_column_4 = tk.Label(master = self.__lf_h, text = 'Optimized').grid(row=0,column=1)

        __row_1_column_0 = tk.Label(master = self.__lf_h, text = 'Resonance (MHz):').grid(row=1,column=0)
        __row_2_column_0 = tk.Label(master = self.__lf_h, text = 'Linewidth (MHz):').grid(row=2,column=0)
        __row_3_column_0 = tk.Label(master = self.__lf_h, text = 'Peak Counts:').grid(row=3,column=0)
        __row_4_column_0 = tk.Label(master = self.__lf_h, text = 'Dark Counts:').grid(row=4,column=0)

        # Entry: input parameters, starting from initial ones
        __i_par = 0
        # horizontal cavity fitting parameters
        for j in [2,3,4]:
            for i in [1,2,3,4]:
                __entry = tk.Entry(master = self.__lf_h, relief=tk.GROOVE, width=10)
                __entry.grid(row=i, column=j, pady=2.5) #  sticky=NSEW,
                __entry.insert(tk.END, self.__par_list_0[__i_par])
                self.__entries.append(__entry)
                __i_par = __i_par + 1

        # engage initial fitting
        self.button_save()
        self.button_display()

        # button frames 
        __button_frame = tk.Frame(master=self.window)
        __button_frame.grid(row=5, column=0, columnspan=10)
        # button for fit
        __button_1 = tk.Button(master=__button_frame,text='Save & Fit',
                     command=lambda:[self.button_save(),
                                     self.button_display()],
                     font=('Arial',15), width=20,height=2,relief=tk.RAISED,bd=3)
        __button_1.pack(side=tk.LEFT)
        # button for close
        __button_2 = tk.Button(master=__button_frame, text='Close',command=self.button_close,
                             font=('Arial',15), width=20,height=2, relief=tk.RAISED,bd=3)
        __button_2.pack(side=tk.LEFT)
       
    # optimized fitting parameters
    def parameters(self, *cavity):
        return self.__par_fit
    
    # resonance
    def resonance(self, *cavity):
        return self.parameters(cavity)[0]
    # linewidth
    def linewidth(self, *cavity):
        return self.parameters(cavity)[1]
    # dark counts
    def amplitude(self, *cavity):
        return self.parameters(cavity)[2]
    # dark counts
    def background(self, *cavity):
        return self.parameters(cavity)[3] 
    # lorentzian
    def lorentz(self,x,x0,fwhm,a,b):   # a - amplitude, k - linewidth, x0-center, b - background
        self.value = a * (fwhm/2)**2 / ( (fwhm/2)**2 + (x - x0)**2 ) + b
        return self.value

            
    # button to save input fitting parameters
    def button_save(self):
#         self.figure.savefig('fit_cavity.png')
        self.__par_list = []
        __i_par = 0   # index
        for j in [2,3,4]:
            for i in [1,2,3,4]:
                self.__par_list.append(float(self.__entries[__i_par].get()))
                __i_par = __i_par + 1
        return self.__par_list
    # button to display fitted value
    def button_display(self,*cavity):
        __master = self.__lf_h
        __col    = 0
        __par_in = self.__par_list    
        __x      = self.__freq_h
        __y      = self.__transm_h
        __title  = 'Cavity'
        # fit curves, display fitted parameters & curves
        self.tk_plot(__x,__y,6,__col,title=__title,parameter=__par_in)
        # display optimized parameters
        for i in [1,2]:  # read only display fitted parameters, resonance & linewidth
            __par_show   = tk.StringVar()
            __entry = tk.Entry(master = __master, textvariable=__par_show, relief=tk.RIDGE, width=10, 
                               state = tk.DISABLED, disabledforeground="black") #, disabledbackground="#1E6FBA"
            __par_show.set('{:.1f}'.format(self.__par_fit[i-1]))
            __entry.grid(row=i, column=__col+1, pady=2.5) #  sticky=NSEW,
        for i in [3,4]:  # read only display of fitted parameters, Counts
            __par_show   = tk.StringVar()
            __entry = tk.Entry(master = __master, textvariable=__par_show, relief=tk.RIDGE, width=10, 
                               state = tk.DISABLED, disabledforeground="black")#, justify='center'
            __par_show.set('{:.3e}'.format(self.__par_fit[i-1]))
            __entry.grid(row=i, column=__col+1, pady=2.5) #  sticky=NSEW,


    # button for close window
    def button_close(self):
        self.window.destroy()
#         self.window.quit()

    # plot fitting in tkinter window
    def tk_plot(self,x,y,row,col,**kwargs):  # arg: []
        # the figure that will contain the plot
        __fig = Figure(figsize = (5, 4), dpi = 100)
        __subplot = __fig.add_subplot(1,1,1)
#         __subplot.plot(x,y,'go-.')
        __subplot.plot(x,y,'.')

        __txt = ['Data']
        # title
        if 'title' in kwargs:
            __subplot.set_title('{}'.format(kwargs['title']))
        # xlabel, default = 'MHz'
        if 'xlabel' in kwargs:
            __subplot.set_xlabel('{}'.format(kwargs['xlabel']))
        else:
            __subplot.set_xlabel('MHz')
        # ylabel, default = 'title'
        if 'ylabel' in kwargs:
            __subplot.set_ylabel('{}'.format(kwargs['ylabel']))
        else:
            __subplot.set_ylabel('Counts')
            
        # fit, only if parameters are provided
        if any(re.search('^(par).*',key,re.IGNORECASE) for key in kwargs):
            # find the parameter
            for key in kwargs:
                if re.search('^(par).*',key,re.IGNORECASE):
                    __par_list = kwargs[key]
            # (x, amplitude=1.0, center=0.0, sigma=1.0)
            self.__par_fit, self.__par_fit_cov = curve_fit(self.lorentz, x, y, 
                                                 p0=__par_list[4:8], 
                                                 bounds=(__par_list[0:4],__par_list[8:12]))
#             __subplot.plot(x,self.lorentz(x,*__par_fit),'r-')
            __subplot.plot(x,self.lorentz(x,*self.__par_fit))
            __txt.append('Fit')
        __subplot.legend(__txt,fontsize = 'small')        
        
        # creating the Tkinter canvas containing the Matplotlib figure
        __canvas = FigureCanvasTkAgg(__fig, master = self.window)  
        __canvas.draw()
        __canvas.get_tk_widget().grid(row=row,column=col,columnspan=5)

        # creating the Matplotlib toolbar
        __toolbar_frame = tk.Frame(master=self.window)
        __toolbar_frame.grid(row=row+1, column=col, columnspan=5)
        __toolbar = NavigationToolbar2Tk(__canvas, __toolbar_frame)
        __toolbar.update()
        
        # global figure
        self.figure = __fig

# ##########################################################################################################
# # class for fit one cavity
# class FitCavity:
#     def __init__(self,window,x_h,y_h,parameters):
#         self.window = window
#         window.title('Cavity Resonance Fitting')
#         self.__freq_h   = x_h
#         self.__transm_h = y_h
#         self.__par_list_0  = parameters
#         self.__entries  = []

#         # label frames for the input table
#         self.__lf_h = tk.LabelFrame(master = self.window, text = 'Fitting Parameters', font=('Arial',18),bd=2) 
#         self.__lf_h.grid(row = 0, column = 0, columnspan = 5,  padx=5, pady = 5)

#         # labels for parameters
#         __row_0_column_1 = tk.Label(master = self.__lf_h, text = 'Lower Limit').grid(row=0,column=2)
#         __row_0_column_2 = tk.Label(master = self.__lf_h, text = 'Initial Parameters').grid(row=0,column=3)
#         __row_0_column_3 = tk.Label(master = self.__lf_h, text = 'Upper Limit').grid(row=0,column=4)
#         __row_0_column_4 = tk.Label(master = self.__lf_h, text = 'Optimized').grid(row=0,column=1)

#         __row_1_column_0 = tk.Label(master = self.__lf_h, text = 'Resonance (MHz):').grid(row=1,column=0)
#         __row_2_column_0 = tk.Label(master = self.__lf_h, text = 'Linewidth (MHz):').grid(row=2,column=0)
#         __row_3_column_0 = tk.Label(master = self.__lf_h, text = 'Peak Counts:').grid(row=3,column=0)
#         __row_4_column_0 = tk.Label(master = self.__lf_h, text = 'Dark Counts:').grid(row=4,column=0)

#         # Entry: input parameters, starting from initial ones
#         __i_par = 0
#         # horizontal cavity fitting parameters
#         for j in [2,3,4]:
#             for i in [1,2,3,4]:
#                 __entry = tk.Entry(master = self.__lf_h, relief=tk.GROOVE, width=10)
#                 __entry.grid(row=i, column=j, pady=2.5) #  sticky=NSEW,
#                 __entry.insert(tk.END, self.__par_list_0[__i_par])
#                 self.__entries.append(__entry)
#                 __i_par = __i_par + 1
   
#         # engage initial fitting
#         self.button_save()
#         self.tk_plot(x_h,y_h,6,0,par=self.__par_list,title='Cavity Transmission')
#         self.button_display()

#         # button frames 
#         __button_frame = tk.Frame(master=self.window)
#         __button_frame.grid(row=5, column=0, columnspan=8)
#         # button for fit
#         __button_1 = tk.Button(master=__button_frame,text='Fit & Save',
#                  command=lambda:[self.button_save(),
#                                  self.tk_plot(x_h,y_h,6,0,par=self.__par_list,title='Cavity Transmission'),
#                                  self.button_display()],
#                  font=('Arial',15), width=20,height=2,relief=tk.RAISED,bd=3)
#         __button_1.pack(side=tk.LEFT)
#         # button for close
#         __button_2 = tk.Button(master=__button_frame, text='Close',command=self.button_close,
#                              font=('Arial',15), width=20,height=2, relief=tk.RAISED,bd=3)
#         __button_2.pack(side=tk.LEFT)

#     # optimized fitting parameters    
#     def parameters(self):  
#         return self.__par_fit
#     # resonance
#     def resonance(self):
#         return self.parameters()[0]
#     # linewidth
#     def linewidth(self):
#         return self.parameters()[1]
#     # dark counts
#     def amplitude(self):
#         return self.parameters()[2]
#     # dark counts
#     def background(self):
#         return self.parameters()[3]                      
#     # lorentzian
#     def lorentz(self,x,x0,fwhm,a,b):   # a - amplitude, k - linewidth, x0-center, b - background
#         self.value = a * (fwhm/2)**2 / ( (fwhm/2)**2 + (x - x0)**2 ) + b
#         return self.value

            
#     # button to save values
#     def button_save(self):
# #         self.figure.savefig('fit_cavity.png')
#         self.__par_list = []
#         __i_par = 0   # index
#         for j in [1,2,3]:
#             for i in [1,2,3,4]:
#                 self.__par_list.append(float(self.__entries[__i_par].get()))
#                 __i_par = __i_par + 1
#         return self.__par_list
#     # button to display fitted value
#     def button_display(self):
#         for i in [1,2]:  # read only display fitted parameters, resonance & linewidth
#             __par_show   = tk.StringVar()
#             __entry = tk.Entry(master = self.__lf_h, textvariable=__par_show, relief=tk.RIDGE, width=10, 
#                                state = tk.DISABLED, disabledforeground="black") #, disabledbackground="#1E6FBA"
#             __par_show.set('{:.1f}'.format(self.__par_fit[i-1]))
#             __entry.grid(row=i, column=1, pady=2.5) #  sticky=NSEW,
#         for i in [3,4]:  # read only display of fitted parameters, Counts
#             __par_show   = tk.StringVar()
#             __entry = tk.Entry(master = self.__lf_h, textvariable=__par_show, relief=tk.RIDGE, width=10, 
#                                state = tk.DISABLED, disabledforeground="black")#, justify='center'
#             __par_show.set('{:.3e}'.format(self.__par_fit[i-1]))
#             __entry.grid(row=i, column=1, pady=2.5) #  sticky=NSEW,

#     # button for close window
#     def button_close(self):
#         self.window.destroy()
# #         self.window.quit()

#     # plot fitting in tkinter window
#     def tk_plot(self,x,y,row,col,**kwargs):  # arg: []
#         # the figure that will contain the plot
#         __fig = Figure(figsize = (5, 4), dpi = 100)
#         __subplot = __fig.add_subplot(1,1,1)
#         __subplot.plot(x,y,'.')

#         __txt = ['Data']
#         # title
#         if 'title' in kwargs:
#             __subplot.set_title('{}'.format(kwargs['title']))
#         # xlabel, default = 'MHz'
#         if 'xlabel' in kwargs:
#             __subplot.set_xlabel('{}'.format(kwargs['xlabel']))
#         else:
#             __subplot.set_xlabel('MHz')
#         # ylabel, default = 'title'
#         if 'ylabel' in kwargs:
#             __subplot.set_ylabel('{}'.format(kwargs['ylabel']))
#         else:
#             __subplot.set_ylabel('Counts')
        
#         # fit, only if parameters are provided
#         if any(re.search('^(par).*',key,re.IGNORECASE) for key in kwargs):
#             # find the parameter
#             for key in kwargs:
#                 if re.search('^(par).*',key,re.IGNORECASE):
#                     __par_list = kwargs[key]
#             # (x, amplitude=1.0, center=0.0, sigma=1.0)
#             self.__par_fit, self.__par_fit_cov = curve_fit(self.lorentz, x, y, 
#                                                  p0=__par_list[4:8], 
#                                                  bounds=(__par_list[0:4],__par_list[8:12]))
#             __subplot.plot(x,self.lorentz(x,*self.__par_fit))
#             __txt.append('Fit')
#         __subplot.legend(__txt,fontsize = 'small')        
        
#         # creating the Tkinter canvas containing the Matplotlib figure
#         __canvas = FigureCanvasTkAgg(__fig, master = self.window)  
#         __canvas.draw()
#         __canvas.get_tk_widget().grid(row=row,column=col,columnspan=5)

#         # creating the Matplotlib toolbar
#         __toolbar_frame = tk.Frame(master=self.window)
#         __toolbar_frame.grid(row=row+1, column=col, columnspan=5)
#         __toolbar = NavigationToolbar2Tk(__canvas, __toolbar_frame)
#         __toolbar.update()
        
#         # save figure
#         self.figure = __fig


        
# # # this is used as main module        
# if __name__ == '__main__':
#     window = tk.Tk()
# #     par_fit_2 = Fit2Cavity(window,x_h,y_h,x_v,y_v,par_list_0)
#     par_fit_1 = FitCavity(window,x_h,y_h,par_list_0[0:12])
#     window.mainloop()  

# # window = tk.Tk()
# # x = fit_cavity(window,x_h,y_h,x_v,y_v,par_list_0)
# # window.mainloop()  

