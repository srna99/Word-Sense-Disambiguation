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

test_with_tags = sys.argv[1]  # tagged test set file
test_key = sys.argv[2]  # test key file

test_tagged_content = []  # test broken apart
test_key_content = []  # key broken apart

tags_test = []  # tags from test
tags_key = []  # tags from key


# split tags from words and add to respective tag arrays
def separate_tags(array, sep_array):
    for term in array:
        # skip brackets
        if term == '[' or term == ']':
            continue

        # separate words from tags
        parts = term.rsplit('/', 1)
        pos = parts[1].split('|')[0]
        sep_array.append(pos)


# tokenize tagged test
with open(test_with_tags, 'r', encoding="utf-8-sig") as file:
    test_tagged_content.extend(file.read().split())

# tokenize key
with open(test_key, 'r', encoding="utf-8-sig") as file:
    test_key_content.extend(file.read().split())

# get only tags
separate_tags(test_tagged_content, tags_test)
separate_tags(test_key_content, tags_key)

all_tags = set(tags_key)  # get unique tags
tag_dict = dict(zip(all_tags, range(len(all_tags))))  # associate tag with num

# create matrix filled with 0s that is sized (num of tags x num of tags)
confusion_matrix = [[0] * len(all_tags) for _ in range(len(all_tags))]

most_tag = ''  # most frequent tag
most_count = 0  # correct count of frequent tag
total_correct = 0  # total correct count of all tags
for i in range(len(tags_key)):
    actual_tag = tags_key[i]  # actual
    predicted_tag = tags_test[i]  # predicted

    # increment on matrix
    confusion_matrix[tag_dict[actual_tag]][tag_dict[predicted_tag]] += 1

    if actual_tag == predicted_tag:
        # update if tag count is higher than current highest count
        if confusion_matrix[tag_dict[actual_tag]][tag_dict[predicted_tag]] > \
                most_count:
            most_tag = actual_tag
            most_count = confusion_matrix[tag_dict[actual_tag]][tag_dict[
                predicted_tag]]

        # increment total correct count if tag is correct
        total_correct += 1

# BA = (num of correct tags if all are most frequent tag)/total num of tags
baseline_accuracy = round(most_count / len(tags_key), 2)
# A = num of correct tags/total num of tags
accuracy = round(total_correct / len(tags_key), 2)

print("Baseline Accuracy:", baseline_accuracy)
print("Overall Accuracy:", accuracy)

ordered_tags = [''] * len(all_tags)
# put tags in order
for tag, num in tag_dict.items():
    ordered_tags[num] = tag

# print all tags horizontally
for i in range(len(ordered_tags)):
    if i == 0:
        print("\n     ", end='')
    print(format(ordered_tags[i], '>4'), end=' ')

# print all tags and counts in matrix
for i in range(len(all_tags)):
    print("\n", format(ordered_tags[i], '4'), end='')
    for j in range(len(all_tags)):
        print(format(confusion_matrix[i][j], '4'), end=' ')