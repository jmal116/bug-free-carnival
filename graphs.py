import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import random
from operator import itemgetter

def discrete_bars(results, category_names):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plot.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plot.subplots(figsize=(11, 50))
    ax.invert_yaxis()
    #ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        #xcenters = starts + widths / 2

        #r, g, b, _ = color
        #text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        #for y, (x, c) in enumerate(zip(xcenters, widths)):
            #ax.text(x, y, str(int(c)), ha='center', va='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax

commentFile = pd.read_csv("fullCommentData.csv", quotechar='"', encoding='utf8')
threadFile = pd.read_csv("fullThreadData.csv", quotechar='"', encoding='utf8')

# make log scaled scatter of views to replies


# Discrete bar chart of comment categorization
categories = ['Trade', 'Positive Review', 'Negative Review', 'Q&A', 'Self-Promotion', 'Other']

thread_ids = commentFile['Thread ID']
# print(thread_ids)
# input()
trade_marks = commentFile['Trade']
# print(trade_marks)
# input()
review_marks = commentFile['Review']
# print(review_marks)
# input()
qa_marks = commentFile['Q&A']
# print(qa_marks)
# input()
promo_marks = commentFile['Self-Promotion']
# print(promo_marks)
# input()

cw_threads = [[0 for i in range(7)] for j in range(50)]
caas_threads = [[0 for i in range(7)] for j in range(50)]

i = 0
for i, id in enumerate(thread_ids):
    if id < 50:
        cw_threads[id][0] += 1
        if trade_marks[i] != 0:
            cw_threads[id][1] += 1
        elif review_marks[i] == '+':
            cw_threads[id][2] += 1
        elif review_marks[i] == '-':
            cw_threads[id][3] += 1
        elif review_marks[i] != '0':
            print(review_marks[i])
            cw_threads[id][6] += 1
        elif qa_marks[i] != 0:
            cw_threads[id][4] += 1
        elif promo_marks[i] != 0:
            cw_threads[id][5] += 1
        else:
            cw_threads[id][6] += 1
    else:
        id -= 50
        caas_threads[id][0] += 1  # numComments
        if trade_marks[i] != 0:
            caas_threads[id][1] += 1
        elif review_marks[i] == '+':
            caas_threads[id][2] += 1
        elif review_marks[i] == '-':
            caas_threads[id][3] += 1
        elif review_marks[i] != '0':
            caas_threads[id][6] += 1
        elif qa_marks[i] != 0:
            caas_threads[id][4] += 1
        elif promo_marks[i] != 0:
            caas_threads[id][5] += 1
        else:
            caas_threads[id][6] += 1

cw_threads = sorted([[i / thread[0] for i in thread] for thread in cw_threads], key=itemgetter(1,2,3,4,5,6), reverse=True)
caas_threads = sorted([[i / thread[0] for i in thread] for thread in caas_threads], key=itemgetter(1,2,3,4,5,6), reverse=True)
print([(i[1], i[2]) for i in caas_threads])

cw_dict = {}
caas_dict = {}

# print(cw_threads)
# print(caas_threads)
for i, thread in enumerate(cw_threads):
    # print(thread)
    #thread = [i / thread[0] for i in thread]
    # print(thread)
    cw_dict[f'Thread {i+1}'] = thread[1:]
    # print(cw_dict[f'Thread {i+1}'])
# print(cw_dict)

for i, thread in enumerate(caas_threads):
    #thread = [i / thread[0] for i in thread]
    caas_dict[f'Thread {i+51}'] = thread[1:]

# discrete_bars(cw_dict, categories)
# plot.show()
# discrete_bars(caas_dict, categories)
# plot.show()
# sample_keys = list(caas_dict)[random.choice([0,1,2,3,4])::3]
# discrete_bars({k:caas_dict[k] for k in sample_keys}, categories)
# plot.show()
