class RelationProbMerger:
    def __init__(self):
        self.no_rel_prob = 1.0

    def step(self, prob: float):
        self.no_rel_prob *= (1 - prob)

    def finalize(self):
        return 1.0 - self.no_rel_prob
