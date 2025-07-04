import tkinter as tk
from tkinter import ttk
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from collections import deque

class SystemMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("System Health Monitor")
        self.geometry("700x500")

        tab_control = ttk.Notebook(self)
        self.cpu_tab = tk.Frame(tab_control, bg="#2b2b2b")
        self.ram_tab = tk.Frame(tab_control, bg="#1e1e2f")
        self.fan_tab = tk.Frame(tab_control, bg="#223344")


        tab_control.add(self.cpu_tab, text="CPU")
        tab_control.add(self.ram_tab, text="RAM")
        tab_control.add(self.fan_tab, text="FAN")
        tab_control.pack(expand=1, fill="both")

        self.init_cpu_tab()
        self.init_ram_tab()
        self.init_fan_tab()

    def init_cpu_tab(self):
        self.cpu_label = ttk.Label(self.cpu_tab, text="", font=("Segoe UI", 14))
        self.cpu_label.pack()

        fig, self.ax = plt.subplots(figsize=(6, 2.5), dpi=100)
        self.cpu_x = deque(maxlen=60)
        self.cpu_y = deque(maxlen=60)
        self.cpu_line, = self.ax.plot([], [], color='lime', linewidth=2)

        self.ax.set_title("CPU Usage Over Time")
        self.ax.set_ylim(0, 100)
        self.ax.set_ylabel("CPU %")
        self.ax.set_xlabel("Time")
        self.ax.grid(True)

        self.cpu_canvas = FigureCanvasTkAgg(fig, master=self.cpu_tab)
        self.cpu_canvas.get_tk_widget().pack()

        self.anim = animation.FuncAnimation(fig, self.update_cpu_plot, interval=1000)

    def update_cpu_plot(self, i):
        usage = psutil.cpu_percent()
        self.cpu_label.config(text=f"Current CPU Usage: {usage}%")
        self.cpu_y.append(usage)
        self.cpu_x.append(i)

        self.cpu_line.set_data(self.cpu_x, self.cpu_y)
        self.ax.set_xlim(max(0, i - 60), i)
        return self.cpu_line,

    def init_ram_tab(self):
        self.ram_label = ttk.Label(self.ram_tab, text="", font=("Segoe UI", 14))
        self.ram_label.pack(pady=10)

        self.ram_progress = ttk.Progressbar(self.ram_tab, orient='horizontal', length=400, mode='determinate')
        self.ram_progress.pack(pady=5)

        self.after(1000, self.update_ram)

    def update_ram(self):
        mem = psutil.virtual_memory()
        self.ram_label.config(text=f"RAM Usage: {mem.percent}% ({mem.used // (1024 ** 2)}MB / {mem.total // (1024 ** 2)}MB)")
        self.ram_progress["value"] = mem.percent
        self.after(1000, self.update_ram)

    def init_fan_tab(self):
        self.fan_label = ttk.Label(self.fan_tab, text="", font=("Segoe UI", 14))
        self.fan_label.pack(pady=10)
        self.after(2000, self.update_fan)

    def update_fan(self):
        try:
            fans = psutil.sensors_fans()
            if not fans:
                self.fan_label.config(text="⚠️ No fan data available.")
            else:
                fan_text = ""
                for name, entries in fans.items():
                    for entry in entries:
                        fan_text += f"{name} - {entry.label or 'Fan'}: {entry.current} RPM\n"
                self.fan_label.config(text=fan_text.strip())
        except Exception as e:
            self.fan_label.config(text=f"Error: {e}")
        self.after(5000, self.update_fan)

if __name__ == "__main__":
    app = SystemMonitorApp()
    app.mainloop()

