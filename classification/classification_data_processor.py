import os
import csv

folder_path = os.path.join(os.getcwd(), 'classification')
source_file_name = 'classification_data.csv'
train_file_name = 'train_data.csv'
test_file_name = 'test_data.csv'

train_data_proportion = 0.8
test_data_proportion = 1.0 - train_data_proportion

def process():
    if not os.path.isfile(os.path.join(folder_path, source_file_name)):
        report = "Error... Source file not found. Please import the data first."
        return report
    labels = get_labels()
    labels_count = get_labels_count(labels)
    # Determine the number of data allocated to the training data
    # The rests go to the test data
    train_data_count = {}
    for label in labels_count:
        train_data_count[label] = int(labels_count[label] * train_data_proportion)
    # Separate the train and test data
    train_csv_file = open(os.path.join(folder_path, train_file_name), mode='w')
    test_csv_file = open(os.path.join(folder_path, test_file_name), mode='w')
    train_csv_writer = csv.writer(train_csv_file)
    test_csv_writer = csv.writer(test_csv_file)
    # Write data to the train file and test file
    # Beforehand, write the header file
    train_csv_writer.writerow(['id', 'title', 'content', 'label'])
    test_csv_writer.writerow(['id', 'title', 'content', 'label'])
    for label in labels:
        data = get_data_with_label(label)
        train_data = data[:train_data_count[label]]
        test_data = data[train_data_count[label]:]
        train_csv_writer.writerows(train_data)
        test_csv_writer.writerows(test_data)
    train_csv_file.close()
    test_csv_file.close()
    report = 'Train and test data created'
    return report


def get_labels():
    labels = []
    with open(os.path.join(folder_path, source_file_name), mode='r') as csv_file:
        reader = csv.reader(csv_file)
        for data in reader:
            # data[3] is the label
            if data[3] not in labels:
                labels.append(data[3])
    return labels

def get_labels_count(labels):
    labels_count = {}
    for label in labels:
        labels_count[label] = 0
    with open(os.path.join(folder_path, source_file_name), mode='r') as csv_file:
        reader = csv.reader(csv_file)
        for data in reader:
            labels_count[data[3]] = labels_count[data[3]] + 1
    return labels_count

def get_data_with_label(label):
    data = []
    with open(os.path.join(folder_path, source_file_name), mode='r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if row[3] == label:
                data.append(row)
    return data
