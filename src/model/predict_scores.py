import csv
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

import sys
sys.path.append('../util')

from featurize_helper import get_data_with_important_features

print('reading data...')
with open('./data/featurized.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    featurized_data = list(reader)

def get_data_and_scores(dlist):
    scores = [float(row['score']) for row in dlist]
    feature_names = featurized_data[0].keys()
    data_list = [[ float(v) for k, v in row.iteritems() if k != 'score'] for row in dlist]
    return [data_list, scores]

def find_accuracy(gt, pred, threshold=0.15):
    total = len(gt)
    hits = 0
    for i,gtv in enumerate(gt):
        pv = pred[i]
        if abs(gtv - pv) <= threshold:
            hits += 1
    return (float(hits)/float(total)) * 100

def evaluate_model(model_name, sklearn_model, score_threshold=0.5, accuracy_threshold=0.1):
    print('Evaluation for model_name={}'.format(model_name))
    print('--------------------')
    print('getting data with important features')
    feature_reduced_data = get_data_with_important_features(score_threshold=score_threshold, featurized_data=featurized_data)
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

    return sklearn_model

#evaluate_model('Linear Regression', LinearRegression())
#evaluate_model('Ridge', Ridge(alpha=12))
#evaluate_model('SVM', SVR(C=10.0, epsilon=0.001, kernel='rbf', verbose=True), score_threshold=0.2)
#evaluate_model('Elastic Net', ElasticNet(alpha=5.0, copy_X=True, fit_intercept=True, l1_ratio=0.5, selection='cyclic', normalize=False, positive=False))
#model = evaluate_model('MLPRegressor', MLPRegressor(hidden_layer_sizes=(200,), activation='logistic', solver='adam', verbose=True, random_state=5, max_iter=200))
model = evaluate_model('Random Forest', RandomForestRegressor(n_estimators=150, max_depth=128, random_state=0, verbose=2))

#pickle.dump(model, open('../model_files/mlp_150_tanh_adam_mi200.pkl', 'wb'))
pickle.dump(model, open('../model_files/rf_150_128.pkl', 'wb'))
