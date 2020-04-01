"""
Serena Cheng
CMSC 416 - PA 4: WSD (scorer.py)
3/31/2020
~~~~~
Problem:
This program addresses the goal of scoring the accuracy of the POS tagger.
The overall accuracy of the implemented tagger is 0.81 or 81%.
Usage:
The user should include the template below when executing:
    (tagged test data) (test key data) > (tag report stdout)
Ex. python3 tagger.py test-with-tags.txt pos-test-key.txt > tag-report.txt
    > Baseline Accuracy: 0.13
    > Overall Accuracy: 0.81
    > (confusion matrix displayed)
Algorithm:
Each tag in the tagged test set is compared to the tag in the key and then
inputted in the confusion matrix. The baseline accuracy is calculated by
assuming every tag to be the most frequent one (in this case it is "NN") and
dividing the number of correct instances by the total number of tags. The
overall accuracy is calculated by dividing the total correct tags by the
total number of tags.
"""

import sys
import re

line_answers = sys.argv[1]  # tagged test set file
line_key = sys.argv[2]  # test key file

answer_content = []  # test broken apart
key_content = []  # key broken apart

answers = []
key = []

senses = {"phone": 0, "product": 1}


# split tags from words and add to respective tag arrays
def get_senses(answer_list, instance_sense_dict):
    for ans in answer_list:
        sense = re.search(r'senseid=\"(.*)\"', ans).group(1)
        instance_sense_dict.append(sense)


# tokenize tagged test
with open(line_answers, 'r', encoding="utf-8-sig") as file:
    answer_content.extend(file.read().split("\n"))
    answer_content.pop()

# tokenize key
with open(line_key, 'r', encoding="utf-8-sig") as file:
    key_content.extend(file.read().split("\n"))
    key_content.pop()

# get only tags
get_senses(answer_content, answers)
get_senses(key_content, key)

# # create matrix filled with 0s that is sized (num of tags x num of tags)
confusion_matrix = [[0] * len(senses) for _ in range(len(senses))]

most_sense = ''  # most frequent tag
most_count = 0  # correct count of frequent tag
total_correct = 0  # total correct count of all tags
for ind in range(len(key)):
    actual_sense = key[ind]  # actual
    predicted_sense = answers[ind]  # predicted

    # increment on matrix
    confusion_matrix[senses[actual_sense]][senses[predicted_sense]] += 1

    if actual_sense == predicted_sense:
        # update if tag count is higher than current highest count
        if confusion_matrix[senses[actual_sense]][senses[predicted_sense]] > most_count:
            most_sense = actual_sense
            most_count = confusion_matrix[senses[actual_sense]][senses[predicted_sense]]

        # increment total correct count if tag is correct
        total_correct += 1

# BA = (num of correct tags if all are most frequent tag)/total num of tags
baseline_accuracy = round(most_count / len(key), 2)
# A = num of correct tags/total num of tags
accuracy = round(total_correct / len(key), 2)

print("Baseline Accuracy:", baseline_accuracy)
print("Overall Accuracy:", accuracy)

ordered_tags = [''] * len(senses)
# put tags in order
for tag, num in senses.items():
    ordered_tags[num] = tag

# print all tags horizontally
for ind in range(len(ordered_tags)):
    if ind == 0:
        print("\n        ", end='')
    print(format(ordered_tags[ind], '>4'), end=' ')

# print all tags and counts in matrix
for ind in range(len(senses)):
    print("\n", format(ordered_tags[ind], '7'), end='')
    for j in range(len(senses)):
        print(format(confusion_matrix[ind][j], '5'), end=' ')
