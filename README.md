# 🖥️ System Health Monitor

A real-time desktop monitoring tool built with Python's Tkinter GUI library, Matplotlib, and psutil. This application visualizes CPU usage dynamically, displays RAM usage, and attempts to retrieve fan RPM data—all packed in a sleek tabbed interface.

## 📌 Features

- **CPU Usage Graph**: Real-time line graph with usage updates every second.
- **RAM Monitor**: Live RAM consumption with a progress bar and formatted memory stats.
- **Fan RPM**: Displays current fan speeds using `psutil.sensors_fans()` (if available).
- **Tabbed UI**: Organized with three tabs—CPU, RAM, and FAN.

## 🛠️ Technologies Used

- `tkinter` for GUI layout
- `psutil` for system monitoring data
- `matplotlib` for dynamic graphing
- `matplotlib.animation` for live updates
- `ttk` for styled widgets
- `deque` for efficient data handling

## 📦 Installation & Setup

1. **Install dependencies**:
   ```bash
   pip install psutil matplotlib
