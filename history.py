

class History:
    def __init__(self, max_size = 100):
        self.max_size = max_size
        self.memory_program = []
        self.memory_signature = []
    def store(self,sample:dict[list]):
        for j in range(len(sample)):
            self.memory_program.append(sample["program"][j])
            self.memory_signature.append(sample["signature"][j])
        self.eviction()
    def eviction(self):
        if len(self.memory_program)>self.maxsize:
            self.memory_program = self.memory_program[-self.maxsize:]
            self.memory_signature = self.memory_signature[-self.maxsize:]
    def select_closest_code(self,signature: dict)->dict:
        min_distance = 0
        idx = 0
        for j,signature_buffer in enumerate(self.memory_signature):
            dist = 0
            for k in signature_buffer.keys():
                dist += (signature_buffer[k] - signature[k])**2
            if min_distance:
                if dist<min_distance:
                    min_distance= dist
                    idx = j
            else:
                min_distance = dist
                idx = j
        return {"code": self.code_list[idx] ,"signature": self.signature_list[idx]}
