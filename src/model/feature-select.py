from sklearn.linear_model import Lasso, Ridge
from sklearn.feature_selection import VarianceThreshold
import csv
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import boruta

with open('./data/featurized.csv', 'rb') as csv_file:
    reader = csv.DictReader(csv_file)
    featurized_data = list(reader)

scores = [float(row['score']) for row in featurized_data]

feature_names = featurized_data[0].keys()
data_list = [[float(v) for k, v in row.iteritems() if k != 'score'] for row in featurized_data]

# lasso = Lasso(alpha=0.5)
# lasso.fit(data_list, scores)
# #print(np.unique(lasso.coef_, return_counts=True))
#
# ridge = Ridge(alpha=10.0)
# ridge.fit(data_list, scores)
#
# coeffs = ridge.coef_
# positive_coeffs = [c for c in coeffs if c > 0]
# #print(max(positive_coeffs))
#
# variance_threshold = 0.16
#
# sel = VarianceThreshold(threshold=variance_threshold)
# sel.fit(data_list)
#
# variances = sel.variances_
# important_features = {feature_names[i]: v for i, v in enumerate(variances) if v >= variance_threshold}
# #print(important_features)
#
# rf = RandomForestRegressor()
# rf.fit(data_list, scores)
#
# rf_important_features = {feature_names[i]: v for i, v in enumerate(rf.feature_importances_) if v > 0.16}
#
# print(len(rf_important_features))


print('data aggregation done')
feat_selector = boruta.BorutaPy(RandomForestRegressor(), n_estimators='balanced', verbose=2)
print('feat selector initialization')
print(np.array(data_list).shape)
feat_selector.fit(np.array(data_list), scores)
print('fit')

print(feat_selector.support_)
