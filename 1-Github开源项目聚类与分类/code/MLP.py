import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim, dropout = 0.5):
        # assert len(hidden_dims) == 3
        
        super().__init__()
        
        self.w1 = nn.Linear(input_dim, hidden_dims[0])
        self.w2 = nn.Linear(hidden_dims[0], hidden_dims[1])
        self.w3 = nn.Linear(hidden_dims[1], hidden_dims[2])
        self.w4 = nn.Linear(hidden_dims[2], output_dim)
        
        self.dropout = nn.Dropout(dropout)
        self.relu = nn.ReLU()
        
        nn.init.kaiming_normal_(self.w1.weight)
        nn.init.kaiming_normal_(self.w2.weight)
        nn.init.kaiming_normal_(self.w3.weight)
        nn.init.kaiming_normal_(self.w4.weight)
        
    def forward(self, X):

        l1 = self.relu(self.dropout(self.w1(X)))
        l2 = self.relu(self.dropout(self.w2(l1)))
        l3 = self.relu(self.dropout(self.w3(l2)))
        out = self.w4(l3)
        
        return out