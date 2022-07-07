#!/usr/bin/env python3.6
import collections
import csv
import os
import time
from tkinter import font
try:
    import inflect
except:
    os.system("pip3 install inflect --user")
inflect = inflect.engine()

from common import *

MAX_WORDS = 10
FOR_SLIDES = True

this_file_dir = os.path.dirname(os.path.realpath(__file__))
results_file = os.path.join(this_file_dir, "../data/in/20220223_skillTaxonomy.csv")

with open(results_file, 'r') as f:
    lines = f.readlines()

results = []
for l in csv.reader(lines, quotechar='"', delimiter=';',
                    quoting=csv.QUOTE_ALL, skipinitialspace=True):
    # print(l)
    results.append(l)

results = np.array(results)

header = results[0, :]
results = results[1:, :]

# relevant papers
selection_symbol = 'Y'
selection_column = 2
selected_results = results[results[:, selection_column] == selection_symbol, :]

# # industrial  / non-industrial
selection_symbol = 'X'
selection_column = 5
selected_results = results[results[:, selection_column] == selection_symbol, :]


def preprocess_spelling(input_list, split_by_comma=True, camel_case_to_spaces=True, spaces_to_underscores=True,
                        to_lowercase=True):
    if split_by_comma:
        output_list = [s.split(',') for s in input_list if s not in ['-', '']]  # split by comma
        output_list = [item for sublist in output_list for item in sublist]  # flatten list of list
    if "" in output_list:  # check for empty names, could result from a name with trailing comma
        idx = output_list.index("")
        print(
            f"WARNING: found at least one empty string '' in output_list after item: {output_list[idx - 1]} with index: {idx}")
    if camel_case_to_spaces:
        output_list = [camel_case_split(s) for s in output_list]  # resolve camel case into spaces_?
    if spaces_to_underscores:
        output_list = [n.strip().replace(' ', '_') for n in output_list]  # replace spaces with underscores
    if to_lowercase:
        output_list = [s.lower() for s in output_list]  # make all lower case
    return output_list


# column_mapping = {'implementation': 23,
#                   'requirements': 4,
#                   'param': 24}

column_mapping = {'Skills': 10,
                  'IdentifiedSkills': 11,
                  'Primitives': 12,
                  'IdentifiedPrimitives': 13,
                  'Tasks': 16,
                  'IdentifiedTasks': 17
                  }


single_figs = []
plot_titles = []

import seaborn as sns
import pandas as pd
#sns.distplot(data)

def plot_hist(word_list, plot_title, n_words=8, xlabel_rotation=90):
    # counts = Counter(word_list) # for all words
    counts = dict(Counter(word_list).most_common(n_words))

    labels, values = zip(*counts.items())

    # sort your values in descending order
    indSort = np.argsort(values)[::-1]

    # rearrange your data
    labels = np.array(labels)[indSort]
    values = np.array(values)[indSort]

    indexes = np.arange(len(labels))

    data = pd.DataFrame(indexes, values)

    #fig, axes = plt.subplots()
    if FOR_SLIDES:
        fig = plt.figure(figsize=(6, 4), num=plot_title)
        # plt.bar(indexes, values, width=0.5)
        sns.barplot(indexes, values, color=[0, 0, 0.6])

        # add labels
        plt.xticks(indexes, labels, rotation=90)
        plt.ylabel("Number of appearances")
    else:
        fig = plt.figure(figsize=(16, 8), dpi=100, facecolor='w', edgecolor='k')
        sns.barplot(indexes, values) #, bins=200, alpha=0.7, range=(14.2, 16.4), label='10mm', color='#003359')

        # add labels
        plt.xticks(indexes, labels, rotation=70, fontsize=16)
        plt.yticks(fontsize=16)
        plt.ylabel("Number of appearances", fontsize = 17)

    
    plt.tight_layout()
    # plt.show()
    single_figs.append(fig)
    plot_titles.append(plot_title)


for key, value in column_mapping.items():
    label = key
    input_list = selected_results[:, value]
    output_list = preprocess_spelling(input_list=input_list)
    output_list = [n.strip().replace('x', '') for n in output_list]

    # remove plural forms, ending with s and keep singular word
    for i, word in enumerate(output_list):
        if word.endswith("ss"):
            continue
        singular_word = inflect.singular_noun(word)
        if singular_word == False:
            pass
        else:
            print(f"Found plural: {word}")
            output_list[i] = singular_word

    if (label != "requirements"):
        if (label != 'param'):
            plot_hist(output_list, label, MAX_WORDS)
            plt.savefig(os.path.join(os.path.dirname(__file__), "..", "data", "out", "barplot-" + key + ".pdf"),
                        dpi=600)
            plt.savefig(os.path.join(os.path.dirname(__file__), "..", "data", "out", "barplot-" + key + ".png"),
                        dpi=600)
        else:
            output_list = [n.strip().replace('parameter', '') for n in output_list]
            # remove empty entries from previous step
            while "" in output_list:
                output_list.remove("")
            plot_hist(output_list, label, MAX_WORDS, xlabel_rotation=0)
            plt.savefig(os.path.join(os.path.dirname(__file__), "..", "data", "out", "barplot-" + key + ".pdf"),
                        dpi=600)
            plt.savefig(os.path.join(os.path.dirname(__file__), "..", "data", "out", "barplot-" + key + ".png"),
                        dpi=600)
    else:
        output_list = [n.strip().replace(' 6', '6') for n in output_list]
        counter = collections.Counter(output_list)
        print(counter)
        plot_hist(output_list, label, MAX_WORDS)
        plt.savefig(os.path.join(os.path.dirname(__file__), "..", "data", "out", "barplot-" + key + ".pdf"), dpi=600)
        plt.savefig(os.path.join(os.path.dirname(__file__), "..", "data", "out", "barplot-" + key + ".png"), dpi=600)
        
plt.show()
