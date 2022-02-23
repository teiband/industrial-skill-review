#!/usr/bin/env python3.6
import csv
import pickle
import time
import os

from wordcloud import WordCloud

from common import *

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

# The following cannot handle delimiters in double quotes
# results_1 = np.loadtxt(results_1_file, dtype=str, delimiter=',')

header = results[0, :]
results = results[1:, :]

# relevant papers
selection_symbol = 'Y'
selection_column = 2
selected_results = results[results[:, selection_column] == selection_symbol, :]

# # industrial  / non-industrial
selection_symbol = '-'
selection_column = 5
selected_results = results[results[:, selection_column] == selection_symbol, :]

 
def preprocess_spelling(input_list, split_by_comma=True, camel_case_to_spaces=True, spaces_to_underscores=True,
                        to_lowercase=True):
    if split_by_comma:
        output_list = [s.split(',') for s in input_list if s not in ['-', '']]  # split by comma
        output_list = [item for sublist in output_list for item in sublist]  # flatten list of list
    if "" in output_list: # check for empty names, could result from a name with trailing comma
        idx = output_list.index("")
        print(f"WARNING: found at least one empty string '' in output_list after item: {output_list[idx-1]} with index: {idx}")
    if camel_case_to_spaces:
        output_list = [camel_case_split(s) for s in output_list]  # resolve camel case into spaces_?
    if spaces_to_underscores:
        output_list = [n.strip().replace(' ', '_') for n in output_list]  # replace spaces with underscores
    if to_lowercase:
        output_list = [s.lower() for s in output_list]  # make all lower case
    return output_list


def plot_cloud(wordcloud):
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout()

# For skills naming
# column_mapping = {'Skills': 10,
#                   'IdentifiedSkills': 11,
#                   'Primitives': 12,
#                   'IdentifiedPrimitives': 13,
#                   'Tasks': 16,
#                   'IdentifiedTasks': 17
#                   }

# Implementation
column_mapping = {'implementation': 23, 
                  'requirements': 4,
                  'param': 24}

start = time.time()
for key, value in column_mapping.items():
    label = key
    input_list = selected_results[:, value]
    output_list = preprocess_spelling(input_list=input_list)
    output_list = [n.strip().replace('x', '') for n in output_list]
    output_joined = ", ".join(output_list)  # join to single string

    # Generate word cloud
    if (label != "requirements"):
        wordcloudName = WordCloud(width=800, height=400, random_state=1, background_color='white', colormap='Set2', # "Paired" also looks nice
                            collocations=False, stopwords=None).generate(output_joined)
        # Plot
        plot_cloud(wordcloudName)
        #plt.title(key)
        plt.savefig(os.path.join(os.path.dirname(__file__) ,"..", "data", "out", "wordcloud-" + key + ".pdf"), dpi=600)
    else:
        import collections
        output_list = [n.strip().replace(' 6', '6') for n in output_list]
        counter=collections.Counter(output_list)
        print(counter)
        wordcloudNum = WordCloud(width=800, height=400, random_state=1, background_color='white', colormap='Set2').generate_from_frequencies(frequencies=counter)
        plot_cloud(wordcloudNum)
        plt.savefig(os.path.join(os.path.dirname(__file__) ,"..", "data", "out", "wordcloud-" + key + ".pdf"), dpi=600)


now = time.time()
print(f"duration:{now - start}")

#plt.show()

exit()
############################################
# Only data extraction until here, then continue with script from interactive-contact-class


# vectorize functions to apply them on each array element
v_clean_name = np.vectorize(clean_name)
v_stemmer = np.vectorize(stemmer)
v_lemmatizer = np.vectorize(lemmatizer)

clean_skill_names = v_clean_name(skill_names)
lemma_skill_names = v_lemmatizer(clean_skill_names)

all_skill_names = split_names_into_words(lemma_skill_names)

plot_file_path = "../../../papers/2021-interactive-contact-class-paper/figures/user_study_round_1.pdf"
plot_file_path_single_figs = "../../../papers/2021-interactive-contact-class-paper/figures/user_study_round_1_"

ordered_skill_names, frequency_skill_names, fig, single_figs = process_skill_names(subplot_titles, all_skill_names,
                                                                                   rows=2, cols=4)

with open('../data/skill_names.txt', 'w') as f:
    f.writelines(ordered_skill_names.__str__())
with open('../data/common_skill_names.txt', 'w') as f:
    f.writelines([names[0] for names in ordered_skill_names].__str__())

data = (ordered_skill_names, frequency_skill_names)
pickle.dump(data, open("../data/data.pickle", 'wb'))

fig.update_layout(showlegend=False,
                  autosize=False,
                  width=1500,
                  height=450,
                  margin=dict(
                      l=0,
                      r=0,
                      b=0,
                      t=20,
                      pad=0),
                  font_size=13,
                  font_family="Times New Roman",
                  )
# fig.write_image(plot_file_path)
fig.show()

for f, t in zip(single_figs, subplot_titles):
    # f.savefig(plot_file_path_single_figs + t + '.pdf')
    f.show()

plt.show()
