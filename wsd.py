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

frequency_dict = {w_plus_1: {}, w_minus_1: {}, w_pair_minus_2: {},
                  w_pair_plus_2: {}, w_pair_minus_plus_1: {}, w_window_3: {},
                  w_window_5: {}}


def clean_context(content):
    content = re.sub(r'(<.>|<\/.>|\.|,|\")', ' ', content)
    content = re.sub(r'\s+', ' ', content)
    content = re.sub("lines", "line", content)
    return content.split()


with open(train_set, 'r', encoding="utf-8-sig") as file:
    train_content.extend(file.read().lower().split("</instance>"))
    train_content.pop()

with open(test_set, 'r', encoding="utf-8-sig") as file:
    test_content.extend(file.read().lower().split("</instance>"))
    test_content.pop()

for instance in train_content:
    sense = instance[instance.find("senseid=") + 9: instance.find("\"/>")]

    context = instance[
              instance.find("<context>") + 9: instance.find("</context>")]
    context_words = clean_context(context)
    print(context_words)
    target = context_words.index("<head>line</head>")

    if target + 1 < len(context_words):
        feature_word = context_words[target + 1]
        print(feature_word)
        if feature_word not in frequency_dict[w_plus_1].keys():
            frequency_dict[w_plus_1] = {feature_word: {}}
            frequency_dict[w_plus_1][feature_word] = {sense_phone: 0,
                                                      sense_product: 0}
        frequency_dict[w_plus_1][feature_word][sense] += 1

print(frequency_dict)
# print(frequency_dict)
# break
