"""
Serena Cheng
CMSC 416 - PA 4: WSD (wsd.py)
3/31/2020
~~~~~
Problem:

Usage:

Ex.
Algorithm:

"""

import sys
import re

train_set = sys.argv[1]
test_set = sys.argv[2]
model = sys.argv[3]

train_content = []
test_content = []

sense_phone = "phone"
sense_product = "product"

w_plus_1 = "+1"
w_minus_1 = "-1"
w_pair_minus_2 = "-2 & -1"
w_pair_plus_2 = "+1 & +2"
w_pair_minus_plus_1 = "-1 & +1"
w_window_3 = "k=3"
w_window_5 = "k=5"
w_window_10 = "k=10"

feature_sense_dict = {w_plus_1: {}, w_minus_1: {}, w_pair_minus_2: {}, w_pair_plus_2: {},
                      w_pair_minus_plus_1: {}, w_window_3: {}, w_window_5: {}, w_window_10: {}}
feature_frequency_dict = {}


def clean_context(content):
    content = re.sub(r'(<.>|<\/.>|\.|,|;|!|-|\")', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    content = re.sub("lines", "line", content)
    return content.split()


def add_to_feature_sense_dict(feature_type, feature_word):
    if feature_word not in feature_sense_dict[feature_type].keys():
        feature_sense_dict[feature_type][feature_word] = {sense_phone: 0, sense_product: 0}

    feature_sense_dict[feature_type][feature_word][sense] += 1


def add_with_window_size(context_list, feature_type, k, target_ind, add_frequencies):
    for ind in range(target_ind - k, target_ind + k):
        if ind < 0 or ind >= len(context_list) or ind == target_ind:
            continue

        add_to_feature_sense_dict(feature_type, context_list[ind])

        if add_frequencies:
            increment_feature_frequency(context_list[ind])


def increment_feature_frequency(feature):
    if feature in feature_frequency_dict.keys():
        feature_frequency_dict[feature] += 1
    else:
        feature_frequency_dict[feature] = 1


with open(train_set, 'r', encoding="utf-8-sig") as file:
    train_content.extend(file.read().lower().split("</instance>"))
    train_content.pop()

with open(test_set, 'r', encoding="utf-8-sig") as file:
    test_content.extend(file.read().lower().split("</instance>"))
    test_content.pop()

for instance in train_content:
    sense = instance[instance.find("senseid=") + 9: instance.find("\"/>")]

    context = instance[instance.find("<context>") + 9: instance.find("</context>")]
    context_words = clean_context(context)

    target = context_words.index("<head>line</head>")

    if target + 1 < len(context_words):
        add_to_feature_sense_dict(w_plus_1, context_words[target + 1])

    if target - 1 >= 0:
        add_to_feature_sense_dict(w_minus_1, context_words[target - 1])

    if target - 2 >= 0:
        bigram = context_words[target - 2] + " " + context_words[target - 1]
        add_to_feature_sense_dict(w_pair_minus_2, bigram)
        increment_feature_frequency(bigram)

    if target + 2 < len(context_words):
        bigram = context_words[target + 1] + " " + context_words[target + 2]
        add_to_feature_sense_dict(w_pair_plus_2, bigram)
        increment_feature_frequency(bigram)

    if target - 1 >= 0 and target + 1 < len(context_words):
        bigram = context_words[target - 1] + " " + context_words[target + 1]
        add_to_feature_sense_dict(w_pair_minus_plus_1, bigram)
        increment_feature_frequency(bigram)

    add_with_window_size(context_words, w_window_3, 3, target, False)
    add_with_window_size(context_words, w_window_5, 5, target, False)
    add_with_window_size(context_words, w_window_10, 10, target, True)

print(feature_frequency_dict)





