class GoalGenerator:
    def __init__(self):
        self.execution_time__min = 4
        self.execution_time__max = 100
    def __call__(self, N = 1)->dict:
        return {"core1_exec_time":np.random.randint(self.execution_time__min, self.execution_time__max, (N,)),
               "core2_exec_time":np.random.randint(self.execution_time__min, self.execution_time__max, (N,))}
