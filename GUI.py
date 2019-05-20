import tkinter as tk
from tkinter import messagebox, StringVar, END, HORIZONTAL
from tkinter.filedialog import askopenfilename

import pandas
from PIL import ImageTk, Image

from Assignment import Assignment
from DragNDrop import Tester, Icon


class GUI:
    assignment_file = None
    assignment_list = []

    window = None
    datafile_button = None
    add_button = None
    done_button = None
    subject_field = None
    days_till_due_field = None
    time_to_complete_field = None
    difficulty_field = None
    description_field = None
    label = None
    background_image = None
    background_label = None

    var = None

    def __init__(self, name):
        self.window = tk.Tk()
        self.window.title(name)
        self.window.geometry("400x250")
        self.var = StringVar(self.window)
        self.var.set("Subject")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def data_setup(self):
        self.background_image = ImageTk.PhotoImage(Image.open('./bg.jpg').resize((400, 200), Image.ANTIALIAS))
        self.background_label = tk.Label(self.window, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.label = tk.Label(self.window, text="Please select the assignment history data file.", anchor="n")
        self.datafile_button = tk.Button(self.window, text="Import assignment data", command=self.datafile_dialogue)
        self.label.grid(row=0, column=0, sticky="n")
        self.datafile_button.grid(row=1, column=0, sticky="n")
        self.background_label.grid()
        self.window.mainloop()

    def next_screen(self):
        self.clear_screen()
        print("Clearing")
        self.window.quit()

    def assignment_setup(self, subject_list: pandas.DataFrame):
        self.window.geometry("550x125")
        self.subject_field = tk.OptionMenu(self.window, self.var, *subject_list)

        self.days_till_due_field = tk.Scale(self.window, label="Days till due", orient=HORIZONTAL, from_=1, to=7)
        self.time_to_complete_field = tk.Entry(self.window, width=4)
        self.time_to_complete_field.insert(index=END, string="Time")
        self.difficulty_field = tk.Scale(self.window, label="Difficulty", orient=HORIZONTAL, from_=1, to=10)
        self.description_field = tk.Entry(self.window, width=20)
        self.description_field.insert(index=END, string="Description")

        self.add_button = tk.Button(self.window, text="Add", command=self.intake_assignment)
        self.done_button = tk.Button(self.window, text="Done", command=self.done)

        self.subject_field.grid(row=0, column=0)
        self.days_till_due_field.grid(row=0, column=1)
        self.time_to_complete_field.grid(row=0, column=2)
        self.difficulty_field.grid(row=0, column=3)
        self.description_field.grid(row=1, column=1)
        self.add_button.grid(row=0, column=4)
        self.done_button.grid(row=2, column=4)
        self.window.mainloop()

    def intake_assignment(self):
        # Add assignment to list
        # Need to check for illegal or missing values
        self.assignment_list.append(Assignment(subject=self.var.get(), days=self.days_till_due_field.get(),
                                               time=self.time_to_complete_field.get(), diff=self.difficulty_field.get(),
                                               priority=None, descrip=self.description_field.get()))
        # Reset dialogues
        self.time_to_complete_field.delete(0, 'end')
        self.description_field.delete(0, 'end')
        self.days_till_due_field.set(1)
        self.difficulty_field.set(1)
        self.description_field.insert(index=END, string="Description")
        self.time_to_complete_field.insert(index=END, string="Time")
        self.var.set("Subject")

    def display_assignments(self):
        index = 1
        x_pos = 0
        y_pos = 0

        t1 = Tester(self.window, width=self.window.winfo_width(), height=self.window.winfo_height())
        t1.top.geometry("+1+60")

        for assignment in self.assignment_list:
            icon = Icon(name="Assignment #" + str(index), subject=assignment.subject, priority=assignment.priority,
                        description=assignment.description)
            icon.attach(canvas=t1.canvas, x=x_pos, y=y_pos)
            tk.Tk.update(self.window)  # Need to call this in order to get label height and width
            # print(icon.label.winfo_width())
            x_pos += icon.label.winfo_width()
            if x_pos > self.window.winfo_width():
                x_pos = 0
                y_pos += icon.label.winfo_height()
            if y_pos > self.window.winfo_height():
                self.window.geometry("550x" + str(self.window.winfo_height() + icon.label.winfo_height()))
            index += 1
        self.window.withdraw()
        self.window.mainloop()

    def datafile_dialogue(self):
        self.assignment_file = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
        self.next_screen()

    def done(self):
        self.next_screen()
        print("Assignments entered:\n", *self.assignment_list, sep='\n')

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()
            exit(1)

    def clear_screen(self):
        try:
            self.label.grid_forget()
            self.datafile_button.grid_forget()
            self.background_label.grid_forget()
            self.subject_field.grid_forget()
            self.days_till_due_field.grid_forget()
            self.time_to_complete_field.grid_forget()
            self.difficulty_field.grid_forget()
            self.add_button.grid_forget()
            self.done_button.grid_forget()
        except AttributeError:
            pass
