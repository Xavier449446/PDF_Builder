from matplotlib import pyplot as plt
from io import BytesIO

FONT_FOR_TITLE = {'fontsize': 16}


def pie(data, label, title, auto, explode=None):
    plt.clf()
    file = BytesIO()
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    try:
        wedges, texts, autotexts = ax.pie(data, shadow=True, autopct=auto, explode=explode)
    except ValueError:
        wedges, texts, autotexts = ax.pie(data, shadow=True, autopct=auto, explode=None)
    ax.legend(wedges, label, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title(title, FONT_FOR_TITLE)
    plt.savefig(file, format="png")
    plt.clf()
    return file


def time(data, label, title):
    plt.clf()
    file = BytesIO()
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.bar(label, data, width=0.4)
    ax.set_title(title, FONT_FOR_TITLE)
    plt.savefig(file, format="png")
    plt.clf()
    return file



