import torch
from torch import nn

emb = nn.Embedding(10, 5, padding_idx=0)
word = torch.tensor([[1,2,3,0], [4,5,0,0]])
print(emb(word))