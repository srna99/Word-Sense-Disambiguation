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
import math

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
ranked_tests = []


def clean_context(content):
    content = re.sub(r'(<.>|<\/.>|\.|,|;|!|-|&|\)|\(|\"|\?)', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    # content = re.sub(r'\s(of|a|the|is|was|in|an|are|at|but)\s', ' ', content)
    # content = re.sub(r'\s+', ' ', content)
    content = re.sub("lines", "line", content)
    return content.split()


def add_to_feature_sense_dict(w_feature, feature_word):
    if feature_word not in feature_sense_dict[w_feature].keys():
        feature_sense_dict[w_feature][feature_word] = {sense_phone: 1, sense_product: 1}

    feature_sense_dict[w_feature][feature_word][sense] += 1


def add_with_window_size(context_list, w_feature, k, target_ind, add_frequencies):
    for ind in range(target_ind - k, target_ind + k):
        if ind < 0 or ind >= len(context_list) or ind == target_ind:
            continue

        add_to_feature_sense_dict(w_feature, context_list[ind])

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

for feature_type, feature_list in feature_sense_dict.items():
    for feature, frequency in feature_list.items():
        prob_phone = frequency[sense_phone] / feature_frequency_dict[feature]
        prob_product = frequency[sense_product] / feature_frequency_dict[feature]

        if prob_phone >= prob_product:
            sense = sense_phone
        else:
            sense = sense_product

        log_likelihood_ratio = round(abs(math.log(prob_phone / prob_product)), 5)

        test = (log_likelihood_ratio, feature_type, feature, sense)
        ranked_tests.append(test)

ranked_tests.sort(key=lambda x: x[0], reverse=True)
print(ranked_tests[0])






