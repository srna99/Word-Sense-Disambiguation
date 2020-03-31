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
sense_frequency_dict = {sense_phone: 0, sense_product: 0}

ranked_tests = []
answers = []


def clean_context(content):
    content = re.sub(r'(<.>|<\/.>|\.|,|;|!|-|&|\)|\(|\"|\?)', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    # content = re.sub(r'\s(of|a|the|is|was|in|an|are|at|but|you)\s', ' ', content)
    # content = re.sub(r'\s+', ' ', content)
    content = re.sub(">lines<", ">line<", content)
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


def increment_feature_frequency(feature_term):
    if feature_term in feature_frequency_dict.keys():
        feature_frequency_dict[feature_term] += 1
    else:
        feature_frequency_dict[feature_term] = 1


def create_test(test_number, feature_term, is_list):
    test_feature = ranked_tests[test_number]

    if is_list and test_feature[2] in feature_term:
        return True
    elif not is_list and feature_term == test_feature[2]:
        return True

    return False


def create_test_feature_list(context_list, k, target_ind):
    features_list = []
    for i in range(target_ind - k, target_ind + k):
        if i < 0 or i >= len(context_list) or i == target_ind:
            continue
        features_list.append(context_list[i])

    return features_list


with open(train_set, 'r', encoding="utf-8-sig") as file:
    train_content.extend(file.read().lower().split("</instance>"))
    train_content.pop()

with open(test_set, 'r', encoding="utf-8-sig") as file:
    test_content.extend(file.read().lower().split("</instance>"))
    test_content.pop()

for instance in train_content:
    sense = re.search(r'senseid=\"(.*)\"', instance).group(1)
    sense_frequency_dict[sense] += 1

    context = re.search(r'<context>\n(.*)\n</context>', instance).group(1)
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

with open(model, 'w', encoding="utf-8-sig") as file:
    for data in ranked_tests:
        line = "feature type = " + data[1] + ", feature = " + data[2] + ", log-likelihood score = " + str(
                data[0]) + ", sense = " + data[3] + "\n"
        file.write(line)

for instance in test_content:
    instance_id = re.search(r'instance id=\"(.*)\"', instance).group(1)

    context = re.search(r'<context>\n(.*)\n</context>', instance).group(1)
    context_words = clean_context(context)

    target = context_words.index("<head>line</head>")

    sense = ""
    for ind, test in enumerate(ranked_tests):
        if test[1] == w_plus_1 and target + 1 < len(context_words):
            if create_test(ind, context_words[target + 1], False):
                sense = test[3]
                break
        elif test[1] == w_minus_1 and target - 1 >= 0:
            if create_test(ind, context_words[target - 1], False):
                sense = test[3]
                break
        elif test[1] == w_pair_minus_2 and target - 2 >= 0:
            if create_test(ind, context_words[target - 2] + " " + context_words[target - 1], False):
                sense = test[3]
                break
        elif test[1] == w_pair_plus_2 and target + 2 < len(context_words):
            if create_test(ind, context_words[target + 1] + " " + context_words[target + 2], False):
                sense = test[3]
                break
        elif test[1] == w_pair_minus_plus_1 and target - 1 >= 0 and target + 1 < len(context_words):
            if create_test(ind, context_words[target - 1] + " " + context_words[target + 1], False):
                sense = test[3]
                break
        elif test[1] == w_window_3:
            if create_test(ind, create_test_feature_list(context_words, 3, target), True):
                sense = test[3]
                break
        elif test[1] == w_window_5:
            if create_test(ind, create_test_feature_list(context_words, 5, target), True):
                sense = test[3]
                break
        elif test[1] == w_window_10:
            if create_test(ind, create_test_feature_list(context_words, 10, target), True):
                sense = test[3]
                break

    if sense == "":
        if sense_frequency_dict[sense_phone] >= sense_frequency_dict[sense_product]:
            sense = sense_phone
        else:
            sense = sense_product

    answer = "<answer instance=\"" + instance_id + "\" senseid=\"" + sense + "\"/>"
    answers.append(answer)

for answer in answers:
    print(answer)
