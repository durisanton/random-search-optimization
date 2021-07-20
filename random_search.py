#random search algorithm / Anton Duris(184197)
import math
import time
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib
from tkinter import *
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class GUI:
    def __init__(self,gui):
        self.gui = gui
        self.fig = Figure(figsize = (9,5), dpi = 100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig,self.gui)
        self.ax.set_xlabel("X axis")
        self.ax.set_ylabel("Y axis")
        self.ax.grid()
        self.canvas.get_tk_widget().grid(row = 1,column = 0, columnspan=9, rowspan=5)
        #toolbar
        toolbarFrame = Frame(master=gui)
        toolbarFrame.grid(row=0, column=0)
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
        self.toolbar.update()
        #buttons
        self.btn_function_1 = Button(main_window, text="Function 1", command = lambda: self.plot3d(1))
        self.btn_function_1.grid(row = 8,column = 0)
        self.btn_function_2 = Button(main_window, text="Function 2", command = lambda: self.plot3d(2))
        self.btn_function_2.grid(row = 9,column = 0)
        self.btn_function_3 = Button(main_window, text="Function 3", command = lambda: self.plot3d(3))
        self.btn_function_3.grid(row = 10, column = 0)
        self.btn_function_1contour = Button(main_window, text="Function 1 contour", command = lambda: self.contour(1))
        self.btn_function_1contour.grid(row = 8, column = 1)
        self.btn_function_2contour = Button(main_window, text="Function 2 contour", command = lambda: self.contour(2))
        self.btn_function_2contour.grid(row = 9,column = 1)       
        self.btn_function_3contour = Button(main_window, text="Function 3 contour", command = lambda: self.contour(3))
        self.btn_function_3contour.grid(row = 10,column = 1)
        #input box
        self.x1_lim_input_min = Entry(self.gui, bd =2, width = 5)
        self.x1_lim_input_min.grid(row = 8,column = 4)
        self.x1_lim_input_min.insert(0,'-5.12')
        self.x1_lim_input_max = Entry(self.gui, bd =2, width = 5)
        self.x1_lim_input_max.grid(row = 8,column = 5)
        self.x1_lim_input_max.insert(0,'5.12')
        self.x2_lim_input_min = Entry(self.gui, bd =2, width = 5)
        self.x2_lim_input_min.grid(row = 9,column = 4)
        self.x2_lim_input_min.insert(0,'-5.12')
        self.x2_lim_input_max = Entry(self.gui, bd =2, width = 5)
        self.x2_lim_input_max.grid(row = 9,column = 5)
        self.x2_lim_input_max.insert(0,'5.12')        
        self.density_input = Entry(self.gui, bd =2, width = 5)
        self.density_input.grid(row = 10,column = 4)
        self.density_input.insert(0,'10')
        #labels
        Label(self.gui, text = '3D view').grid(row = 7, column = 0)
        Label(self.gui, text = 'Contour view').grid(row = 7, column = 1)
        Label(self.gui, text = 'X limit:').grid(row = 8, column = 3)
        Label(self.gui, text = 'Y limit:').grid(row = 9, column = 3)
        Label(self.gui, text = 'Density:').grid(row = 10, column = 3)
        Label(self.gui, text = 'Settings:').grid(row = 7, column = 7)
        #list of starting vectors
        Label(self.gui, text = 'List of starting vectors:').grid(row = 1, column = 12)
        self.listbox = Text(self.gui, height = 10, width = 20)
        self.listbox.grid(row = 2, column = 12)
        self.listbox.insert(END,'[1,1]')
        Label(self.gui, text = 'Number of vectors: ').grid(row = 8, column = 6)
        self.iterations = Entry(self.gui, bd = 2, width = 5)
        self.iterations.grid(row = 8, column = 7)
        self.iterations.insert(0,'1')
        self.random_iterations = Button(self.gui,text = 'Random iter. vectors', command = self.random_vectors)
        self.random_iterations.grid(row = 6, column = 12)
        #surroundings
        self.circle_on = IntVar()
        self.square_on = IntVar()
        self.square_on.set(1)
        self.C1 = Checkbutton(self.gui, text = "Square", variable = self.square_on)
        self.C1.grid(row = 9, column = 9)
        self.C2 = Checkbutton(self.gui, text = "Circle", variable = self.circle_on)
        self.C2.grid(row = 10, column = 9)
        Label(self.gui, text = 'Circle radius:').grid(row = 9, column = 6)
        self.circle_radius = Entry(self.gui, bd = 2, width = 5)
        self.circle_radius.grid(row = 9, column = 7)
        self.circle_radius.insert(0,'2')
        Label(self.gui, text = 'Square size:').grid(row = 10, column = 6)
        self.square_size = Entry(self.gui, bd = 2, width = 5)
        self.square_size.grid(row = 10, column = 7)
        self.square_size.insert(0,'2') 
        Label(self.gui, text = 'Surrounding type:').grid(row = 9, column = 8)
        #search
        self.search_btn = Button(self.gui,text = 'Search', command = self.search)
        self.search_btn.grid(row = 7, column = 12)
        #number of iterations
        Label(self.gui, text = 'Number of iterations: ').grid(row = 8, column = 8)
        self.n_iter = Entry(self.gui, bd = 2, width = 5)
        self.n_iter.grid(row = 8, column = 9)
        self.n_iter.insert(0,'100')
        #list of results
        Label(self.gui, text = 'List of results:').grid(row = 3, column = 12)
        self.results = Text(self.gui, height = 10, width = 20)
        self.results.grid(row = 4, column = 12)
        #clear
        self.clear_btn = Button(self.gui,text = 'Clear results table', command = self.clear)
        self.clear_btn.grid(row = 8, column = 12)

    def clear(self):
        self.results.delete('1.0', END)
    
    def input(self):
        self.vectors = []
        self.x1_lim_min = float(self.x1_lim_input_min.get())
        self.x1_lim_max = float(self.x1_lim_input_max.get())
        self.x2_lim_min = float(self.x2_lim_input_min.get())
        self.x2_lim_max = float(self.x2_lim_input_max.get())
        self.density = float(self.density_input.get())
        self.circle_radius_val = float(self.circle_radius.get())
        self.square_size_val = float(self.square_size.get())
        self.n_iter_val = int(self.n_iter.get())
    
    def listbox_content(self):
        for i in range(int(self.iterations.get())):
            test = str(self.listbox.get(str(i+1) + '.0', str(i+2) + '.0-1c'))
            first = (test.split('[')[1]).split(',')[0]
            second = (test.split(',')[1]).split(']')[0]
            self.vectors.append([float(first), float(second)])
    
    def random_vectors(self):
        self.input()
        self.listbox.delete('1.0', END)
        for i in range(int(self.iterations.get())):
            self.listbox.insert(END, '[' + str(round(np.random.uniform(self.x1_lim_min, self.x1_lim_max), 2)) + ',' + str(round(np.random.uniform(self.x2_lim_min, self.x2_lim_max), 2)) + ']\n')
        self.listbox_content()
        
    def init_params(self, arg):
        self.input()
        self.listbox_content()
        self.X = np.append(np.arange(self.x1_lim_min, self.x1_lim_max, 1/self.density), self.x1_lim_max)    
        self.Y = np.append(np.arange(self.x2_lim_min, self.x2_lim_max, 1/self.density), self.x2_lim_max)   
        self.X, self.Y = np.meshgrid(self.X, self.Y)
        self.Z = self.fx(self.X, self.Y, arg)

    def fx(self, x, y, arg):
        if arg == 1:
            self.Z = func_1(x,y)
            self.arg = 1
        elif arg == 2:
            self.Z = func_2(x,y)
            self.arg = 2
        elif arg == 3:
            self.Z = func_3(x,y)
            self.arg = 3

        return self.Z

    def plot3d(self, arg):
        #load initial parameters
        self.init_params(arg)
        #choosing between functions to be plotted
        self.fig.clf()        
        self.ax = self.fig.gca(projection='3d')
        self.ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1, cmap=cm.plasma, linewidth=0, antialiased=False)
        self.cset = self.ax.contour(self.X, self.Y, self.Z, zdir='z', offset=-100, cmap=cm.coolwarm)
        self.canvas.draw()

    def contour(self, arg):
        #load initial parameters
        self.init_params(arg)
        #plotting
        self.fig.clf()
        self.ax = self.fig.add_subplot(111)
        self.ax.contour(self.X, self.Y, self.Z)  
        self.canvas.draw()
        
    def write_to_txt(self):
        self.txt.write('func' + str(self.arg) + ' time: ' +  time.strftime("%Y%m%d-%H%M%S")
 + '\n')
        self.txt.write('start point:' + '[' + str(round(self.x_history[0][0], 2)) + ',' + str(round(self.x_history[0][1], 2)) + ',' + str(round(self.y_history[0])) + ']\n')
        self.txt.write('final point:' + '[' + str(round(self.x_history[self.n_iter_val][0], 2)) + ',' + str(round(self.x_history[self.n_iter_val][1], 2)) + ',' + str(round(self.y_history[self.n_iter_val])) + ']\n')
        self.txt.write('all points[x1,x2,f(x1,x2)]: \n')
        for i in range(self.n_iter_val):
            self.txt.write(str((self.x_history[i][0], self.x_history[i][1], self.y_history[i])) + '\n')
        self.results.insert(END, 'start point:' + '\n' + '[' + str(round(self.x_history[0][0], 2)) + ',' + str(round(self.x_history[0][1], 2)) + ',' + str(round(self.y_history[0])) + ']\n')
        self.results.insert(END, 'final point:' + '\n' + '[' + str(round(self.x_history[self.n_iter_val][0], 2)) + ',' + str(round(self.x_history[self.n_iter_val][1], 2)) + ',' + str(round(self.y_history[self.n_iter_val])) + ']\n')

    def search(self):    
        def minimal_step_value():
            def random_step():
                #generates vector based on chosen step type
                if self.circle_on.get() == 1:
                    a = np.random.randn()
                    b = np.random.randn()
                    while abs(a) > self.circle_radius_val: 
                        while abs(b) > self.circle_radius_val: 
                            if abs(b) < self.circle_radius_val:
                                break
                            else:
                                b = np.random.randn()
                        if abs(a) < self.circle_radius_val:
                            break
                        else:
                            a = np.random.randn()

                    r = np.array([a*np.cos(self.x[0]),b*np.sin(self.x[1])])
                elif self.square_on.get() == 1:
                    r = np.array([np.random.uniform(-self.square_size_val, self.square_size_val), 
                                  np.random.uniform(-self.square_size_val, self.square_size_val)])
                xt = self.x.copy()
                #generate new coordinates by adding generated step
                for j in range(r.size):
                    xt[j] = self.x[j] + r[j]
                    #set new step to bound if it is out of bound
                    if xt[j] < self.x1_lim_min:
                        xt[j] = self.x1_lim_min
                    elif xt[j] > self.x1_lim_max:
                        xt[j] = self.x1_lim_max
                    elif xt[j] < self.x2_lim_min:
                        xt[j] = self.x2_lim_min
                    elif xt[j] > self.x2_lim_max:
                        xt[j] = self.x2_lim_max
                return xt

            xt_history = []
            yt_history = []
            xt_history.append(self.x)
            yt_history.append(self.y)
            #gernerates defined number of steps
            for i in range(42):
                xt = random_step()
                yt = self.fx(xt[0], xt[1], self.arg)
                xt_history.append(xt)
                yt_history.append(yt)
            #minimum value of y
            idx = np.argmin(yt_history)
            #returns new coordinates with lowest function value
            return np.array(xt_history[idx])

        self.init_params(self.arg)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        self.txt = open(('random_search_' + timestr +  '.txt'), 'w+')
        for j in range(int(self.iterations.get())):
            self.x = np.array(self.vectors[j])
            #initialize history matrixes
            self.x_history = [self.x]
            self.y = self.fx(self.x[0], self.x[1], self.arg)
            self.y_history = [self.y]
            no_change = 0 #used if value is not changing
            xt = np.copy(self.x)
            #iteration 
            for i in range(self.n_iter_val):
                #new step
                xt = minimal_step_value()
                self.init_params(self.arg)
                yt = self.fx(xt[0], xt[1], self.arg)
                #if new value is greater than previous value -> use previous value
                if yt < np.min(self.y_history):
                    self.y = yt
                    self.x = np.copy(xt)
                else:
                    no_change += 1

                if (no_change > 20) & (self.square_size_val > 0.0001) & (self.square_on == 1):
                    self.square_size_val *= 0.6
                    no_change = 0    
                elif (no_change > 20) & (self.circle_radius_val > 0.0001) & (self.circle_on == 1):
                    self.circle_radius_val *= 0.6
                    no_change = 0    
                elif no_change > 100:
                    self.n_iter_val = i
                    break
                #all iterations
                self.x_history.append(self.x)
                self.y_history.append(self.y)

            x = []
            y = []
            for k in range(self.n_iter_val):
                x.append(self.x_history[k][0])
                y.append(self.x_history[k][1])
            self.ax.plot(x,y)
            self.ax.plot(self.x_history[0][0], self.x_history[0][1], 'ro')
            self.ax.plot(self.x_history[self.n_iter_val][0], self.x_history[self.n_iter_val][1], 'gx')
            self.canvas.draw()
            self.write_to_txt() 
        self.txt.close()

def func_1(x,y):
    return x**2 + y**2

def func_2(x, y, **kwargs):
    A = kwargs.get('A', 10)
    return A + (x**2 - A * np.cos(2 * math.pi * x)) + (y**2 - A * np.cos(2 * math.pi * y))

def func_3(x, y, **kwargs):
    A = kwargs.get('A', 418.9829)
    return A - (x * np.sin(np.sqrt(np.abs(x))) + y * np.sin(np.sqrt(np.abs(y))))


if __name__ == '__main__':
    main_window = Tk()
    main_window.config(background='white')
    #main_window.geometry("1000x700")
    #Label(main_window, text="Ultimate GUI for searching function minimum", bg = 'white')
    GUI(main_window)
    main_window.mainloop()


