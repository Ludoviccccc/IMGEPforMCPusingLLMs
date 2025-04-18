# Simulator MCPU 💻

I manipulate a code obtained with gpt that simulates a dual core processor. See folder `prompt`.    
Only a few assembly instructions are availble, the ones playing a role in interferences. These are momery instructions (`LOAD,STORE, MOV`) and arithmetic operations (`MUL, DIV, SUB, ADD`).
Although it is not so realistic, each instruction has a default execution time in cycles.
```python
instruction_times = {
        "LOAD": 2, "STORE": 2, "ADD": 1, "SUB": 1, 
        "MUL": 3, "DIV": 4, "MOV": 1  
    }
```
Implementation Plan:

* Simulate Memory Contention – If both cores execute a LOAD or STORE simultaneously, add a penalty (extra cycles).

* (L2/3) Cache Conflicts – If the same memory region is accessed by both cores, introduce a cache penalty.

* ALU/FPUs – Shared Execution Unit Delay –If both cores use heavy arithmetic operations, execution slows down.  When cores run MUL or DIV together, extra latency is added to simulate execution unit contention.
```python
        if core1_op in ["LOAD", "STORE"] and core2_op in ["LOAD", "STORE"]:
            core1_cycles += memory_penalty
            core2_cycles += memory_penalty

        # Detect execution unit contention
        if core1_op in ["MUL", "DIV"] and core2_op in ["MUL", "DIV"]:
            core1_cycles += execution_unit_penalty
            core2_cycles += execution_unit_penalty
        
        # Detect cache conflicts
        if core1_mem and core2_mem and core1_mem == core2_mem:
            core1_cycles += cache_penalty
            core2_cycles += cache_penalty
```
I have now an heuristic dual-core simulator that takes basic assembly code as input and outputs execution times for both cores.

* Code mcpu5.py contains a function that simulates the dual core behavior. It takes two list of mnemonics as input and outputs execution time (in cycle) for both core.
```python
simulate_dual_core(core1_code:list[str], core2_code:list[str])->(int,int):
```
## Demonstration:
The exemple below shows that code on core 1 (that we could choose to remain the same during the exploration) runs with 12 cycles.
```python
from mcpu5 import simulate_dual_core

core1_exec_time, core2_exec_time = simulate_dual_core(
core1_code = "",
core2_code =["MUL R3, R4",
            "STORE R1, 20",
            "MOV R5, R6",
            "LOAD R1, 10",
            "ADD R1, R2",
            "MUL R3, R4",])
print("core1_exec_time", core1_exec_time)
print("core2_exec_time", core2_exec_time)
```

```
>>> core1_exec_time 0
>>> core2_exec_time 12
```
If a code runs on core 1 and uses same ressources than core 2, then execution time of core 2 will be larger:
```python
core1_exec_time, core2_exec_time = simulate_dual_core(core1_code = ["DIV R4,R5",
                                                                    "STORE R1, 20"
                                                                    "MOV R5, R6",
                                                                    "LOAD R1, 10",
                                                                    "ADD R1, R2",],
                                                    core2_code =["MUL R3, R4",
                                                                "STORE R1, 20",
                                                                "MOV R5, R6",
                                                                "LOAD R1, 10",
                                                                "ADD R1, R2",
                                                                "MUL R3, R4",])

print("core1_exec_time", core1_exec_time)
print("core2_exec_time", core2_exec_time)
```
```
>>> core1_exec_time 13
>>> core2_exec_time 16
```


# Approach

Here two codes will be running at the same time, one for each core.
On **core 1**, code `example.code.pickle` will be running, and on **core 2**, we will synthetize disturbing codes, so that the execution time of **core 1** is sometimes elongated:
```
MUL R3, R4
STORE R1, 20
MOV R5, R6
LOAD R1, 10
ADD R1, R2
MUL R3, R4
```

## IMGEP
* A goal is defined as a paire of core execution time `zg = {"core 1 execution time": 12, "core 2 execution time": 26"}` in the behavior space.
The parameter space is defined as the code executed on **core 2**
* The target loss is defined as the quadratic distance between an observation **z** and the goal **z_g** e.g if `z = {"core 1 execution time": 14, "core 2 execution time": 16"}`, then $Lg = \sqrt{{(12-14)}^{2} + {(26 - 16)}^2}$
* I pick 1-Nearest Neighbor algorithm for the selection operator.
* For the goal generator, I choose an discrete uniform distribution $\mathcal{U}_{\\{4,...,100\\}\times\\{4,...,100\\}}$

I would like to compare two main scenari for the implementation of a population based IMGEP:
* The mutation operator is implemented as a python function. See the function bellow i.e `imgep.OptimizationPolicy.light_code_mutation`. The first iterations of the imgep loop are performed by python function `utils.generate_random_code`.

```python

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
```
* The mutation operator is a LLM that understands basic codes e.g Llama, gpt4 ext. This is done with a prompt such as bellow. Soon, I will try it on **Jean Zay** or with another platform.

```python
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
```

# Results for POP-IMGEP with python function mutator



I can't produce interesting results with llms yet. Let's take a look at results for a short imgep with a mutation operator implemented as a python function. We can compare these results with a random exploration, meaning that for a same budget `N >>1`, we generate random assembly code at each iteration. See code `random_exploration.main.py`.
The results are easy to interpret i.e the more columns, the more interferences, the better the exploration. Pictures bellow suggest that POP-IMGEP outperforms the random exploration. 


![image](/image/comparaison.png)

POP-IMGEP with python function mutator             |  Random exploration
:-------------------------:|:-------------------------:
![image](/imgep_with_homemade_mutation_operator/image/history_visual.png)  | ![image](/random_exploration/image/history_visual.png) 


Next, I will attempt to improve the exploration by considering kNN algorithm with $k>1$. I will also try a to simulate more realistic processor e.g with more cores.
