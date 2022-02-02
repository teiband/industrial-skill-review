#!/usr/bin/env python3.6
import os
import pandas as pd
#from sqlalchemy import true
from wordcloud import WordCloud
from common import *
import nltk
import codecs, json
import math
nltk.download('wordnet')

#### Useful functions

def preprocess_spelling(input_list, split_by_comma=True, camel_case_to_spaces=True, underscore_to_spaces=True, spaces_to_underscores=False,
                        to_lowercase=True, remove_words = True, remove_dash = True, change_and = True, column_name=''):

    # If errors appear that means there might be an empty word after the ,
    if split_by_comma:
        output_list = [s.split(',') for s in input_list if s not in ['-', '']]  # split by comma
        output_list = [item for sublist in output_list for item in sublist]  # flatten list of list
    if change_and:
         output_list = [n.strip().replace('&', ' ') for n in output_list]  # replace spaces with underscores
    if remove_dash:
         output_list = [n.strip().replace('-', ' ') for n in output_list]  # replace spaces with underscores
    if camel_case_to_spaces:
        output_list = [camel_case_split(s) for s in output_list]  # resolve camel case into spaces
    if underscore_to_spaces:
         output_list = [n.strip().replace('_', ' ') for n in output_list]  # replace spaces with underscores
    if spaces_to_underscores:
         output_list = [n.strip().replace(' ', '_') for n in output_list]  # replace spaces with underscores
    if to_lowercase:
        output_list = [s.lower() for s in output_list]  # make all lower case
    if remove_words:
        output_list = [n.strip().replace('robot ', ' ') for n in output_list] # take care of trailing space!
        output_list = [n.strip().replace('robotic ', ' ') for n in output_list]  # take care of trailing space!
        output_list = [n.strip().replace(column_name + 's', '') for n in output_list] # remove plural form of column name
        output_list = [n.strip().replace(column_name, '') for n in output_list] # remove singular form of column name
    return output_list


############ MAIN FILE ############


#### Read file with dataframe
#resultsFile = "skill-taxonomy-extraction/data/in/20220127_skillTaxonomy.csv"
this_file_dir = os.path.dirname(os.path.realpath(__file__))
resultsFile = os.path.join(this_file_dir, "../data/in/20220202_skillTaxonomy.csv")


taxonomy = pd.read_csv(resultsFile, delimiter=';')

taxonomy = taxonomy.loc[taxonomy['relevant'] == 'Y']

taxonomyExp = pd.DataFrame(columns=['author', 'link', 'relevant', 'how', 'requirements', 'ind', 'hier',
       'similarity', 'skillclass', 'identified skillclass', 'skill',
       'identified skill', 'primitive', 'identified primitive',
       'parametrizedskill', 'identified parametrizedskill', 'task',
       'identified task', 'request', 'identified request', 'process',
       'identified process', 'arch', 'impl', 'param', 'paramtype'])

column = 'identified task'
localIdx = 0
first = True

for idx, row in taxonomy.iterrows(): 
    if first:
        localIdx = idx
        first = False
    length = len(row[column].split(','))
    if length > 1:
        for internal in range(length):
            taxonomyExp.loc[localIdx] = taxonomy.loc[idx]
            localIdx = localIdx + 1
    else:
        taxonomyExp.loc[localIdx] = taxonomy.loc[idx] 
        localIdx += 1

# Do tests on data integrity
def check_data_integrity(taxonomyExp):

    def has_digits(x):
        if any(c.isdigit() for c in x):
            raise Exception(f"Field contains digits in : {x}")

    def has_too_short_word(x):
        x_list = x.split(' ')
        allowed_short_words = ("-", ",", "in", "up", "to", "on", "of", "at", "or")
        if any(w for w in x_list if len(w) < 3 and w.lower() not in allowed_short_words):
            raise Exception(f"Field contains too short word in: {x}")

    def has_parenthesis(x):
        if '(' in x or ')' in x:
            raise Exception(f"Field contains at least one parenthesis (, ): {x}")

    for key in ('identified task', 'identified skill', 'identified primitive'):
        col = taxonomyExp[key]
        col.apply(has_digits)
        col.apply(has_too_short_word)
        col.apply(has_parenthesis)

check_data_integrity(taxonomyExp)

taxonomyExp = taxonomyExp.loc[taxonomyExp[column] != '-']
print("data frame length: " + str(len(taxonomyExp[column].to_list())))
# the taxonomyExp dataframe has the same amount of rows as the one excorporated by the preprocessing if - are discarded

#### Preprocess the data by cleaning and lematization

v_lemmatizer = np.vectorize(lemmatizer)

outputList = preprocess_spelling(input_list=taxonomy[column].dropna(), column_name=column.split(' ')[-1])
lemmaOutputList  = v_lemmatizer(outputList)
# unique names have not been sorted
print("processed length: " + str(len(lemmaOutputList)))


jsonString = json.dumps(lemmaOutputList.tolist())

#with open('D:/1. Papers/4. MyPapers/6_(20210609) Skill taxonomy/skill-taxonomy-extraction/data/in/' + column.split(' ')[-1] + 'Def.json', 'w') as outfile:
with open(os.path.join(this_file_dir, "..", "data/in/" + column.split(' ')[-1] + 'Def.json'), 'w') as outfile:
    outfile.write(jsonString)