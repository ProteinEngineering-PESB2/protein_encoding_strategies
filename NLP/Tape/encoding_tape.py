import pandas as pd
import numpy as np
import sys
import os

#command line
fasta_doc = sys.argv[1]
path_export = sys.argv[2]

command = "tape-embed unirep {} {}encoding_data.npz babbler-1900 --tokenizer unirep".format(fasta_doc, path_export)
os.system(command)

#check if the output exist
doc_dir = os.listdir(path_export)
is_exist = False

for element in doc_dir:
    if "encoding_data" in element:
        is_exist=True
        break

#processing depending of the response
if is_exist:
    print("Processing dataset")
    data_load = np.load("{}encoding_data.npz".format(path_export),allow_pickle=True)
    matrix_data = []
    for value in list(data_load.keys()):
        data = data_load[value]
        values = dict(enumerate(data.flatten(), 1))
        array_data = [element for element in values[1]['avg']]
        array_data.insert(0, value)
        matrix_data.append(array_data)

    print("Exporting data")
    header = ["p_{}".format(i+1) for i in range(1900)]
    header.insert(0, "id_seq")
    df_data = pd.DataFrame(matrix_data, columns=header)
    df_data.to_csv("{}export_data_encoding.csv".format(path_export), index=False)
else:
    print("Error with encoder, check the input dataset")
