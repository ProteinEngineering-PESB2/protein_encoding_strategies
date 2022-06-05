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
    data_load = np.load("{}encoding_data.npz".format(path_export))
    print(data_load)
else:
    print("Error with encoder, check the input dataset")
