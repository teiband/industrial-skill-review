import copy
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib import rcParams
from nltk.stem import WordNetLemmatizer
from nltk.stem.lancaster import LancasterStemmer
from plotly.subplots import make_subplots

rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Times New Roman']
rcParams['font.size'] = '11'
rcParams['pdf.fonttype'] = 42
# import nltk
# nltk.download('wordnet') # for first time usage


st = LancasterStemmer()
wnl = WordNetLemmatizer()



def camel_case_split(string):
    words = [[string[0]]]

    for c in string[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    # return [''.join(word) for word in words]
    return " ".join([''.join(word) for word in words])


def split_names_into_words(skill_names, delimiter=','):
    """
    Splits a string into multiple words
    :param skill_names: string consisting of multiple words
    :param delimiter: character used for splitting
    :return:
    """
    extended_skill_names = []
    for skill in skill_names.T:
        curr_skill_names = []
        for answer in skill:
            for word in answer.strip().split(delimiter):
                word.strip()
                curr_skill_names.append(word)
        extended_skill_names.append(copy.deepcopy(curr_skill_names))
    return extended_skill_names


def clean_name(name):
    """
    Cleans a name consisting of multiple words from prepositions or other artifacts
    :param name: string
    :return: cleaned name
    """
    name = name.casefold()  # to lower case
    name = " ".join(name.split())  # remove redundant whitespace
    remove_list = ['to ', '"', 'sth.', 'the ', 'on ', '/']
    for r in remove_list:
        name = name.replace(r, '')
    replace_list = ['-']
    for r in replace_list:
        name = name.replace(r, '')
    # remove things in parenthesis
    i1 = name.find('(')
    if i1 >= 0:
        i2 = name[i1:].find(')')
        if i2 >= 0:
            name = name[:i1] + name[i2 + 1:]
    return name


def stemmer(name):
    """
    A stemmer tries to find the word stem for a given word, which does not necessarily result in a real english work
    :param name: source name
    :return: stemmed word
    """
    stemmed_name = ''
    for word in name.split(' '):
        stemmed_name += st.stem(word) + ' '
    return stemmed_name.strip()


def lemmatizer(name, part_of_speech='v'):
    """
    Lemmatization is preferred over Stemming because lemmatization does morphological analysis of the words.
    :param name: source name consisting of multiple words
    :param part_of_speech: tag from language theory: (n)oun, (p)ronoun, (v)erb, ..., adjective, adverb, preposition, conjunction, and interjection
    :return: lemmatized words
    """
    lemmatized_name = ''
    for word in name.split(' '):
        lemmatized_name += wnl.lemmatize(word, part_of_speech) + ' '
    return lemmatized_name.strip()


subplot_titles = (
    'touch',
    'press',
    'slide',
    'contour',
    'turn',
    'hand-over',
    'insert',
    'push')


def process_skill_names(subplot_titles, all_skill_names, rows=2, cols=4):
    subplot_titles = np.array(subplot_titles).reshape(cols, rows).T.flatten()

    fig = make_subplots(rows=rows, cols=cols, subplot_titles=subplot_titles, vertical_spacing=0.7,
                        horizontal_spacing=0.01)

    # ordered_skill_names = np.zeros((len(all_skill_names), np.max([len(l) for l in all_skill_names])))
    ordered_skill_names = []
    frequency_skill_names = []

    single_figs = []
    n_max_answers = 10

    for i, skill in enumerate(all_skill_names):
        c = Counter(skill)
        v = np.array(list(c.values()))
        vi = np.argsort(v)[::-1]  # invert sorting from many to less
        vo = v[vi]
        k = np.array(list(c.keys()))
        ko = k[vi]
        ordered_skill_names.append(ko.tolist())
        frequency_skill_names.append(vo.tolist())
        bar = go.Bar(x=ko, y=vo, textangle=90, marker_color='rgb(55, 83, 109)', orientation='v')
        fig.add_trace(bar, row=i % rows + 1,
                      col=int(i / rows) + 1)
        tmp_fig = go.Figure(
            data=bar,
            layout_title_text=subplot_titles[i],
        )
        # single_figs.append(tmp_fig)
        tmp_fig = plt.figure(figsize=(2.8, 3.0))

        cur_max_answers = min(n_max_answers, len(ko))
        t = range(cur_max_answers)
        plt.bar(t, vo[:cur_max_answers])
        plt.xticks(ticks=t, labels=ko[:cur_max_answers], rotation='vertical')
        plt.subplots_adjust(bottom=0.8)
        #plt.tight_layout()
        single_figs.append(tmp_fig)

    return ordered_skill_names, frequency_skill_names, fig, single_figs
