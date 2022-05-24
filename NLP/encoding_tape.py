import torch
import pandas as pd
from tape import ProteinBertModel, TAPETokenizer
import sys

def encode(sequence):
    model = ProteinBertModel.from_pretrained('bert-base')
    tokenizer = TAPETokenizer(vocab='iupac')
    token_ids = torch.tensor([tokenizer.encode(sequence)])
    output = model(token_ids)
    sequence_output = output[0]
    pooled_output = output[1]
    return pooled_output

dataset = pd.read_csv(sys.argv[1])
path_output = sys.argv[2]
columns = ["id"] + ["P_" + str(i) for i in range(768)]
output = pd.DataFrame(columns = columns)
for index, row in dataset.iterrows():
    res = encode(row.sequence)
    embedding = list(res.detach().numpy()[0])
    output.loc[index] = [row.id] + list(res.detach().numpy()[0])    
output.to_csv("tape_embedding.csv", sep=",", index=False)