# importing necessary libraries
import sys

import numpy as np
import pandas
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC as SupportVectorMachine

debug = False
assignmentFile = None
errorPenalty = 1.75  # Accuracy caps out at 0.9924 after 1.68.
subject = 0
numSubjects = 7
daysTillDue = 0
timeToComplete = 0
difficulty = 0

if len(sys.argv) > 1:
    assignmentFile = ''.join([s for s in sys.argv if ".csv" in s])
    if any(arg == "-error" for arg in sys.argv):
        errorPenalty = float(sys.argv[sys.argv.index("-error") + 1])  # Get value after "-error"
        if errorPenalty <= 0.0:
            print("ERROR: Error penalty (" + str(errorPenalty) + ") must be greater than 0.")
            sys.exit()

    if any(arg == "-subject" for arg in sys.argv):
        subject = int(sys.argv[sys.argv.index("-subject") + 1])  # Get value after "-subject"
        if subject not in range(1, numSubjects):
            print("ERROR: Subject number must be between 1 and " + str(numSubjects))
            sys.exit()

    if any(arg == "-days-due" for arg in sys.argv):
        daysTillDue = int(sys.argv[sys.argv.index("-days-due") + 1])  # Get value after "-subject"
        if daysTillDue <= 0:
            print("ERROR: Subject number must be greater than 0")
            sys.exit()

    if any(arg == "-time" for arg in sys.argv):
        timeToComplete = int(sys.argv[sys.argv.index("-time") + 1])  # Get value after "-subject"
        if timeToComplete <= 0:
            print("ERROR: Time to complete must be greater than 0")
            sys.exit()

    if any(arg == "-difficulty" for arg in sys.argv):
        daysTillDue = int(sys.argv[sys.argv.index("-difficulty") + 1])  # Get value after "-subject"
        if difficulty <= 0:
            print("ERROR: Difficulty must be greater than 0")
            sys.exit()

    if any(arg == "-debug" for arg in sys.argv):
        print("File:", assignmentFile)
        print("Error penalty:", errorPenalty)
        print("Subject:", subject)
        print("Days till due:", daysTillDue)
        print("Time to complete:", timeToComplete)
        print("Difficulty:", difficulty)
        debug = True

dataframe_raw = pandas.read_csv(assignmentFile, header=0)
# Get all but the first row (which is all the column names).
dataset = dataframe_raw.iloc[1:].values
features = dataset[:, 0:4].astype(float)
labels = dataset[:, 4]  # Get answers
if debug:
    pandas.set_option('display.max_rows', 10)  # Only print first 5 and last 5 rows (10 rows total)
    print(dataframe_raw)

# dividing features, labels into train and test data
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, random_state=0)

# training a linear SVM classifier
svm_model = SupportVectorMachine(kernel='rbf', C=errorPenalty).fit(features_train, labels_train)
svm_predictions = svm_model.predict(features_test)

# using classifier to predict
'''
MIGHT WANT TO CONSIDER NOT HAVING THE USER INPUT A TIMETOCOMPLETE (BECAUSE THEY DON'T
KNOW THAT NUMBER BEFORE DOING THE ASSIGNMENT) AND INSTEAD USING THEIR AVERAGE TIMETOCOMPLETE
FOR THAT SUBJECT FROM PAST ASSIGNMENTS OR SAMPLING FROM THEIR DISTRIBUTIONS (BOX-MULLER)
'''
assignment = np.array([subject, daysTillDue, timeToComplete, difficulty])
assignment = assignment.reshape(1, -1)  # Need to do if it's a single sample

answer = svm_model.predict(assignment)
# model accuracy for X_test
accuracy = svm_model.score(features_test, labels_test)

# creating a confusion matrix
cm = confusion_matrix(labels_test, svm_predictions)
if debug:
    print("\n# Support Vectors:", svm_model.n_support_, "\n")
    print("Confusion Matrix:\n", cm, "\n")
    print("Accuracy:", accuracy)

print("Answer:", answer)
