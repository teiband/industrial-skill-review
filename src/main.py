#!/usr/bin/env python3.6
import csv
import pickle
import matplotlib.pyplot as plt

from common import *

results_file = "../data/in/Skill-Taxonomy-Review.csv"

with open(results_file, 'r') as f:
    lines = f.readlines()

results = []
for l in csv.reader(lines, quotechar='"', delimiter=',',
                    quoting=csv.QUOTE_ALL, skipinitialspace=True):
    # print(l)
    results.append(l)

results = np.array(results)

# The following cannot handle delimiters in double quotes
# results_1 = np.loadtxt(results_1_file, dtype=str, delimiter=',')

header = results[0:2, :]
results = results[2:, :]

skill_names_raw = results[:, 11]

skill_names_split = [s.split(',') for s in skill_names_raw if s not in ['-', '']] # split by comma
skill_names_flat = [item for sublist in skill_names_split for item in sublist] # flatten list of list
skill_names = [camel_case_split(s) for s in skill_names_flat] # resolve camel case into spaces
skill_names = [n.strip().replace(' ', '_') for n in skill_names] # replace spaces with underscores
skill_names = [s.lower() for s in skill_names] # make all lower case

skill_names_joined = ", ".join(skill_names) # join to single string

# Plot word cloud
# Define a function to plot word cloud
def plot_cloud(wordcloud):
    # Set figure size
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud)
    # No axis details
    plt.axis("off");

# Import package
from wordcloud import WordCloud, STOPWORDS
# Generate word cloud
wordcloud = WordCloud(width = 3000, height = 2000, random_state=1, background_color='salmon', colormap='Pastel1', collocations=False, stopwords=None).generate(skill_names_joined)
# Plot
plot_cloud(wordcloud)
plt.show()

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

ordered_skill_names, frequency_skill_names, fig, single_figs = process_skill_names(subplot_titles, all_skill_names, rows=2, cols=4)

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
#fig.write_image(plot_file_path)
fig.show()

for f, t in zip(single_figs, subplot_titles):
    #f.savefig(plot_file_path_single_figs + t + '.pdf')
    f.show()

plt.show()