from __future__ import division, print_function

import numpy as np


def hist(data, width=20):
    counts, values = np.histogram(data)
    max_count = counts.max()

    for (count, value) in zip(counts, values):
        scaled = int(round((count / max_count) * width))
        print('%5.2f (%5d):' % (value, count), 'X'*scaled)

def sql_hist(table, column, where=''):
    """
    Queries a table, selecting the column and count of the values in that column. Generates
    a histogram plot of that data for display in a jupyter notebook.
    """

    # this depends on the type of table we're looking at, mysql, postgres, etc...
    # might want to template these queries
    sql = """
    SELECT something FROM %(table)s
    %(where)s
    """
    pass

def sql_scatter(table, x_col, y_col, coloring_dimension=None, where=''):
    """
    Queries a table for data in x_col and y_col, then displays them (optionally colored by
    coloring_dimension) onto a scatterplot.
    """
    pass
