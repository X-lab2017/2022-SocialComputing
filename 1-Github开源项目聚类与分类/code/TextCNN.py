import torch
import torch.nn as nn

class tcnn(nn.Module):
    def __init__(self, seq_len, vocab_size, output_dim, dropout = 0.5):
        super().__init__()
        
        self.embedding = nn.Embedding(vocab_size, 128)
        self.linear1 = nn.Linear(vocab_size, 128)
        self.conv = nn.Sequential(
            nn.Conv2d(1, 128, (2, 128)),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.MaxPool2d((seq_len - 1, 1))
        )
        self.rnn = nn.LSTM(128, 256, 2, batch_first = True, bidirectional = True)
        self.linear2 = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(512, output_dim)
        ) 
        self.dropout = nn.Dropout(dropout)
        
        nn.init.kaiming_normal_(self.embedding.weight)
    
    def forward(self, x):
        
        if len(x.shape) < 3:
            x = self.embedding(x)
        # 64, 102, 10000
        else:
            x = self.linear1(x) 
        # 64, 102, 128
        # x = x.unsqueeze(1) # 64, 1, 102, 128
        # x = self.conv(x) # 64, 128, 2, 1
        x = self.rnn(x)[0][:, -1, :]
        # x = x.view(x.size(0), -1) # 64, 128
        x = self.dropout(x)
        x = self.linear2(x) # 64, 20
        return x