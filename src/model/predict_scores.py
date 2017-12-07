import csv
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet, LogisticRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error, accuracy_score, roc_curve, auc
from sklearn.preprocessing import label_binarize
from sklearn.svm import SVR, SVC
from sklearn.neural_network import MLPRegressor
import pickle
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import numpy as np
import scikitplot as skplt

import sys

sys.path.append('../util')

from src.util.featurize_helper import get_data_with_important_features

print('reading data...')
with open('../model/data/featurized.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    featurized_data = list(reader)


def get_data_and_scores(dlist):
    scores = [float(row['score']) for row in dlist]
    data_list = [[float(v) for k, v in row.iteritems() if k != 'score'] for row in dlist]
    return [data_list, scores]


def get_data_and_classes(dlist):
    categories = []
    for row in dlist:
        row['score'] = float(row['score'])
        categories.append(get_activity_class(row['score']))

    data_list = [[float(v) for k, v in row.iteritems() if k != 'score'] for row in dlist]
    return [data_list, categories]


def find_accuracy(gt, pred, threshold=0.15):
    total = len(gt)
    hits = 0
    for i, gtv in enumerate(gt):
        pv = pred[i]
        if abs(gtv - pv) <= threshold:
            hits += 1
    return (float(hits) / float(total)) * 100


def get_activity_class(score):
    if score < 0.5:
        return 0
    return 1


def evaluate_model(model_name, sklearn_model, score_threshold=0.5, accuracy_threshold=0.1):
    print('Evaluation for model_name={}'.format(model_name))
    print('--------------------')
    print('getting data with important features')
    feature_reduced_data = get_data_with_important_features(score_threshold=score_threshold,
                                                            featurized_data=featurized_data)
    print('using {} features'.format(len(feature_reduced_data[0].keys())))
    print('getting training data...')
    train_data, train_scores = get_data_and_scores(feature_reduced_data[:4500])
    print('getting test data...')
    test_data, test_scores = get_data_and_scores(feature_reduced_data[4500:])

    sklearn_model.fit(train_data, train_scores)
    predicted_scores = sklearn_model.predict(test_data)
    print('R2 Score:', r2_score(test_scores, predicted_scores))
    print('Mean Absolute Error:', mean_absolute_error(test_scores, predicted_scores))
    print('Mean Squared Error:', mean_squared_error(test_scores, predicted_scores))
    print('Accuracy:', find_accuracy(test_scores, predicted_scores, accuracy_threshold))
    print('-------------------')

    test_labels = [get_activity_class(s) for s in test_scores]
    predicted_labels = [get_activity_class(s) for s in predicted_scores]

    return sklearn_model


def plot_metrics_curve(model, plot_type, plot_title, train_data, train_labels, test_data, test_labels):
    if plot_type == 'roc':
        plotter = skplt.metrics.plot_roc_curve
    elif plot_type == 'precision_recall':
        plotter = skplt.metrics.plot_precision_recall_curve
    else:
        raise ValueError('plot_title should either be "roc" or "precision_recall"')

    model.fit(train_data, train_labels)

    predicted_labels = model.predict(test_data)
    predicted_proba = model.predict_proba(test_data)

    ax = plt.axes()
    plotter(test_labels, predicted_proba, title=plot_title, curves=('each_class'), ax=ax)
    handles, old_labels = ax.get_legend_handles_labels()
    new_labels = [old_labels[0].replace('class 0', 'low-activity sgRNA prediction'),
                  old_labels[1].replace('class 1', 'low-activity sgRNA prediction')]

    ax.legend(handles, new_labels)
    plt.show()


# evaluate_model('Linear Regression', LinearRegression())
# evaluate_model('Ridge', Ridge(alpha=12))
# evaluate_model('SVM', SVR(C=10.0, epsilon=0.001, kernel='rbf', verbose=True), score_threshold=0.2)
# evaluate_model('Elastic Net', ElasticNet(alpha=5.0, copy_X=True, fit_intercept=True, l1_ratio=0.5, selection='cyclic', normalize=False, positive=False))
# model = evaluate_model('MLPRegressor', MLPRegressor(hidden_layer_sizes=(200,), activation='logistic', solver='adam', verbose=True, random_state=5, max_iter=200))
# pickle.dump(model, open('../model_files/mlp_150_tanh_adam_mi200.pkl', 'wb'))

model = evaluate_model('Random Forest',
                       RandomForestRegressor(n_estimators=150, max_depth=128, random_state=0, verbose=2))
pickle.dump(model, open('../model_files/rf_150_128.pkl', 'wb'))

# print('getting data with important features')
# feature_reduced_data = get_data_with_important_features(score_threshold=0.5, featurized_data=featurized_data)
# print('using {} features'.format(len(feature_reduced_data[0].keys())))
# print('getting training data...')
# train_data, train_labels = get_data_and_classes(feature_reduced_data[:4500])
# print('getting test data...')
# test_data, test_labels = get_data_and_classes(feature_reduced_data[4500:])
#
# plot_metrics_curve(
# 	model=SVC(C=1.0, kernel='rbf', degree=2, verbose=2, probability=True),
# 	plot_type='roc',
# 	plot_title='SVM ROC Curve',
# 	train_data=train_data, train_labels=train_labels,
# 	test_data=test_data, test_labels=test_labels)
#
# plot_metrics_curve(
# 	model=SVC(C=1.0, kernel='rbf', degree=2, verbose=2, probability=True),
# 	plot_type='precision_recall',
# 	plot_title='SVM Precision-Recall Curve',
# 	train_data=train_data, train_labels=train_labels,
# 	test_data=test_data, test_labels=test_labels)
#
# plot_metrics_curve(
# 	model=RandomForestClassifier(n_estimators=150, max_depth=128, random_state=0, verbose=2),
# 	plot_type='roc',
# 	plot_title='Random Forest ROC Curve',
# 	train_data=train_data, train_labels=train_labels,
# 	test_data=test_data, test_labels=test_labels)
#
# plot_metrics_curve(
# 	model=RandomForestClassifier(n_estimators=150, max_depth=128, random_state=0, verbose=2),
# 	plot_type='precision_recall',
# 	plot_title='Random Forest Precision-Recall Curve',
# 	train_data=train_data, train_labels=train_labels,
# 	test_data=test_data, test_labels=test_labels)
