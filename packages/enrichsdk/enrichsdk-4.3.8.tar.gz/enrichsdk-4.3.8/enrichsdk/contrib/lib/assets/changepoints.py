import math
import ruptures as rpt
from collections import defaultdict
import matplotlib.pyplot as plt

plt.style.use('seaborn-darkgrid')


class ScribbleChangePointDetector(object):

    def __init__(self, df, *args, **kwargs):
        """
        default
        """
        # setup defaults
        self.rpt_model      = 'rbf'
        self.rpt_penalty    = 1
        self.rpt_jump       = 1
        self.rpt_minsize    = 3
        self.rpt_default_hybrid_model = 'maxvote'

        # set the dataframe
        self.data = df

        # init the change points
        self.changepoints = None

        # init the visualization
        self.viz = None

        super().__init__(*args, **kwargs)

    def detect_changepoints(self, method="hybrid"):
        """
        detect change points using the method specified
        """

        if method == "pelt":
            # use the Ruptures changepoint detection method
            self.changepoints = self.detect_changepoints_pelt()
        elif method == "hybrid":
            # use the Ruptures changepoint detection method
            self.changepoints = self.detect_changepoints_hybrid()
        else:
            # we have no other methods available
            pass

        return self.changepoints

    def get_data(self):
        """
        return the data being used
        """
        return self.data

    def get_changepoints(self):
        """
        return the detected changepoints if any
        """
        return self.changepoints


    def detect_changepoints_pelt(self,
                                    model=None,
                                    penalty=None,
                                    jump=None,
                                    min_size=None
                                    ):
        """
        run the change point detector using the Pelt method
        """
        # get the data
        ts = self.data.values

        # set the params
        if model == None:
            model = self.rpt_model
        if penalty == None:
            penalty = self.rpt_penalty
        if jump == None:
            jump = self.rpt_jump
        if min_size == None:
            min_size = self.rpt_minsize

        # fit and find change points
        algo = rpt.Pelt(model=model, jump=jump, min_size=min_size).fit(ts)
        bkps = algo.predict(pen=penalty)

        self.changepoints = bkps

        return self.changepoints

    def detect_changepoints_hybrid(self,
                                    strategy=None,
                                    model=None,
                                    penalty=None,
                                    jump=None,
                                    min_size=None
                                    ):
        """
        run the change point detector using the Hybrid method with one of the following strategies
            strict: all models should agree on the changepoints
            maxvote: a majority of models evaluated should agree on the changepoints (default strategy)
            anyone: all changepoints detected by any model are included
            select: the specified model is run
        """

        # set the params
        if strategy == None:
            strategy = self.rpt_default_hybrid_model

        ## first, run the 3 models
        changepoints = {}
        for m in ['rbf', 'l2', 'l1']:
            changepoints[m] = self.detect_changepoints_pelt(model=m)

        ## then, run the hybrid strategy
        if strategy == 'strict':
            allpoints = []
            for cp in changepoints:
                allpoints.append(changepoints[cp])
            common_bkps = sorted(list(set.intersection(*map(set,allpoints))))
        elif strategy == 'maxvote':
            allpoints = defaultdict(int)
            for model, cps in changepoints.items():
                for cp in cps:
                    allpoints[cp] += 1
            threshold = math.ceil(len(changepoints)/2)
            common_bkps = [cp for cp in allpoints if allpoints[cp]>=threshold]
        elif strategy == 'anyone':
            allpoints = []
            for model, cps in changepoints.items():
                allpoints += cps
            common_bkps = sorted(list(set(allpoints)))
        elif strategy == 'select':
            common_bkps = changepoints[model]
        else:
            # no strategy specified
            common_bkps = []

        common_bkps = sorted(common_bkps)

        self.changepoints = common_bkps

        return self.changepoints

    def visualize_changepoints(self, data, changepoints, title):
        colors = {
            1: 'red',
            -1: 'blue',
        }
        ts = data.values
        rpt.display(ts, changepoints, figsize=(10, 3))
        sgn = 1
        for p in changepoints[:-1]:
            style = dict(size=10, color=colors[sgn])
            plt.text(p, ts[p]+(sgn),
                     data.index[p].strftime("%-d %B, %Y"),
                     **style)
            sgn *= -1
        plt.subplots_adjust(top=.9)
        plt.title(f"Change Points: {title}")

        # save the image data
        self.viz = plt

        return self.viz
