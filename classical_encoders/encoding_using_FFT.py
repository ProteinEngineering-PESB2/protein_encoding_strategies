import pandas as pd
import sys
from scipy.fft import fft
import numpy as np

def apply_FFT(row, number_sample):
    T = 1.0 / float(number_sample)
    x = np.linspace(0.0, number_sample * T, number_sample)
    yf = fft(row)
    #xf = np.linspace(0.0, 1.0 / (2.0 * T), number_sample)
    xf = np.linspace(0.0, 1.0 / (2.0 * T), number_sample // 2)
    #matrix_encoding.append(np.abs(yf[0:number_sample // 2]))
    yf = np.abs(yf[0:number_sample // 2])
    #yf = np.abs(yf[0:number_sample])
    return xf, yf

print("Get param inputs")
dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]
suffix_output = sys.argv[3]

print("Start encoding using FFT")
matrix_encoding = []
matrix_domain = []
columns_post = [value for value in dataset.columns if "p_" not in value]
index_column = [value for value in dataset.columns if "p_" in value]

for i in range(len(dataset)):
    row = [dataset[key][i] for key in index_column]
    domain, encoding = apply_FFT(row, len(row))
    matrix_encoding.append(encoding)
    matrix_domain.append(domain)

print("Export dataset")
header = ["p_{}".format(i) for i in range(len(matrix_encoding[0]))]

df_export = pd.DataFrame(matrix_encoding, columns=header)
domain_export = pd.DataFrame(matrix_domain, columns=header)

for column in columns_post:
    df_export[column] = dataset[column]

df_export.to_csv("{}{}_fft_encoding.csv".format(path_output, suffix_output), index=False)
domain_export.to_csv("{}{}_fft_domain.csv".format(path_output, suffix_output), index=False)