# cpu_scheduler.py
# Classes for CPU Scheduling Simulator to be used with Tkinter GUI

import copy

class Process:
    def __init__(self, process_id, arrival_time, burst_time):
        self.process_id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.completed_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

class CPUScheduler:
    def __init__(self):
        self.process_list = []
        self.completed_list = []

    def add_process(self, process_id, arrival_time, burst_time):
        # Create a new process and add to the list
        if process_id and arrival_time >= 0 and burst_time > 0:
            process = Process(process_id, arrival_time, burst_time)
            self.process_list.append(process)
            return True
        return False

    def clear_results(self):
        # Clear completed list for new calculation
        self.completed_list = []

    def fcfs(self):
        # First Come First Served algorithm
        self.clear_results()
        time = 0
        queue = []

        while self.process_list or queue:
            # Add arrived processes to queue
            self._add_to_queue(time, queue)
            
            # If queue is empty, increment time
            while not queue and self.process_list:
                time += 1
                self._add_to_queue(time, queue)

            # Process the first in queue
            process = queue.pop(0)
            for _ in range(process.burst_time):
                time += 1
                self._add_to_queue(time, queue)
            
            # Calculate times
            process.completed_time = time
            process.turnaround_time = process.completed_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            self.completed_list.append(process)

        return self._calculate_metrics()

    def sjf(self):
        # Shortest Job First algorithm (non-preemptive)
        self.clear_results()
        time = 0
        queue = []

        while self.process_list or queue:
            self._add_to_queue(time, queue)
            
            while not queue and self.process_list:
                time += 1
                self._add_to_queue(time, queue)

            # Select process with shortest burst time
            process = self._select_shortest_job(queue)
            for _ in range(process.burst_time):
                time += 1
                self._add_to_queue(time, queue)

            # Calculate times
            process.completed_time = time
            process.turnaround_time = process.completed_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
            self.completed_list.append(process)

        return self._calculate_metrics()

    def srtf(self):
        # Shortest Remaining Time First algorithm (preemptive)
        self.clear_results()
        time = 0
        queue = []
        original_processes = copy.deepcopy(self.process_list)

        while self.process_list or queue:
            self._add_to_queue(time, queue)
            
            while not queue and self.process_list:
                time += 1
                self._add_to_queue(time, queue)

            # Select process with shortest remaining time
            queue.sort(key=lambda x: x.burst_time)
            process = queue[0]

            if process.burst_time == 1:
                queue.pop(0)
                process.completed_time = time + 1
                self.completed_list.append(process)
            else:
                process.burst_time -= 1

            time += 1
            self._add_to_queue(time, queue)

        # Restore original burst times and calculate metrics
        for p_table in original_processes:
            for p_comp in self.completed_list:
                if p_table.process_id == p_comp.process_id:
                    p_comp.burst_time = p_table.burst_time
                    p_comp.turnaround_time = p_comp.completed_time - p_comp.arrival_time
                    p_comp.waiting_time = p_comp.turnaround_time - p_comp.burst_time

        return self._calculate_metrics()

    def round_robin(self, time_quantum):
        # Round Robin algorithm
        if not time_quantum or time_quantum <= 0:
            return None

        self.clear_results()
        time = 0
        queue = []
        original_processes = copy.deepcopy(self.process_list)

        while self.process_list or queue:
            self._add_to_queue(time, queue)
            
            while not queue and self.process_list:
                time += 1
                self._add_to_queue(time, queue)

            process = queue[0]
            if process.burst_time <= time_quantum:
                queue.pop(0)
                process.completed_time = time + process.burst_time
                for _ in range(process.burst_time):
                    time += 1
                    self._add_to_queue(time, queue)
                self.completed_list.append(process)
            else:
                process.burst_time -= time_quantum
                for _ in range(time_quantum):
                    time += 1
                    self._add_to_queue(time, queue)

        # Restore original burst times and calculate metrics
        for p_table in original_processes:
            for p_comp in self.completed_list:
                if p_table.process_id == p_comp.process_id:
                    p_comp.burst_time = p_table.burst_time
                    p_comp.turnaround_time = p_comp.completed_time - p_comp.arrival_time
                    p_comp.waiting_time = p_comp.turnaround_time - p_comp.burst_time

        return self._calculate_metrics()

    def _add_to_queue(self, time, queue):
        # Helper method to add arrived processes to queue
        i = 0
        while i < len(self.process_list):
            if self.process_list[i].arrival_time <= time:
                queue.append(self.process_list.pop(i))
            else:
                i += 1

    def _select_shortest_job(self, queue):
        # Helper method to select process with shortest burst time
        if queue:
            queue.sort(key=lambda x: x.burst_time)
            return queue.pop(0)
        return None

    def _calculate_metrics(self):
        # Calculate average turnaround time, waiting time, and throughput
        if not self.completed_list:
            return 0, 0, 0

        avg_turnaround_time = 0
        avg_waiting_time = 0
        max_completed_time = 0

        for process in self.completed_list:
            if process.completed_time > max_completed_time:
                max_completed_time = process.completed_time
            avg_turnaround_time += process.turnaround_time
            avg_waiting_time += process.waiting_time

        avg_turnaround_time /= len(self.completed_list)
        avg_waiting_time /= len(self.completed_list)
        throughput = len(self.completed_list) / max_completed_time if max_completed_time > 0 else 0

        return avg_turnaround_time, avg_waiting_time, throughput

    def get_process_list(self):
        # Return the current process list
        return self.process_list

    def get_completed_list(self):
        # Return the completed process list
        return self.completed_list