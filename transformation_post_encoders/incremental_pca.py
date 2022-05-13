import pandas as pd
import sys
from joblib import dump
from sklearn.decomposition import IncrementalPCA

print("Read dataset")
dataset = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

print("Process columns")
columns_no_process = [column for column in dataset.columns if "P" != column[0].upper()]
columns_process = [column for column in dataset.columns if "P" == column[0].upper()]

dataset_no_information = dataset[columns_no_process]
dataset_to_process = dataset.drop(columns=columns_no_process)
dataset_to_process = dataset_to_process.fillna(0)#nos aseguramos de que no hayan null o algo por la codificacion

print("Start dataset")
pca = IncrementalPCA()
pca.fit(dataset_to_process)
transform_data = pca.transform(dataset_to_process)

print("Export data")
header = ["p_{}".format(i) for i in range(0, len(transform_data[0]))]
data_to_export = pd.DataFrame(transform_data, columns=header)

for column in columns_no_process:
    data_to_export[column] = dataset_no_information[column]

name_export = path_export+"incremental_pca_dataset.csv"
name_job = path_export+"incremental_pca_job.joblib"
data_to_export.to_csv(name_export, index=False)

print("Export job")
dump(pca, name_job)