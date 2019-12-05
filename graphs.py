import matplotlib.pyplot as plot
import numpy as np
import pandas as pd
import random
from operator import itemgetter
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection


def radar_factory(num_vars, frame='circle'):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)

    def draw_poly_patch(self):
        # rotate theta such that the first axis is at the top
        verts = unit_poly_verts(theta + np.pi / 2)
        return plot.Polygon(verts, closed=True, edgecolor='k')

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plot.Circle((0.5, 0.5), 0.5)

    patch_dict = {'polygon': draw_poly_patch, 'circle': draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError('unknown value for `frame`: %s' % frame)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def __init__(self, *args, **kwargs):
            super(RadarAxes, self).__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop('closed', True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == 'circle':
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = 'circle'
            verts = unit_poly_verts(theta + np.pi / 2)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {'polar': spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """Return vertices of polygon for subplot axes.

    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
    return verts

def make_radar_data(counts):
    data = []
    for index, count in enumerate(counts):
        lis = [0 for _ in range(len(counts))]
        lis[index] = count
        lis[index-1] = count / 10
        lis[(index+1)%len(lis)] = count / 10
        data.append(lis)
    return data

def radar(counts, categories):
    data = make_radar_data(counts)
    theta = radar_factory(len(categories))
    fig, ax = plot.subplots(figsize=(9, 9), subplot_kw=dict(projection='radar'))
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)
    colors = [(1,0,0), (1,0.5,0), (1,1,0), (0,1,0), (0,1,1), (0,0,1), (1,0,1), (1,0,0.5), (0,0,0)]
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8])
    for d, color in zip(data, colors):
        ax.plot(theta, d, color=color)
        ax.fill(theta, d, facecolor=color, alpha=0.25)
    ax.set_varlabels(categories)

    plot.show()

    return fig, ax

def scatter(views, replies):
    fig, ax = plot.subplots()

    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_xlabel("Views", fontsize=15)
    ax.set_ylabel("Replies", fontsize=15)
    ax.grid(True)
    ax.scatter(views, replies, alpha=0.5)
    ax.set_xlim((100, 1000000))
    ax.plot([1000, 1000000], [10, 10000], c='red', label="y = x / 100")
    ax.set_ylim((10, 10000))
    ax.legend()
    plot.show()
    #ax.legend().remove()

    return fig, ax

def discrete_bars(results, category_names):
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = [(1,0.2,0.2), (1,0.75,0), (1,1,0.4), (0,0.75,0), (0,0.75,0.75), (0,0,1)]

    fig, ax = plot.subplots(figsize=(11, 50))
    ax.invert_yaxis()
    #ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        ax.barh(labels, widths, left=starts, height=0.5,
                label=colname, color=color)
        xcenters = starts + widths / 2

        #r, g, b, _ = color
        text_color = 'black'#'white' if r * g * b < 0.5 else 'darkgrey'
        if len(results) < 25:
            for y, (x, c) in enumerate(zip(xcenters, widths)):
                prop = round(float(c), 3)
                ax.text(x, y, str(prop) if prop != 0 else "", ha='center', va='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    plot.show()
    return fig, ax

commentFile = pd.read_csv("fullCommentData.csv", quotechar='"', encoding='utf8')
threadFile = pd.read_csv("fullThreadData.csv", quotechar='"', encoding='utf8')

# make chart for proportions of different currencies being accepted
unknown = ['?']
paypal = ['PayPal', 'paypal', 'Paypal', 'Venmo']
bitcoin = ['BTC']
etherium = ['ETH']
litecoin = ['LTC']
other_crypto = ['XRP', 'XMR', 'Skrill', 'Any Crypto']
bank_transfer = ['Bank Transfer']
giftcard = ['Gift card', 'Gift Card']
categories = ["Unknown", "PayPal", "Bitcoin", "Etherium", "Litecoin", "Other Cryptocurrency", "Bank Transfer", "Gift card", "Other"]

cw_counts = [0 for _ in range(9)]
caas_counts = [0 for _ in range(9)]

currency_data = [data.split(", ") for data in list(threadFile['Payment Method'])]
for entry in currency_data[:50]: #cw
    for currency in entry:
        if currency in unknown:
            cw_counts[0] += 1
        elif currency in paypal:
            cw_counts[1] += 1
        elif currency in bitcoin:
            cw_counts[2] += 1
        elif currency in etherium:
            cw_counts[3] += 1
        elif currency in litecoin:
            cw_counts[4] += 1
        elif currency in other_crypto:
            cw_counts[5] += 1
        elif currency in bank_transfer:
            cw_counts[6] += 1
        elif currency in giftcard:
            cw_counts[7] += 1
        else:
            cw_counts[8] += 1

for entry in currency_data[50:]: #caas
    for currency in entry:
        if currency in unknown:
            caas_counts[0] += 1
        elif currency in paypal:
            caas_counts[1] += 1
        elif currency in bitcoin:
            caas_counts[2] += 1
        elif currency in etherium:
            caas_counts[3] += 1
        elif currency in litecoin:
            caas_counts[4] += 1
        elif currency in other_crypto:
            caas_counts[5] += 1
        elif currency in bank_transfer:
            caas_counts[6] += 1
        elif currency in giftcard:
            caas_counts[7] += 1
        else:
            caas_counts[8] += 1

cw_counts = [i / 50 for i in cw_counts]
caas_counts = [i / 50 for i in caas_counts]

radar(cw_counts, categories)
radar(caas_counts, categories)

# make log scaled scatter of views to replies
view_counts = [int(v) for v in list(threadFile['Views']) if v.isdigit()]
reply_counts = [int(r) for r in list(threadFile['Replies']) if r.isdigit()]

scatter(view_counts[:50], reply_counts[:50]) #botnets
scatter(view_counts[50:], reply_counts[50:]) #refunds

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
        if str(trade_marks[i]) != '0':
            cw_threads[id][1] += 1
        elif str(review_marks[i]) == '+':
            cw_threads[id][2] += 1
        elif str(review_marks[i]) == '-':
            cw_threads[id][3] += 1
        elif str(review_marks[i]) != '0':
            cw_threads[id][6] += 1
        elif str(qa_marks[i]) != 0:
            print(f"qa 1: {type(qa_marks[i])} {qa_marks[i]} @ {i}")
            cw_threads[id][4] += 1
        elif str(promo_marks[i]) != '0':
            cw_threads[id][5] += 1
        else:
            cw_threads[id][6] += 1
    else:
        id -= 50
        caas_threads[id][0] += 1  # numComments
        if str(trade_marks[i]) != '0':
            caas_threads[id][1] += 1
        elif str(review_marks[i]) == '+':
            caas_threads[id][2] += 1
        elif str(review_marks[i]) == '-':
            caas_threads[id][3] += 1
        elif str(review_marks[i]) != '0':
            caas_threads[id][6] += 1
        elif str(qa_marks[i]) != '0':
            caas_threads[id][4] += 1
        elif str(promo_marks[i]) != '0':
            caas_threads[id][5] += 1
        else:
            caas_threads[id][6] += 1

cw_threads = sorted([[i / thread[0] for i in thread] for thread in cw_threads], key=itemgetter(1,2,3,4,5,6), reverse=True)
caas_threads = sorted([[i / thread[0] for i in thread] for thread in caas_threads], key=itemgetter(1,2,3,4,5,6), reverse=True)

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
    caas_dict[f'Thread {i+1}'] = thread[1:]

discrete_bars(cw_dict, categories)
sample_keys = list(cw_dict)[random.choice([0, 1, 2])::3]
discrete_bars({k:cw_dict[k] for k in sample_keys}, categories) 
discrete_bars(caas_dict, categories)
sample_keys = list(caas_dict)[random.choice([0, 1, 2])::3]
discrete_bars({k:caas_dict[k] for k in sample_keys}, categories)
