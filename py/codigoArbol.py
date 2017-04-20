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

def maximovalor(arr):
    maximo = 0
    for i in range(len(arr)):
        if(arr[i] > arr[maximo]):
            maximo = i
    return maximo

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
            a = maximovalor(tree_.value[node][0])
            print "{}return {};".format(indent, int(a + 1))
        
    recurse(0, 1)


feature_names=[ 'gyro_alpha_avg','gyro_beta_avg','gyro_gamma_avg','accel_x_avg','accel_y_avg','accel_z_avg','gyro_alpha_min','gyro_beta_min','gyro_gamma_min','accel_x_min','accel_y_min','accel_z_min','gyro_alpha_max','gyro_beta_max','gyro_gamma_max','accel_x_max','accel_y_max','accel_z_max','gyro_alpha_std','gyro_beta_std','gyro_gamma_std','accel_x_std','accel_y_std','accel_z_std','xy_cor','xz_cor','yz_cor','x_fft','y_fft','z_fft','gyro_alpha_med','gyro_beta_med','gyro_gamma_med','accel_x_med','accel_y_med','accel_z_med']

tree_to_code(clf,feature_names)