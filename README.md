# Numeric representation of protein sequences

Numeric representations of protein sequences is a requirement to apply machine learning algorithms.

There are different strategies and methodologies available to solve this problem. However, there are no a consensus 
concerning the specific strategy to employee. In this repository, we implement and leave enabled different methods to encoding 
sequences, considering classical strategies and more recent advances using protein language techniques.

## Available strategies

We have collected different strategies to encoding protein sequences, in particular using classical One Hot strategies, apply physicochemical 
properties, using Fast Fourier transform, and different Natural Language proccesing tools.

### One hot encoding

One hot is a binarization strategies that encoding each residue as a binary vector of 0 and 1 which size depends on
the vocabulary size. We have to modalities: Normal execution and parallel execution. 

### Physicochemical properties

### Signal transformation

### Spatial transformation

### Natural Language Processing

#### Tape-Embedding

We have available unirep methods from [Tape-Embedding tools](https://github.com/songlab-cal/tape)

Example of use 

```
    python encoding_tape.py param1 param2
```

- param1: Is the input file in fasta format
- param2: Is the path to save output values
- The script create two outputs:
  - A npz file with the result of the encoding
  - A .csv file with the result of encoding


