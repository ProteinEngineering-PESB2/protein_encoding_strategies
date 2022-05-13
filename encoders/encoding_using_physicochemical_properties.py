import pandas as pd
import sys
import numpy as np

def encoding_seq(sequence, encoders, group, allow_residues):
    vector_encoder = []
    sequence = sequence.upper()
    for residue in sequence:
        if residue.upper() in allow_residues:
            df_enc = encoders.loc[encoders['residue'] == residue].reset_index()
            vector_encoder.append(df_enc[group][0])
        else:
            vector_encoder.append(None)
    return vector_encoder

#Get params
dataset = pd.read_csv(sys.argv[1])
properties_values = pd.read_csv(sys.argv[2])
path_export = sys.argv[3]

columns = dataset.columns
columns_filter = [value for value in columns if value not in ['id_seq', 'response']]

allow_residues = [residue for residue in properties_values['residue']]

id_seq = dataset['id_seq']
response_values = dataset['response']

for group in ['Group_0','Group_1','Group_2','Group_3','Group_4','Group_5','Group_6','Group_7']:
    print("Encoding_values using group: ", group)
    matrix_encoding = []
    length_data = []
    for i in range(len(dataset)):
        sequence = dataset['seq'][i].upper()
        encoding_sequence = encoding_seq(sequence, properties_values, group, allow_residues)
        matrix_encoding.append(encoding_sequence)
        length_data.append(len(encoding_sequence))

    print("Apply zero padding")
    max_value = np.max(length_data)

    for i in range(len(matrix_encoding)):
        for j in range(len(matrix_encoding[i]), max_value):
            matrix_encoding[i].append(0)

    print("Exporting_df")
    header = ["p_{}".format(i) for i in range(max_value)]
    df_export = pd.DataFrame(matrix_encoding, columns=header)
    for column in columns_filter:
        df_export[column] = dataset[column]

    df_export['id_sequence'] = id_seq
    df_export['response'] = response_values

    df_export.to_csv("{}{}_properties.csv".format(path_export, group), index=False)