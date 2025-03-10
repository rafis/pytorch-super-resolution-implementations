import torch
import torch.nn as nn
import torch.nn.init as init
import math

class Upconv(nn.Module):
    def __init__(self, upscale_factor):
        super(Upconv, self).__init__()
        self.offset = 7
        self.prelu = nn.LeakyReLU(negative_slope=0.1)
        self.conv1 = nn.Conv2d(1, 16,kernel_size=3,stride=1,padding=1) 
        self.conv2 = nn.Conv2d(16, 32,kernel_size=3,stride=1,padding=1) 
        self.conv3 = nn.Conv2d(32, 64,kernel_size=3,stride=1,padding=1) 
        self.conv4 = nn.Conv2d(64, 128,kernel_size=3,stride=1,padding=1) 
        self.conv5 = nn.Conv2d(128, 128,kernel_size=3,stride=1,padding=1) 
        self.conv6 = nn.Conv2d(128, 256,kernel_size=3,stride=1,padding=1) 
        self.conv7 = nn.ConvTranspose2d(256, 1,kernel_size=4,stride=2,padding=1,bias=False) 
        

        self.criterion = nn.MSELoss()
        #self.criterion = nn.SmoothL1Loss()
        self.optimizer = torch.optim.Adam(self.parameters())
        #self.scheduler = torch.optim.lr_scheduler.MultiStepLR(self.optimizer, milestones=[50, 75, 100], gamma=0.5)


        self._initialize_weights()

    def forward(self, x):
        x = self.prelu(self.conv1(x))
        x = self.prelu(self.conv2(x))
        x = self.prelu(self.conv3(x))
        x = self.prelu(self.conv4(x))
        x = self.prelu(self.conv5(x))
        x = self.prelu(self.conv6(x))
        x = self.conv7(x)
        return x

    def _initialize_weights(self):
        init.normal_(self.conv1.weight, init.calculate_gain('leaky_relu'))
        init.normal_(self.conv2.weight, init.calculate_gain('leaky_relu'))
        init.normal_(self.conv3.weight, init.calculate_gain('leaky_relu'))
        init.normal_(self.conv4.weight, init.calculate_gain('leaky_relu'))
        init.normal_(self.conv5.weight, init.calculate_gain('leaky_relu'))
        init.normal_(self.conv6.weight, init.calculate_gain('leaky_relu'))
        init.normal_(self.conv7.weight)
        
