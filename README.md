# CPU Scheduling Simulator

> Developed By: Akshath Arya 

A graphical CPU scheduling simulator built with **Tkinter** to demonstrate the following CPU scheduling algorithms:

- **FCFS** (First-Come, First-Served)  
- **SJF** (Shortest Job First)  
- **SRTF** (Shortest Remaining Time First)  
- **Round Robin**

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

Clone the repository to your local machine:

```bash
git clone "https://github.com/ARYAAKSHATH/OS-Scheduling-Simulator-.git"
cd OS-Scheduling-Simulator-
````

### 2. Create and Activate Virtual Environment

#### Create the virtual environment:

```bash
python -m venv venv
```

#### Activate the virtual environment:

* **On Windows**:

  ```bash
  venv\Scripts\activate
  ```

* **On macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

---

## 📁 File Descriptions and Execution

### `sim_gui.py`

* **Description**: Implements a **Tkinter-based GUI** for:

  * Inputting process details
  * Selecting scheduling algorithms
  * Displaying simulation results (e.g., Gantt chart, metrics)

* **Run Command**:

  ```bash
  python sim_gui.py
  ```

---

### `os_sim.py`

* **Description**: Contains the **core logic** for CPU scheduling algorithms:

  * FCFS
  * SJF
  * SRTF
  * Round Robin

* **Note**: This file is **not executed directly**; it is imported by `sim_gui.py`.
