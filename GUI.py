import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename

import pandas

from Assignment import Assignment


class GUI:
    assignment_file = None
    assignment_list = []

    window = None
    datafile_button = None
    add_button = None
    next_button = None
    subject_field = None
    days_till_due_field = None
    time_to_complete_field = None
    difficulty_field = None
    label = None

    var = None
    screen_number = 1

    def __init__(self, name):
        self.window = tk.Tk()
        self.window.title(name)
        self.window.geometry("400x100")
        self.var = StringVar(self.window)
        self.var.set("Subject")

    def data_setup(self):
        self.label = tk.Label(self.window, text="Please select the assignment history data file.", anchor="n")
        self.datafile_button = tk.Button(self.window, text="Import assignment data", command=self.datafile_dialogue)
        self.next_button = tk.Button(self.window, text="Next", command=self.next_screen, anchor="se")
        self.label.grid(row=0, column=0, sticky="n")
        self.datafile_button.grid(row=1, column=0, sticky="n")
        self.next_button.grid(row=2, column=0)
        self.window.mainloop()

    def next_screen(self):
        if self.screen_number == 1:
            self.label.grid_forget()
            self.datafile_button.grid_forget()
            self.screen_number = 2
            self.window.quit()

    def assignment_setup(self, subject_list: pandas.DataFrame):
        self.subject_field = tk.OptionMenu(self.window, self.var, *subject_list)

        self.days_till_due_field = tk.Scale(self.window, orient=HORIZONTAL, from_=1, to=7)
        self.time_to_complete_field = tk.Entry(self.window, width=3)
        self.difficulty_field = tk.Scale(self.window, orient=HORIZONTAL, from_=1, to=10)

        self.add_button = tk.Button(self.window, text="Add", command=self.intake_assignment)

        self.subject_field.grid(row=0, column=0)
        self.days_till_due_field.grid(row=0, column=1)
        self.time_to_complete_field.grid(row=0, column=2)
        self.difficulty_field.grid(row=0, column=3)
        self.add_button.grid(row=0, column=4)
        self.window.mainloop()

    def intake_assignment(self):
        # Add assignment to list
        # Need to check for illegal or missing values
        self.assignment_list.append(Assignment(self.var.get(), self.days_till_due_field.get(),
                                               self.time_to_complete_field.get(), self.difficulty_field.get(),
                                               priority=None))
        # Reset dialogues
        self.time_to_complete_field.delete(0, 'end')
        self.days_till_due_field.set(1)
        self.difficulty_field.set(1)
        self.var.set("Subject")
        print(*self.assignment_list, sep='\n')

    def datafile_dialogue(self):
        self.assignment_file = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
