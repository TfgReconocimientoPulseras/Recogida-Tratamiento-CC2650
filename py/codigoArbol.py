#! /usr/bin/python

import numpy as np
import pandas as pd
from numpy import genfromtxt
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import _tree


X = genfromtxt("X_train.csv", delimiter=',')
y = genfromtxt("y_train.csv", delimiter='')

clf = DecisionTreeClassifier(criterion='entropy', max_depth=6, random_state=0)
clf = clf.fit(X, y)

def tree_to_code(tree, feature_names):
    tree_ = tree.tree_
    feature_name = [
        feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
        for i in tree_.feature
    ]
    #print "def tree({}):".format(", ".join(feature_names))

    def recurse(node, depth):
        indent = "  " * depth
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            print "{}if({} <= {})".format(indent, name, threshold)
            recurse(tree_.children_left[node], depth + 1)
            print "{}else //if({} > {})".format(indent, name, threshold)
            recurse(tree_.children_right[node], depth + 1)
        else:
            if tree_.value[node][0][0] > tree_.value[node][0][1]:
                print "{}return {};".format(indent, int(tree.classes_[0]))
            else:
                print "{}return {};".format(indent, int(tree.classes_[1]))
        
    recurse(0, 1)


feature_names=['avg_gyro-alpha', 'avg_gyro-beta', 'avg_gyro-gamma', 'avg_ax', 'avg_ay', 'avg_az', 'min_gyro-alpha', 'min_gyro-beta', 'min_gyro-gamma', 'min_ax', 'min_ay', 'min_az', 'max_gyro-alpha', 'max_gyro-beta', 'max_gyro-gamma', 'max_ax', 'max_ay', 'max_az']

tree_to_code(clf,feature_names)