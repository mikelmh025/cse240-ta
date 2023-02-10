#!/usr/bin/env python3
import sys
import os
import numpy as np
import time
import subprocess

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("pygame")
import pygame
# import pygame

[_, input_dir, output_dir] = sys.argv
submit_dir = os.path.join(input_dir, 'res')
sys.path.append(submit_dir)

from boostit import BoostingClassifier

# codalab evaluation only
dataset_dir = os.path.join(input_dir, 'ref')
train_set = os.path.join(dataset_dir, 'train.npy')
test_set = os.path.join(dataset_dir, 'test.npy')
model_path = os.path.join(submit_dir, 'model.npy')

def evaluation_score(y_pred, y_test):
    y_pred = np.squeeze(y_pred)
    assert y_pred.shape == y_test.shape, "Error: the shape of your prediction doesn't match the shape of ground truth label."

    TP = 0	# truth positive
    FN = 0	# false negetive
    TN = 0	# true negetive
    FP = 0 	# false positive

    for i in range(len(y_pred)):
        pred_label = y_pred[i]
        gt_label = y_test[i]

        if int(pred_label) == -1:
            if pred_label == gt_label:
                TN += 1
            else:
                FN += 1
        else:
            if pred_label == gt_label:
                TP += 1
            else:
                FP += 1

    accuracy = (TP + TN) / (TP + FN + FP + TN)
    precision = TP / (TP + FP) if ((TP + FP) > 0) else 0
    recall = TP / (TP + FN) if ((TP + FN)) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if ((precision + recall) > 0) else 0
    final_score = 50 * accuracy + 50 * f1

    return accuracy, precision, recall, f1, final_score

# load dataset
with open(train_set, 'rb') as f:
    X_train = np.load(f)
    y_train = np.load(f)

with open(test_set, 'rb') as f:
    X_test = np.load(f)
    y_test = np.load(f)

arr = np.load(model_path)
print('success load model.npy')

clf = BoostingClassifier().fit(X_train, y_train)
y_pred = clf.predict(X_test)
acc, precision, recall, f1, final_score = evaluation_score(y_pred, y_test)

with open(os.path.join(output_dir, 'scores.txt'), 'w') as output_file:
    print("Accuracy: {}, F-measure: {}, Precision: {}, Recall: {}, Final_Score: {}".format(acc, f1, precision, recall, final_score))
    output_file.write("Accuracy:{}\nFmeasure:{}\nPrecision:{}\nRecall:{}\nFinal_Score:{}".format(acc, f1, precision, recall, final_score))
