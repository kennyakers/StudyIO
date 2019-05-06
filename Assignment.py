import numpy as np


class Assignment:
    subject = None
    days_till_due = None
    time_to_complete = None
    difficulty = None
    priority = None

    def __init__(self, subject, days, time, diff, priority):
        self.subject = subject
        self.days_till_due = days
        self.time_to_complete = time
        self.difficulty = diff
        self.priority = priority

    def __str__(self):
        return str(self.subject) + ", " + str(self.days_till_due) + ", " + str(self.time_to_complete) + ", " + str(
            self.difficulty) + ", " + str(self.priority)

    def get_array(self):
        return np.array([self.subject, self.days_till_due, self.time_to_complete, self.difficulty])
