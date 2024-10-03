import torch
print(torch.cuda.is_available())
import torch.nn as nn
import torch.optim as optim

# Define the model classes as before
class SpatialTransformer(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(SpatialTransformer, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1)
        self.bn = nn.BatchNorm2d(out_channels)
        
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = F.relu(x)
        return x

class TemporalTransformer(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(TemporalTransformer, self).__init__()
        self.conv = nn.Conv3d(in_channels, out_channels, kernel_size=(3, 1, 1), stride=(1, 1, 1), padding=(1, 0, 0))
        self.bn = nn.BatchNorm3d(out_channels)
        
    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = F.relu(x)
        return x

class VideoTransformer(nn.Module):
    def __init__(self, in_channels, spatial_out_channels, temporal_out_channels, num_classes):
        super(VideoTransformer, self).__init__()
        self.spatial_transformer = SpatialTransformer(in_channels, spatial_out_channels)
        self.temporal_transformer = TemporalTransformer(spatial_out_channels, temporal_out_channels)
        self.fc = nn.Linear(temporal_out_channels, num_classes)
        
    def forward(self, x):
        x = self.spatial_transformer(x)  # Apply spatial transformer
        x = x.permute(0, 2, 1, 3, 4).contiguous()  # Rearrange dimensions for temporal transformer
        x = self.temporal_transformer(x)  # Apply temporal transformer
        x = x.mean(dim=1)  # Global average pooling over the temporal dimension
        x = self.fc(x)  # Final fully connected layer
        return x

# Create a sample model
model = VideoTransformer(in_channels=3, spatial_out_channels=64, temporal_out_channels=128, num_classes=10)

# Loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Sample input (batch_size, channels, time, height, width)
inputs = torch.randn(8, 3, 10, 64, 64)  # Example input: batch of 8 videos, each with 3 channels, 10 frames, 64x64 resolution
labels = torch.randint(0, 10, (8,))  # Example labels: batch of 8 with classes in range [0, 9]

# Training step
model.train()  # Set model to training mode

# Forward pass
outputs = model(inputs)

# Compute loss
loss = criterion(outputs, labels)

# Backward pass
optimizer.zero_grad()  # Zero the gradients
loss.backward()  # Backpropagation, compute gradients

# Update weights
optimizer.step()  # Optimizer step, update model weights

print(f'Loss: {loss.item()}')  # Print loss
