from .template import CrowdModel
import numpy as np
import pymc3 as pm


def sigmoid(x):
    return np.piecewise(
        x,
        [x > 0],
        [
            lambda i: 1 / (1 + np.exp(-i)),
            lambda i: np.exp(i) / (1 + np.exp(i)),
        ],
    )


class DS_mc(CrowdModel):
    def __init__(self, answers, n_classes, **kwargs):
        super().__init__(answers)
        self.n_classes = n_classes
        self.n_workers = len(self.converter.table_worker)
        self.n_task = len(self.answers)

    def init_list(self):
        jj = list()  # annotator IDs
        ii = list()  # item IDs
        yy = list()  # response

        y_init = np.zeros(self.n_task, dtype=np.int64)

        for task, all_response in self.answers.items():
            all_ = []
            for worker, ans in all_response.items():
                ii.append(task)
                jj.append(worker)
                yy.append(ans)
                all_.append(ans)
            y_init[task] = np.bincount(np.array(all_)).argmax()

        self.y_init = y_init
        self.ii = ii
        self.jj = jj
        self.yy = yy

    def run(self, nsample=5000):
        assert nsample > 1000, "Number of samples must be > 1000"
        self.init_list()
        # priors
        K = self.n_classes
        nt, nw = self.n_task, self.n_workers
        beta = np.ones((K, K)) + np.diag(np.ones(K))
        alpha = np.ones(K)

        # define model
        model = pm.Model()

        with model:
            pi = pm.Dirichlet("pi", a=alpha, shape=K)
            theta = pm.Dirichlet("theta", a=beta, shape=(nw, K, K))
            z = pm.Categorical("z", p=pi, shape=nt, testval=self.y_init)
            y_obs = pm.Categorical(
                "y_obs", p=theta[self.jj, z[self.ii]], observed=self.yy
            )

        # run model
        with model:
            step1 = pm.Metropolis(vars=[pi, theta])
            step2 = pm.CategoricalGibbsMetropolis(vars=[z])
            trace = pm.sample(nsample, step=[step1, step2], progressbar=True)
        self.trace = trace
        self.model = model

    def get_probas(self):
        z = self.trace["z"][-1000:, :]

        z_hat = np.zeros((self.n_task, self.n_classes))
        for i in range(self.n_task):
            unique, counts = np.unique(z[:, i], return_counts=True)
            z_hat[i, unique] = counts / sum(counts)
        self.baseline = z_hat
        return self.baseline[self.converter.inv_task]

    def get_answers(self):
        return np.vectorize(self.converter.inv_labels.get)(
            np.argmax(self.get_probas(), axis=1)
        )
