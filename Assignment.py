import numpy as np


class Assignment:
    subject = None
    days_till_due = None
    time_to_complete = None
    difficulty = None
    priority = None
    description = None

    def __init__(self, subject, days, time, diff, priority, descrip):
        self.subject = subject
        self.days_till_due = days
        self.time_to_complete = time
        self.difficulty = diff
        self.priority = priority
        self.description = descrip

    def __str__(self):
        return "Subject: " + str(self.subject) + "\nDays Until Due: " + str(
            self.days_till_due) + "\nTime to Complete: " + str(
            self.time_to_complete) + "\nDifficulty: " + str(
            self.difficulty) + "\nPriority: " + str(self.priority) + "\nDescription: " + self.description + "\n"

    def get_array(self):
        return np.array([self.subject, self.days_till_due, self.time_to_complete, self.difficulty])
