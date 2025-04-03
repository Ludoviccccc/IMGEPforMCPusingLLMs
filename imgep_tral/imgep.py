from model import make_model
from utils import *
from mcpu5 import simulate_dual_core
from join_string import join_strings
import matplotlib.pyplot as plt
import numpy as np

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
    def __init__(self,model, tokenizer):
        """
        Selects a parameter based on a chosen goal and the history.
        Takes the code corresponding to the closest signature to the desired goal signature
        """
        self.model = model
        self.tokenizer = tokenizer
    def __call__(self,goal:dict[list],H:History):
        closest_code = H.select_closest_code(goal) #most promising sample from the history
        output = self.light_code_mutation(closest_code["program"]) #expansion strategie: small random mutation
        return output
    def light_code_mutation(self,program:list[str]):
        messages = [
        {"from": "human", "value": f"""I have a cpu simulator with registers R1 up to R10, and that takes assembly instructions STORE, LOAD, ADD, MUL as input. \n
        Here is an example of a list of instructions in this language:
        \n DIV R5, R6\n SUB R7, R8 \n LOAD R9, 30\nADD R9, R10\n
        
        
        A mutation of a list of instructions consists in inserting, deleting or replacing a few instruction in program. For instance, here is a mutation of the list above. I added a the instruction LOAD in the fist line and I have replaced the last instruction by an instruction STORE.
        
        
        \nLOAD R4, 30\n DIV R5, R6\n SUB R7, R8 \n LOAD R9, 30\nSTORE R1, 20\n

        Note that arithmetic operators take only two operands. For instance: "MUL R3, R2, R1" is not valid and "MUL R2, R1" is valid.
        
        Please, insert, delete or replace a few instructions of the program below.
            Don't write python code. Your response has to contain only the mutated list of assembly instructions inside triple backticks with no more explanations.
        {join_strings(program)}
            """},
        ]
        return message2code(messages, self.model, self.tokenizer)



class IMGEP:
    def __init__(self,model,tokenizer,N:int, N_init:int,H:History, G:GoalGenerator, Pi:OptimizationPolicy):
        """
        model: llm
        N: int. The experimental budget
        N_init: int. Number of experiments at random
        H: History. Buffer containing codes and signature pairs
        G: GoalGenerator.
        Pi: OptimizationPolicy.
        """
        self.model = model
        self.tokenizer = tokenizer
        self.N = N
        self.H = H
        self.G = G
        self.N_init = N_init
        self.Pi = Pi
    def __call__(self):
        for i in range(self.N):
            if i<self.N_init:
                #Initial random iterations
                core1_code = make_random_code(self.model, tokenizer=self.tokenizer)
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
