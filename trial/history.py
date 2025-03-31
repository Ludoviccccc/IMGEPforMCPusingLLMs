class History:
    def __init__(self, max_size = 100):
        self.max_size = max_size
        self.memory_program = []
        self.memory_signature = {"core1_exec_time":[],
                                 "core2_exec_time":[]}
    def store(self,sample:dict[list]):
        for j in range(len(sample["program"])):
            self.memory_program.append(sample["program"][j])
            self.memory_signature["core1_exec_time"].append(sample["signature"][j]["core1_exec_time"])
            self.memory_signature["core2_exec_time"].append(sample["signature"][j]["core2_exec_time"])
        self.eviction()
        
    def eviction(self):
        if len(self.memory_program)>self.max_size:
            self.memory_program = self.memory_program[-self.max_size:]
            self.memory_signature = self.memory_signature[-self.max_size:]
    def select_closest_code(self,signature: dict)->dict:
        min_distance = 0
        idx = 0
        for j in range(len(self.memory_program)):
            dist = 0
            for k in signature.keys():
                dist += (self.memory_signature[k] - signature[k])**2
            if min_distance:
                if dist<min_distance:
                    min_distance= dist
                    idx = j
            else:
                min_distance = dist
                idx = j
        return {"program": self.memory_program[idx] ,"signature": self.memory_signature[idx]}
    def select_closest_code(self,signature: dict)->dict:
        assert len(self.memory_program)>0, "history empty"
        b = np.transpose([h for h in self.memory_signature.values()])
        a = np.array([a[0] for a in signature.values()])
        idx = np.argmin(np.linalg.norm(a-b, axis=1))
        return {"program": self.memory_program[idx] ,"signature": {"core1_exec_time":self.memory_signature["core1_exec_time"][idx],"core2_exec_time":self.memory_signature["core2_exec_time"][idx]}}
