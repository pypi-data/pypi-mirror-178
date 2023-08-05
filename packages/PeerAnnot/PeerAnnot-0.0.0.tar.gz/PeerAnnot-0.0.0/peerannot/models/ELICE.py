from .template import CrowdModel
import numpy as np
from peerannot.helpers.converters import Converter


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class ELICE1(CrowdModel):
    def __init__(self, answers, trappingset, n_classes=2, **kwargs):
        """
        Trapping set must be in the form {task: {worker: answer}} too, with
        worker being anything as this superworker is "the source of knowledge"
        """
        self.n_classes = n_classes
        assert self.n_classes == 2, "ELICE1 is only for binary data \pm 1"
        self.answers = answers
        self.n_task = len(answers)
        self.trappingsetconverter = Converter(trappingset)
        self.trappingset = self.trappingsetconverter.transform()
        self.n_workers = len(self.converter.table_worker)
        self.n_task_trap = len(self.answers)
        self.n_task_trap = len(self.trappingset)

    def get_alphas_betas_trap(self):
        betas = np.zeros(self.n_task_trap)  # difficulty trapping set
        w_labelers = np.zeros(self.n_task_trap)  # nb of workers per trap task
        alphas = np.zeros(self.n_workers)  # labeler ability
        times_answered = np.zeros(self.n_workers)  # dividor
        for task, ans in self.trappingset.items():
            ans = list(ans.values())[0]  # unique ground truth per task
            workerans = self.answers[ans]
            w_labelers[task] += len(ans)
            for w, lab in workerans.items():
                times_answered[w] += 1
                oknotok = ans == lab
                betas[task] += oknotok
                diff = 2 * (oknotok) - 1
                alphas[w] += diff

        betas /= w_labelers
        alphas /= times_answered
        self.alphas = alphas
        self.betas_trap = betas
        self.labelers_trap = w_labelers
        self.times_answered_trap = times_answered

    def get_betas(self):
        betas = np.zeros(self.n_task)  # compute beta
        hl = np.zeros(self.n_task)
        for task, vals in self.answers.items():
            for worker, label in vals.items():
                hl[task] += self.alphas[worker] * label
            hl[task] = np.sign(hl[task] / len(vals))
            for worker, label in vals.items():
                betas[task] += hl[task] == label
        self.betas = betas

    def run(self):
        self.get_alphas_betas_trap()
        self.get_betas()

    def get_answers(self):
        y_hat = np.zeros(self.n_task)
        for task, vals in self.answers.items():
            for worker, label in vals.items():
                y_hat[task] += (
                    sigmoid(self.alphas[worker] * self.betas[task]) * label
                )
            y_hat[task] /= len(vals)
        return np.sign(y_hat)

    def get_probas(self):
        raise NotImplementedError("ELICE1 can not produce soft labels")
