#!/usr/bin/env python3.6
import os
import pandas as pd
from wordcloud import WordCloud
from common import *
import nltk
import codecs, json
import math
nltk.download('wordnet')

#### Useful functions

def preprocessSpelling(input_list, split_by_comma=True, camel_case_to_spaces=True, underscore_to_spaces=True, spaces_to_underscores=False,
                        to_lowercase=True):
    if split_by_comma:
        output_list = [s.split(',') for s in input_list if s not in ['-', '']]  # split by comma
        output_list = [item for sublist in output_list for item in sublist]  # flatten list of list
    if camel_case_to_spaces:
        output_list = [camel_case_split(s) for s in output_list]  # resolve camel case into spaces
    if underscore_to_spaces:
         output_list = [n.strip().replace('_', ' ') for n in output_list]  # replace spaces with underscores
    if spaces_to_underscores:
         output_list = [n.strip().replace(' ', '_') for n in output_list]  # replace spaces with underscores
    if to_lowercase:
        output_list = [s.lower() for s in output_list]  # make all lower case
    return output_list

#### Read file with dataframe
resultsFile = "skill-taxonomy-extraction/data/in/20220119_skillTaxonomy.csv"

taxonomy = pd.read_csv(resultsFile, delimiter=';')
del taxonomy['Unnamed: 26']

taxonomyExp = pd.DataFrame(columns=['author', 'link', 'relevant', 'how', 'requirements', 'ind', 'hier',
       'similarity', 'skillclass', 'identified skillclass', 'skill',
       'identified skill', 'primitive', 'identified primitive',
       'parametrizedskill', 'identified parametrizedskill', 'task',
       'identified task', 'request', 'identified request', 'process',
       'identified process', 'arch', 'impl', 'param', 'paramtype'])

column = 'identified skill'
localIdx = 0

for idx, row in taxonomy.iterrows(): 
    length = len(row[column].split(','))
    if length > 1:
        for addIdx in range(length):
            localIdx = localIdx + 1
            taxonomyExp.loc[localIdx] = taxonomy.loc[idx]
    else:
        taxonomyExp.loc[localIdx] = taxonomy.loc[idx] 
        localIdx += 1

print(taxonomyExp[column])

#### Preprocess the data by cleaning and lematization

v_lemmatizer = np.vectorize(lemmatizer)

outputList = preprocessSpelling(input_list=taxonomy[column].dropna())
lemmaOutputList  = v_lemmatizer(outputList)
print(len(lemmaOutputList))

jsonString = json.dumps(lemmaOutputList.tolist())

with open('D:/1. Papers/4. MyPapers/6_(20210609) Skill taxonomy/skill-taxonomy-extraction/data/in/' + column.split(' ')[-1] + 'Def.json', 'w') as outfile:
    outfile.write(jsonString)