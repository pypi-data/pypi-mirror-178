from .template import CrowdModel
import torch
import torch.optim as opt
from tqdm import tqdm
import numpy as np


class Rasch(CrowdModel):
    def __init__(self, answers, n_classes, **kwargs):
        super().__init__(answers)
        self.n_classes = n_classes
        self.n_workers = len(self.converter.table_worker)
        self.n_task = len(self.answers)
        assert self.n_classes == 2, "Rasch model only supports binary answers"
        self.crowd_matrix()

    def crowd_matrix(self):
        X = np.zeros((self.n_task, self.n_workers))
        for task, ans in self.answers.items():
            for worker, lab in ans.items():
                X[task, worker] = lab
        self.X = X

    def run(self, lr=0.1, n_epoch=1000, device="auto"):
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            assert (
                device.startswith("cuda") or device == "cpu"
            ), "device must be cuda (specific or not) or cpu"
            device = device
        self.crowd_matrix()
        optimizer = opt.SGD(lr=lr)
        alpha = torch.zeros((self.n_task, 1), device=device)
        delta = torch.zeros((1, self.n_workers), device=device)
        for t in tqdm(range(n_epoch), total=n_epoch, desc="Epoch"):
            optimizer.zero_grad()
            nll = -torch.sum(
                self.X * torch.log(torch.sigmoid(alpha - delta))
                + (1 - self.X) * torch.log(1 - torch.sigmoid(alpha - delta))
            )
            nll.backward()
            optimizer.step()
        self.alpha = alpha.detach().cpu().numpy()
        self.delta = delta.detach().cpu().numpy()

    def get_probas(self):
        raise ValueError("Rasch model does not estimate probabilities")

    def get_answers(self):
        raise ValueError("Rasch model does not estimate ground truths")
