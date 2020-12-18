

import pandas as pd
import ast
from xml.dom import minidom
from statistics import median

def label(data):
    data_views = data[['views']]
    data_views_ls = data_views.values.tolist()
    data_views_ls = [i[0] for i in data_views_ls]
    med = median(data_views_ls)
    labels = []
    for i in data_views_ls:
        if (i >= med):
            labels.append(1)
        else:
            labels.append(-1)
    return labels
