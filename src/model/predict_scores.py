import csv
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor

print('reading data...')
with open('./data/featurized.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    featurized_data = list(reader)

def get_data_with_important_features(score_threshold):
    importance_field_names = ('X', 'MeanDecreaseGini')
    reader = csv.DictReader(open('../../datasets/crisprpred/pone.0181943.s002.csv'))

    feature_importance = list(reader)

    for feature in feature_importance:
        feature['MeanDecreaseGini'] = float(feature['MeanDecreaseGini'])

    sorted_importance = sorted(feature_importance, key=lambda k: k[importance_field_names[1]])
    sorted_importance.reverse()

    important_features = [feature['X'] for feature in sorted_importance if feature['MeanDecreaseGini'] >= score_threshold]
    important_features.append('score')

    dlist = []
    for row in featurized_data:
        new_data = {}
        for feature in important_features:
            new_data[feature] = row[feature]
        dlist.append(new_data)

    return dlist

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

def evaluate_model(model_name, sklearn_model, score_threshold=0.5, accuracy_threshold=0.15):
    print('Evaluation for model_name={}'.format(model_name))
    print('--------------------')
    print('getting data with important features')
    feature_reduced_data = get_data_with_important_features(score_threshold=score_threshold)
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

#evaluate_model('Linear Regression', LinearRegression())
#evaluate_model('Ridge', Ridge(alpha=12))
#evaluate_model('SVM', SVR(C=10.0, epsilon=0.001, kernel='rbf', verbose=True), score_threshold=0.2)
evaluate_model('MLPRegressor', MLPRegressor(hidden_layer_sizes=(150,), activation='tanh', solver='adam', verbose=True, max_iter=200))
