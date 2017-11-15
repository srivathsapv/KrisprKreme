from sklearn.linear_model import Lasso
import csv

with open('./data/featurized.csv', 'rb') as csv_file:
    reader = csv.reader(csv_file)
    csv_raw = list(reader)

attribute_names = csv_raw[0]
data_rows = csv_raw[1:]

lasso = Lasso(alpha=0.3)
