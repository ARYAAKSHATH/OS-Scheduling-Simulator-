# cpu_scheduler_gui.py
# Tkinter GUI for CPU Scheduling Simulator

import tkinter as tk
from tkinter import ttk, messagebox
from cpu_scheduler import Process, CPUScheduler

class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.scheduler = CPUScheduler()
        self.setup_gui()

    def setup_gui(self):
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input frame for process details
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Add Process", padding="10")
        self.input_frame.grid(row=0, column=0, pady=5, sticky=tk.W)

        # Process ID
        ttk.Label(self.input_frame, text="Process ID:").grid(row=0, column=0, padx=5)
        self.process_id = ttk.Entry(self.input_frame, width=10)
        self.process_id.grid(row=0, column=1, padx=5)

        # Arrival Time
        ttk.Label(self.input_frame, text="Arrival Time:").grid(row=0, column=2, padx=5)
        self.arrival_time = ttk.Entry(self.input_frame, width=10)
        self.arrival_time.grid(row=0, column=3, padx=5)

        # Burst Time
        ttk.Label(self.input_frame, text="Burst Time:").grid(row=0, column=4, padx=5)
        self.burst_time = ttk.Entry(self.input_frame, width=10)
        self.burst_time.grid(row=0, column=5, padx=5)

        # Add Process Button
        ttk.Button(self.input_frame, text="Add Process", command=self.add_process).grid(row=0, column=6, padx=5)

        # Algorithm selection frame
        self.algo_frame = ttk.LabelFrame(self.main_frame, text="Select Algorithm", padding="10")
        self.algo_frame.grid(row=1, column=0, pady=5, sticky=tk.W)

        # Algorithm dropdown
        self.algorithm = tk.StringVar()
        algorithms = ["FCFS", "SJF", "SRTF", "Round Robin"]
        self.algorithm.set(algorithms[0])
        self.algo_dropdown = ttk.Combobox(self.algo_frame, textvariable=self.algorithm, values=algorithms, state="readonly")
        self.algo_dropdown.grid(row=0, column=0, padx=5)
        self.algo_dropdown.bind("<<ComboboxSelected>>", self.toggle_time_quantum)

        # Time Quantum (hidden by default)
        self.time_quantum_frame = ttk.Frame(self.algo_frame)
        self.time_quantum_frame.grid(row=0, column=1, padx=5)
        ttk.Label(self.time_quantum_frame, text="Time Quantum:").grid(row=0, column=0, padx=5)
        self.time_quantum = ttk.Entry(self.time_quantum_frame, width=10)
        self.time_quantum.grid(row=0, column=1, padx=5)
        self.time_quantum_frame.grid_remove()  # Hide initially

        # Calculate Button
        ttk.Button(self.algo_frame, text="Calculate", command=self.calculate).grid(row=0, column=2, padx=5)

        # Process List Table
        self.process_frame = ttk.LabelFrame(self.main_frame, text="Process List", padding="10")
        self.process_frame.grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))

        self.process_tree = ttk.Treeview(self.process_frame, columns=("ID", "Arrival", "Burst"), show="headings")
        self.process_tree.heading("ID", text="Process ID")
        self.process_tree.heading("Arrival", text="Arrival Time")
        self.process_tree.heading("Burst", text="Burst Time")
        self.process_tree.grid(row=0, column=0)

        # Results Table
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding="10")
        self.results_frame.grid(row=3, column=0, pady=5, sticky=(tk.W, tk.E))

        self.results_tree = ttk.Treeview(self.results_frame, columns=("ID", "Arrival", "Burst", "Completed", "Waiting", "Turnaround"), show="headings")
        self.results_tree.heading("ID", text="Process ID")
        self.results_tree.heading("Arrival", text="Arrival Time")
        self.results_tree.heading("Burst", text="Burst Time")
        self.results_tree.heading("Completed", text="Completed Time")
        self.results_tree.heading("Waiting", text="Waiting Time")
        self.results_tree.heading("Turnaround", text="Turnaround Time")
        self.results_tree.grid(row=0, column=0)

        # Metrics Frame
        self.metrics_frame = ttk.LabelFrame(self.main_frame, text="Metrics", padding="10")
        self.metrics_frame.grid(row=4, column=0, pady=5, sticky=tk.W)

        ttk.Label(self.metrics_frame, text="Avg Turnaround Time:").grid(row=0, column=0, padx=5)
        self.avg_turnaround = ttk.Entry(self.metrics_frame, width=10, state="readonly")
        self.avg_turnaround.grid(row=0, column=1, padx=5)

        ttk.Label(self.metrics_frame, text="Avg Waiting Time:").grid(row=0, column=2, padx=5)
        self.avg_waiting = ttk.Entry(self.metrics_frame, width=10, state="readonly")
        self.avg_waiting.grid(row=0, column=3, padx=5)

        ttk.Label(self.metrics_frame, text="Throughput:").grid(row=0, column=4, padx=5)
        self.throughput = ttk.Entry(self.metrics_frame, width=10, state="readonly")
        self.throughput.grid(row=0, column=5, padx=5)

    def toggle_time_quantum(self, event=None):
        # Show/hide time quantum field based on algorithm
        if self.algorithm.get() == "Round Robin":
            self.time_quantum_frame.grid()
        else:
            self.time_quantum_frame.grid_remove()

    def add_process(self):
        # Add process to scheduler and update process table
        try:
            process_id = int(self.process_id.get())
            arrival_time = int(self.arrival_time.get())
            burst_time = int(self.burst_time.get())

            if self.scheduler.add_process(process_id, arrival_time, burst_time):
                self.process_tree.insert("", "end", values=(process_id, arrival_time, burst_time))
                self.process_id.delete(0, tk.END)
                self.arrival_time.delete(0, tk.END)
                self.burst_time.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please enter valid process details")
        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values")

    def calculate(self):
        # Run selected algorithm and display results
        if not self.scheduler.get_process_list():
            messagebox.showerror("Error", "Please add some processes")
            return

        self.results_tree.delete(*self.results_tree.get_children())  # Clear previous results
        algo = self.algorithm.get()

        if algo == "FCFS":
            metrics = self.scheduler.fcfs()
        elif algo == "SJF":
            metrics = self.scheduler.sjf()
        elif algo == "SRTF":
            metrics = self.scheduler.srtf()
        elif algo == "Round Robin":
            try:
                time_quantum = int(self.time_quantum.get())
                metrics = self.scheduler.round_robin(time_quantum)
                if metrics is None:
                    messagebox.showerror("Error", "Please enter a valid time quantum")
                    return
            except ValueError:
                messagebox.showerror("Error", "Please enter a numeric time quantum")
                return

        # Display results in table
        for process in self.scheduler.get_completed_list():
            self.results_tree.insert("", "end", values=(
                process.process_id,
                process.arrival_time,
                process.burst_time,
                process.completed_time,
                process.waiting_time,
                process.turnaround_time
            ))

        # Display metrics
        avg_turnaround, avg_waiting, throughput = metrics
        self.avg_turnaround.config(state="normal")
        self.avg_waiting.config(state="normal")
        self.throughput.config(state="normal")
        self.avg_turnaround.delete(0, tk.END)
        self.avg_waiting.delete(0, tk.END)
        self.throughput.delete(0, tk.END)
        self.avg_turnaround.insert(0, f"{avg_turnaround:.2f}")
        self.avg_waiting.insert(0, f"{avg_waiting:.2f}")
        self.throughput.insert(0, f"{throughput:.2f}")
        self.avg_turnaround.config(state="readonly")
        self.avg_waiting.config(state="readonly")
        self.throughput.config(state="readonly")

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()