import numpy as np
import pandas
from numpy import random, sqrt, log, sin, pi
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC as SupportVectorMachine

from GUI import GUI

debug = False
assignmentFile = None
errorPenalty = 1.75  # Accuracy caps out at 0.9924 after 1.68.
subject = 0
daysTillDue = 0
timeToComplete = 0
difficulty = 0

gui = GUI("StudyIO")
gui.data_setup()

'''
if len(sys.argv) > 1:
    if any(arg == "-help" for arg in sys.argv):
        print("Commands:")
        print("-error")
        print("-subject")
        print("-days-due")
        print("-time")
        print("-difficulty")
        print("-debug")
        # Need to finish

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
        difficulty = int(sys.argv[sys.argv.index("-difficulty") + 1])  # Get value after "-subject"
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
'''

dataframe_raw = pandas.read_csv(gui.assignment_file, header=0)
if debug:
    pandas.set_option('display.max_rows', 10)  # Only print first 5 and last 5 rows (10 rows total)
    print(dataframe_raw)

# Get all but the first row (which is all the column names).
dataset = dataframe_raw.iloc[1:].values

subject_list = pandas.unique(dataset[:, 0])
gui.assignment_setup(subject_list)  # pass in all subject names
for i, val in enumerate(dataset[:, 0]):
    dataset[i, 0], = np.where(val == subject_list)[0]

if debug:
    pandas.set_option('display.max_rows', 10)  # Only print first 5 and last 5 rows (10 rows total)
    print("\n", dataset, "\n")

features = dataset[:, 0:4].astype('float')
labels = dataset[:, 4].astype('float')  # Get answers

# dividing features, labels into train and test data
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, random_state=0)

# training a linear SVM classifier
svm_model = SupportVectorMachine(kernel='rbf', C=errorPenalty).fit(features_train, labels_train)
svm_predictions = svm_model.predict(features_test)


# Box-Muller sampling method for generating normally distributed
# random numbers from uniformly distributed random numbers.
def sample(mean, std_dev):
    u1 = 1.0 - random.rand()
    u2 = 1.0 - random.rand()
    rand_std_normal = sqrt(-2.0 * log(u1)) * sin(2.0 * pi * u2)
    rand_normal = mean + std_dev * rand_std_normal
    return rand_normal

if timeToComplete == 0:  # Didn't get a value for time to complete, need to sample one
    timeToComplete_mean = dataset[:, 2].mean()
    timeToComplete_stdDev = dataset[:, 2].std()
    timeToComplete = sample(timeToComplete_mean, timeToComplete_stdDev)
    if debug:
        print("No time to complete provided. Using Box-Muller sampled value:", timeToComplete)

# assignment = np.array([subject, daysTillDue, timeToComplete, difficulty])
# assignment = assignment.reshape(1, -1)  # Need to do if it's a single sample
# answer = svm_model.predict(assignment)[0].astype('int')

# Replace subject name with corresponding index in subject_list, then predict priorities
for assignment in gui.assignment_list:
    temp_assign = np.array(  # Temporary array as to preserve subject names
        [np.where(assignment.subject == subject_list)[0][0], assignment.days_till_due, assignment.time_to_complete,
         assignment.difficulty])
    assignment.priority = svm_model.predict(temp_assign.reshape(1, -1))[0].astype('int')


def sort_priority(a):
    return a.priority


gui.assignment_list.sort(reverse=True, key=sort_priority)  # Sort highest priority assignments first
gui.display_assignments()

if debug:
    print("Assignment:", assignment)

    # model accuracy for X_test
    accuracy = svm_model.score(features_test, labels_test)

    # creating a confusion matrix
    cm = confusion_matrix(labels_test, svm_predictions)

    print("\n# Support Vectors:", svm_model.n_support_, "\n")
    print("Confusion Matrix:\n", cm, "\n")
    print("Accuracy:", accuracy)

for assignment in gui.assignment_list:
    print(assignment)
