"""
Main code by Yudian Zheng adapted for our work
method by Demartini et al 2012
"""
from .template import CrowdModel
import numpy as np


def gete2wlandw2el(data):
    e2wl = {}
    w2el = {}
    label_set = []

    for example, answers in data.items():
        for worker, label in answers.items():
            if example not in e2wl:
                e2wl[example] = []
            e2wl[example].append([worker, label])
            if worker not in w2el:
                w2el[worker] = []
            w2el[worker].append([example, label])
            if label not in label_set:
                label_set.append(label)
    return e2wl, w2el, label_set


class ZC(CrowdModel):
    def __init__(self, answers):
        super().__init__(answers)
        self.n_workers = len(self.converter.table_worker)
        self.n_task = len(self.answers)
        e2wl, w2el, label_set = gete2wlandw2el(answers)

        self.e2wl = e2wl
        self.w2el = w2el
        self.label_set = label_set
        self.n_classes = len(label_set)

    def InitPj(self):
        l2pd = {}
        for label in self.label_set:
            l2pd[label] = 1.0 / len(self.label_set)
        return l2pd

    def InitWM(self, workers):
        wm = {}

        if workers == {}:
            workers = self.w2el.keys()
            for worker in workers:
                wm[worker] = 0.8
        else:
            for worker in workers:
                if worker not in wm:  # workers --> wm
                    wm[worker] = 0.8
                else:
                    wm[worker] = workers[worker]

        return wm

    # E-step
    def ComputeTij(self, e2wl, l2pd, wm):
        e2lpd = {}
        for e, workerlabels in e2wl.items():
            e2lpd[e] = {}
            for label in self.label_set:
                e2lpd[e][label] = 1.0  # l2pd[label]

            for worker, label in workerlabels:
                for candlabel in self.label_set:
                    if label == candlabel:
                        e2lpd[e][candlabel] *= wm[worker]
                    else:
                        e2lpd[e][candlabel] *= (
                            (1 - wm[worker]) * 1.0 / (len(self.label_set) - 1)
                        )

            sums = 0
            for label in self.label_set:
                sums += e2lpd[e][label]

            if sums == 0:
                for label in self.label_set:
                    e2lpd[e][label] = 1.0 / self.len(self.label_set)
            else:
                for label in self.label_set:
                    e2lpd[e][label] = e2lpd[e][label] * 1.0 / sums

        # print e2lpd
        return e2lpd

    # M-step
    def ComputePj(self, e2lpd):
        l2pd = {}

        for label in self.label_set:
            l2pd[label] = 0
        for e in e2lpd:
            for label in e2lpd[e]:
                l2pd[label] += e2lpd[e][label]

        for label in self.label_set:
            l2pd[label] = l2pd[label] * 1.0 / len(e2lpd)

        return l2pd

    def ComputeWM(self, w2el, e2lpd):
        wm = {}
        for worker, examplelabels in w2el.items():
            wm[worker] = 0.0
            for e, label in examplelabels:
                wm[worker] += e2lpd[e][label] * 1.0 / len(examplelabels)

        return wm

    def run(self, maxiter=100):
        # wm     worker_to_confusion_matrix = {}
        # e2pd   example_to_softlabel = {}
        # l2pd   label_to_priority_probability = {}
        workers = {}
        l2pd = self.InitPj()
        wm = self.InitWM(workers)
        while maxiter > 0:
            # E-step
            e2lpd = self.ComputeTij(self.e2wl, {}, wm)

            # M-step
            # l2pd = self.ComputePj(e2lpd)
            wm = self.ComputeWM(self.w2el, e2lpd)

            # print l2pd,wm

            maxiter -= 1

        self.e2lpd, self.wm = e2lpd, wm

    def get_answers(self):
        return np.vectorize(self.converter.inv_labels.get)(
            np.argmax(self.get_probas(), axis=1)
        )

    def get_probas(self):
        probas = np.zeros((self.n_task, self.n_classes))
        for i, ans in self.e2lpd.items():
            ans = dict(sorted(ans.items()))
            probas[i] = np.array(list(ans.values()))
        return probas[self.converter.inv_task]
