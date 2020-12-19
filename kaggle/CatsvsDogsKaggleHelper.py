import os
import random
from shutil import copyfile

def create_folders():
    try:
        os.mkdir('D:/Downloads/training')
        os.mkdir('D:/Downloads/training/cats')
        os.mkdir('D:/Downloads/training/dogs')
        os.mkdir('D:/Downloads/validation')
        os.mkdir('D:/Downloads/validation/cats')
        os.mkdir('D:/Downloads/validation/dogs')
    except OSError:
        pass

def preprocess_data(SOURCE):
    catNames = []
    dogNames = []
    for unitData in os.listdir(SOURCE):
        data = SOURCE + unitData
        if(os.path.getsize(data)> 0 and unitData.find('cat')!= -1):
            catNames.append(unitData)
        elif (os.path.getsize(data) > 0 and unitData.find('dog') != -1):
            dogNames.append(unitData)

    return catNames, dogNames

def split_data(SOURCE, TRAINING, TESTING, SPLIT_SIZE, FILENAMES):
    train_data_length = int(len(FILENAMES) * SPLIT_SIZE)
    shuffled_set = random.sample(FILENAMES, len(FILENAMES))
    train_set = shuffled_set[:train_data_length]
    test_set = shuffled_set[train_data_length:]

    for data in train_set:
        temp_train_data = SOURCE + data
        final_train_data = TRAINING + data
        copyfile(temp_train_data, final_train_data)

    for data in test_set:
        temp_test_data = SOURCE + data
        final_test_data = TESTING + data
        copyfile(temp_test_data, final_test_data)


create_folders()
catNames, dogNames = preprocess_data('D:/Downloads/train/')

split_data('D:/Downloads/train/', 'D:/Downloads/training/cats/', 'D:/Downloads/validation/cats/', 0.9, catNames)
split_data('D:/Downloads/train/', 'D:/Downloads/training/dogs/', 'D:/Downloads/validation/dogs/', 0.9, dogNames)
