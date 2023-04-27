import torch
from lightning import LightningDataModule


class MyDataModule(LightningDataModule):
    def __init__(self):
        super().__init__()
        self.data = torch.rand(100, 32, 28, 28)
        self.save_hyperparameters(logger=False)
        print(self.hparams)
        
        
if __name__ == "__main__":
    _ = MyDataModule()