import tkinter as tk
from tkinter import messagebox, simpledialog
import os

FILE_NAME = "tasks.txt"

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.root.configure(bg="#ffe6f2")  # Light pink background

        self.tasks = self.load_tasks()

        self.frame = tk.Frame(root, bg="#ffe6f2")
        self.frame.pack(padx=10, pady=10)

        self.listbox = tk.Listbox(
            self.frame,
            height=15,
            width=50,
            selectmode=tk.SINGLE,
            bg="#ffccdd",         # Soft pink background
            fg="#660033",         # Dark pink text color
            font=("Helvetica", 12),
            highlightthickness=2,
            highlightbackground="#ff66aa",  # Pink border when unfocused
            selectbackground="#ff3399",      # Bright pink for selected background (visible)
            selectforeground="#ffffff"       # White text when selected for readability
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.listbox.bind('<Double-1>', self.edit_task)
        self.listbox.bind('<Button-3>', self.show_context_menu)
        self.listbox.bind('<Key-Delete>', lambda e: self.remove_task())
        self.listbox.bind('<Return>', lambda e: self.edit_task())
        self.listbox.focus_set()

        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.entry = tk.Entry(
            root,
            width=52,
            font=("Helvetica", 12),
            bg="#ffe6f2",
            fg="#660033",
            insertbackground="#660033",
            relief=tk.GROOVE,
            highlightthickness=2,
            highlightbackground="#ff66aa"
        )
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', lambda event: self.add_task())

        self.add_button = tk.Button(
            root,
            text="Add Task",
            width=48,
            command=self.add_task,
            bg="#ff66aa",
            fg="white",
            activebackground="#ff3388",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT
        )
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(
            root,
            text="Remove Selected Task",
            width=48,
            command=self.remove_task,
            bg="#ff66aa",
            fg="white",
            activebackground="#ff3388",
            font=("Helvetica", 12, "bold"),
            relief=tk.FLAT
        )
        self.remove_button.pack(pady=5)

        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#ffccdd", fg="#660033", font=("Helvetica", 12))
        self.context_menu.add_command(label="Edit Task", command=self.edit_task)
        self.context_menu.add_command(label="Remove Task", command=self.remove_task)

        self.populate_listbox()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_tasks(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                tasks = file.read().splitlines()
            return tasks
        return []

    def save_tasks(self):
        with open(FILE_NAME, "w") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)

    def add_task(self):
        task = self.entry.get().strip()
        if not task:
            messagebox.showwarning("Input Error", "Task cannot be empty.", parent=self.root)
            return
        self.tasks.append(task)
        self.populate_listbox()
        self.entry.delete(0, tk.END)

    def remove_task(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a task to remove.", parent=self.root)
            return
        selected_index = selected_indices[0]
        removed_task = self.tasks.pop(selected_index)
        self.populate_listbox()
        messagebox.showinfo("Task Removed", f"Removed task: {removed_task}", parent=self.root)

    def edit_task(self, event=None):
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a task to edit.", parent=self.root)
            return
        selected_index = selected_indices[0]
        current_task = self.tasks[selected_index]
        new_task = simpledialog.askstring("Edit Task", "Edit the selected task:", initialvalue=current_task, parent=self.root)
        if new_task:
            self.tasks[selected_index] = new_task.strip()
            self.populate_listbox()

    def show_context_menu(self, event):
        try:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(self.listbox.nearest(event.y))
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def on_closing(self):
        self.save_tasks()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
