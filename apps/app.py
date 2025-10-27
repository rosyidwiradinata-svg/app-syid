import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from collections import deque
import random

# ================= Matrix Kalem =================
class MatrixBackground:
    def __init__(self, canvas, width, height):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.chars = "01"
        self.font_size = 14
        self.columns = int(width / self.font_size)
        self.drops = [random.randint(0, height // self.font_size) for _ in range(self.columns)]
        self.intensity = [random.randint(100, 255) for _ in range(self.columns)]
        self.canvas.configure(bg="black")
        self.animate()

    def animate(self):
        self.canvas.delete("matrix")
        for i in range(self.columns):
            char = random.choice(self.chars)
            x = i * self.font_size
            y = self.drops[i] * self.font_size
            g = self.intensity[i]
            self.canvas.create_text(x, y, text=char, fill=f"#00{g:02x}00",
                                    font=("Consolas", self.font_size, "bold"),
                                    tag="matrix")
            if random.random() < 0.02:
                self.drops[i] = 0
                self.intensity[i] = random.randint(100, 255)
            else:
                self.drops[i] += 1
                self.intensity[i] = max(50, self.intensity[i]-5)
                if self.drops[i] * self.font_size > self.height:
                    self.drops[i] = 0
                    self.intensity[i] = random.randint(100, 255)
        self.canvas.after(150, self.animate)  # Lebih lambat, ringan

# ================= CPU Scheduler =================
class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("950x700")
        self.root.configure(bg="black")

        # Canvas Matrix di belakang
        self.canvas = tk.Canvas(root, width=950, height=700, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.matrix = MatrixBackground(self.canvas, 950, 700)

        # Frame scheduler di tengah (semi-transparent)
        self.frame_main = tk.Frame(self.canvas, bg="#111111")
        self.frame_main.place(relx=0.5, rely=0.5, anchor="center")

        # Style modern
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#1e293b",
                        foreground="white",
                        fieldbackground="#1e293b",
                        rowheight=30,
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        background="#334155",
                        foreground="white",
                        font=("Segoe UI", 11, "bold"))

        # Frame input
        self.frame_input = tk.Frame(self.frame_main, bg="#111111", pady=10)
        self.frame_input.pack(fill="x")

        tk.Label(self.frame_input, text="Jumlah Proses:", bg="#111111", fg="white").grid(row=0, column=0, padx=5)
        self.num_entry = tk.Entry(self.frame_input, width=5)
        self.num_entry.grid(row=0, column=1, padx=5)
        self.num_entry.insert(0, "3")

        tk.Label(self.frame_input, text="Algoritma:", bg="#111111", fg="white").grid(row=0, column=2, padx=5)
        self.algo_choice = ttk.Combobox(self.frame_input,
                                        values=["FIFO", "SJF", "SRTF", "Round Robin"],
                                        state="readonly", width=20)
        self.algo_choice.grid(row=0, column=3, padx=5)
        self.algo_choice.current(0)

        self.q_label = tk.Label(self.frame_input, text="Quantum (RR):", bg="#111111", fg="white")
        self.q_label.grid(row=0, column=4, padx=5)
        self.q_entry = tk.Entry(self.frame_input, width=5)
        self.q_entry.grid(row=0, column=5, padx=5)
        self.q_entry.insert(0, "2")

        tk.Button(self.frame_input, text="Buat Tabel", command=self.make_table,
                  bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold")).grid(row=0, column=6, padx=5)

        # Frame tabel input
        self.table_frame = tk.Frame(self.frame_main, bg="#111111", pady=10)
        self.table_frame.pack(fill="x")

        # Frame tombol
        self.btn_frame = tk.Frame(self.frame_main, bg="#111111", pady=10)
        self.btn_frame.pack(fill="x")

        self.btn_run = tk.Button(self.btn_frame, text="Hitung & Simulasi",
                                 command=self.run_simulation, state="disabled",
                                 bg="#16a34a", fg="white", font=("Segoe UI", 10, "bold"))
        self.btn_run.pack()

        # Frame hasil
        self.result_frame = tk.Frame(self.frame_main, bg="#111111", pady=10)
        self.result_frame.pack(fill="both", expand=True)

        self.gantt_frame = tk.Frame(self.result_frame, bg="#111111")
        self.gantt_frame.pack(fill="x", pady=10)

        self.progress = ttk.Progressbar(self.result_frame, length=750, mode="determinate")
        self.progress.pack(pady=5)

        self.status_label = tk.Label(self.result_frame, text="", font=("Segoe UI", 12, "bold"),
                                     bg="#111111", fg="white")
        self.status_label.pack(pady=5)

        # Tabel hasil
        self.tree = ttk.Treeview(self.result_frame,
                                 columns=("Proses", "Masuk", "CPU", "Selesai", "TAT", "WT"),
                                 show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)
        self.tree.pack(fill="x", pady=10)

        self.avg_label = tk.Label(self.result_frame, text="", bg="#111111", fg="white",
                                  font=("Segoe UI", 11, "bold"))
        self.avg_label.pack(pady=5)

        self.entries = []

    # ================= Table Input =================
    def make_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries.clear()
        num = int(self.num_entry.get())
        tk.Label(self.table_frame, text="Proses", bg="#111111", fg="white").grid(row=0, column=0, padx=5)
        tk.Label(self.table_frame, text="Arrival Time", bg="#111111", fg="white").grid(row=0, column=1, padx=5)
        tk.Label(self.table_frame, text="CPU Time", bg="#111111", fg="white").grid(row=0, column=2, padx=5)
        for i in range(num):
            tk.Label(self.table_frame, text=f"P{i+1}", bg="#111111", fg="white").grid(row=i+1, column=0, padx=5)
            at = tk.Entry(self.table_frame, width=10)
            bt = tk.Entry(self.table_frame, width=10)
            at.insert(0, "0")
            bt.insert(0, "0")
            at.grid(row=i+1, column=1, padx=5)
            bt.grid(row=i+1, column=2, padx=5)
            self.entries.append((at, bt))
        self.btn_run["state"] = "normal"

    # ================= Run Simulation =================
    def run_simulation(self):
        processes = []
        for i, (at, bt) in enumerate(self.entries):
            try:
                arrival = int(at.get())
                burst = int(bt.get())
            except:
                arrival, burst = 0, 0
            processes.append([f"P{i+1}", arrival, burst])

        algo = self.algo_choice.get()
        if algo == "FIFO":
            gantt, results = self.fcfs(processes)
        elif algo == "SJF":
            gantt, results = self.sjf(processes)
        elif algo == "SRTF":
            gantt, results = self.srtf(processes)
        elif algo == "Round Robin":
            q = int(self.q_entry.get())
            gantt, results = self.rr(processes, q)
        else:
            return

        # Update tabel hasil
        for row in self.tree.get_children():
            self.tree.delete(row)
        total_tat, total_wt = 0, 0
        for r in results:
            self.tree.insert("", "end", values=r)
            total_tat += r[4]
            total_wt += r[5]
        n = len(results)
        self.avg_label.config(text=f"Average TAT = {total_tat/n:.2f} | Average WT = {total_wt/n:.2f}")

        # Jalankan animasi Gantt
        threading.Thread(target=self.animate_gantt, args=(gantt,)).start()

    # ================= Algoritma =================
    def fcfs(self, processes):
        processes.sort(key=lambda x: x[1])
        time_now, gantt, results = 0, [], []
        for p, at, bt in processes:
            if time_now < at: time_now = at
            start, finish = time_now, time_now + bt
            tat, wt = finish - at, finish - at - bt
            gantt.append((p, start, finish, bt))
            results.append((p, at, bt, finish, tat, wt))
            time_now = finish
        return gantt, results

    def sjf(self, processes):
        n = len(processes)
        time_now, done, gantt, results = 0, 0, [], []
        completed = []
        while done < n:
            available = [p for p in processes if p[1] <= time_now and p not in completed]
            if not available:
                time_now += 1
                continue
            p = min(available, key=lambda x: x[2])
            start, finish = time_now, time_now + p[2]
            tat, wt = finish - p[1], finish - p[1] - p[2]
            gantt.append((p[0], start, finish, p[2]))
            results.append((p[0], p[1], p[2], finish, tat, wt))
            completed.append(p)
            time_now = finish
            done += 1
        return gantt, results

    def srtf(self, processes):
        n = len(processes)
        time_now, done, gantt, results = 0, 0, [], []
        remaining = {p[0]: p[2] for p in processes}
        while done < n:
            available = [p for p in processes if p[1] <= time_now and remaining[p[0]] > 0]
            if not available:
                time_now += 1
                continue
            p = min(available, key=lambda x: remaining[x[0]])
            remaining[p[0]] -= 1
            gantt.append((p[0], time_now, time_now+1, 1))
            time_now += 1
            if remaining[p[0]] == 0:
                finish = time_now
                tat, wt = finish - p[1], finish - p[1] - p[2]
                results.append((p[0], p[1], p[2], finish, tat, wt))
                done += 1
        return gantt, results

    def rr(self, processes, q):
        n = len(processes)
        time_now, gantt, results = 0, [], []
        remaining = {p[0]: p[2] for p in processes}
        queue = deque()
        completed = []
        processes.sort(key=lambda x: x[1])
        i = 0
        while len(completed) < n:
            while i < n and processes[i][1] <= time_now:
                queue.append(processes[i])
                i += 1
            if not queue:
                time_now = processes[i][1]
                continue
            p = queue.popleft()
            bt = min(q, remaining[p[0]])
            gantt.append((p[0], time_now, time_now+bt, bt))
            time_now += bt
            remaining[p[0]] -= bt
            while i < n and processes[i][1] <= time_now:
                queue.append(processes[i])
                i += 1
            if remaining[p[0]] > 0:
                queue.append(p)
            else:
                finish = time_now
                tat, wt = finish - p[1], finish - p[1] - p[2]
                results.append((p[0], p[1], p[2], finish, tat, wt))
                completed.append(p)
        return gantt, results

    # ================= Animasi Gantt =================
    def animate_gantt(self, gantt):
        for widget in self.gantt_frame.winfo_children():
            widget.destroy()
        self.status_label.config(text="Memulai simulasi...")
        self.progress["value"] = 0

        for p, start, finish, bt in gantt:
            lbl = tk.Label(self.gantt_frame, text=f"{p}\n{start}-{finish}", width=12, height=4,
                           bg="#334155", fg="white", relief="raised", font=("Segoe UI", 10, "bold"))
            lbl.pack(side="left", padx=3, pady=3)

            self.status_label.config(text=f"Menjalankan {p} ...")
            self.progress["value"] = 0
            self.progress["maximum"] = bt * 20

            for i in range(bt * 20):
                time.sleep(0.05)
                self.progress["value"] = i + 1
                r = int(50 + (i / (bt*20)) * 100)
                g = int(80 + (i / (bt*20)) * 150)
                b = 85
                lbl.config(bg=f"#{r:02x}{g:02x}{b:02x}")
                self.root.update_idletasks()

        self.status_label.config(text="Simulasi selesai ✅")

# ================= Jalankan App =================
if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerApp(root)
    root.mainloop()
