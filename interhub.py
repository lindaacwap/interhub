import psutil
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

class InterHub:
    def __init__(self, master):
        self.master = master
        self.master.title("InterHub Memory Manager")
        
        self.create_widgets()
        
        self.update_memory_info()
        
    def create_widgets(self):
        self.memory_label = ttk.Label(self.master, text="Memory Usage:")
        self.memory_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.memory_info = ttk.Label(self.master, text="", width=30)
        self.memory_info.grid(row=0, column=1, padx=10, pady=10)
        
        self.refresh_button = ttk.Button(self.master, text="Refresh", command=self.update_memory_info)
        self.refresh_button.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.plot_button = ttk.Button(self.master, text="Plot Memory Usage", command=self.plot_memory_usage)
        self.plot_button.grid(row=2, column=0, columnspan=2, pady=10)
        
    def update_memory_info(self):
        mem = psutil.virtual_memory()
        self.memory_info.config(text=f"Used: {mem.used // (1024 ** 2)} MB / Total: {mem.total // (1024 ** 2)} MB")
        
    def plot_memory_usage(self):
        def plot_thread():
            plt.ion()
            fig, ax = plt.subplots()
            ax.set_ylabel('Memory Usage (MB)')
            ax.set_xlabel('Time (s)')
            ax.set_title('Real-time Memory Usage')
            
            x_data, y_data = [], []
            start_time = time.time()
            
            while True:
                current_time = time.time() - start_time
                mem = psutil.virtual_memory()
                x_data.append(current_time)
                y_data.append(mem.used / (1024 ** 2))
                
                ax.plot(x_data, y_data, color='b')
                plt.draw()
                plt.pause(1)
                
                if len(x_data) > 60:  # Keep last 60 seconds of data
                    x_data.pop(0)
                    y_data.pop(0)
                    
        Thread(target=plot_thread, daemon=True).start()

def main():
    root = tk.Tk()
    app = InterHub(master=root)
    root.mainloop()

if __name__ == "__main__":
    main()