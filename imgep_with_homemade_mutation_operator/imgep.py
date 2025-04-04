from utils import *
import sys
sys.path.append("../")
from mcpu5 import simulate_dual_core
from join_string import join_strings
import matplotlib.pyplot as plt
import numpy as np
import random

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
            self.memory_signature["core1_exec_time"] = self.memory_signature["core1_exec_time"][-self.max_size:]
            self.memory_signature["core2_exec_time"] = self.memory_signature["core2_exec_time"][-self.max_size:]
    def select_closest_code(self,signature: dict)->dict:
        assert len(self.memory_program)>0, "history empty"
        b = np.transpose([h for h in self.memory_signature.values()])
        a = np.array([a[0] for a in signature.values()])
        idx = np.argmin(np.linalg.norm(a-b, axis=1))
        return {"program": self.memory_program[idx] ,"signature": {"core1_exec_time":self.memory_signature["core1_exec_time"][idx],"core2_exec_time":self.memory_signature["core2_exec_time"][idx]}}
    def representation(self, name="image/history_visual"):
        plt.figure()
        plt.scatter(self.memory_signature["core2_exec_time"],self.memory_signature["core1_exec_time"])
        plt.savefig(name)





class GoalGenerator:
    def __init__(self):
        self.execution_time__min = 4
        self.execution_time__max = 100
    def __call__(self, N = 1)->dict:
        return {"core1_exec_time":np.random.randint(self.execution_time__min, self.execution_time__max, (N,)),
               "core2_exec_time":np.random.randint(self.execution_time__min, self.execution_time__max, (N,))}
class OptimizationPolicy:
    def __init__(self):
        """
        Selects a parameter based on a chosen goal and the history.
        Takes the code corresponding to the closest signature to the desired goal signature
        """
        #self.model = model
        #self.tokenizer = tokenizer
        pass
    def __call__(self,goal:dict[list],H:History):
        closest_code = H.select_closest_code(goal) #most promising sample from the history
        output = self.light_code_mutation(closest_code["program"]) #expansion strategie: small random mutation
        return output
    def light_code_mutation(self,assembly_code:list[str], mutation_rate=0.3):
        mutated_code = assembly_code.copy()
        num_mutations = max(1, int(len(mutated_code) * mutation_rate))
        
        for _ in range(num_mutations):
            mutation_type = random.choice(["insert", "delete", "replace"])
            
            if mutation_type == "insert":
                # Insert a new random instruction at a random position
                new_instr = generate_random_assembly(1)[0]
                pos = random.randint(0, len(mutated_code))
                mutated_code.insert(pos, new_instr)
            
            elif mutation_type == "delete" and len(mutated_code) > 1:
                # Delete a random instruction
                pos = random.randint(0, len(mutated_code) - 1)
                mutated_code.pop(pos)
            
            elif mutation_type == "replace":
                # Replace a random instruction with a new one
                pos = random.randint(0, len(mutated_code) - 1)
                new_instr = generate_random_assembly(1)[0]
                mutated_code[pos] = new_instr
        return mutated_code



class IMGEP:
    def __init__(self,N:int, N_init:int,H:History, G:GoalGenerator, Pi:OptimizationPolicy):
        """
        N: int. The experimental budget
        N_init: int. Number of experiments at random
        H: History. Buffer containing codes and signature pairs
        G: GoalGenerator.
        Pi: OptimizationPolicy.
        """
        #self.model = model
        #self.tokenizer = tokenizer
        self.N = N
        self.H = H
        self.G = G
        self.N_init = N_init
        self.Pi = Pi
    def __call__(self):
        for i in range(self.N):
            if i<self.N_init:
                #Initial random iterations
                #core1_code = make_random_code(self.model, tokenizer=self.tokenizer)
                core1_code = generate_random_assembly(np.random.randint(1,20,1)[0])
            else:
                #break
                #Sample target goal
                goal_code = self.G()
                core1_code = self.Pi(goal_code,self.H)
                 
            core1_exec_time, core2_exec_time = simulate_dual_core(
            core1_code = core1_code,
            core2_code =["MUL R3, R4",
                        "STORE R1, 20",
                        "MOV R5, R6",
                        "LOAD R1, 10",
                        "ADD R1, R2",
                        "MUL R3, R4",])
            self.H.store({"program":[core1_code],
                         "signature": [{"core1_exec_time": core1_exec_time,
                                        "core2_exec_time": core2_exec_time}]})
