# Simulator 💻

Discussion we had with GPT
Me:

"Can you detail shared resources between the cores so that the execution time on one core depends on what is running on the other core ? "

ChatGPT said:

"To introduce shared resources between the cores, we need to model contention for components like:
```
Shared Cache (L2/L3) – Accessing shared memory introduces delays.

Memory Bus – Both cores competing for memory increases latency.

ALU/FPUs – If both cores use heavy arithmetic operations, execution slows down.
```
Implementation Plan:
```
Simulate Memory Contention – If both cores execute a LOAD or STORE simultaneously, add a penalty (extra cycles).

Cache Conflicts – If the same memory region is accessed by both cores, introduce a cache penalty.

Shared Execution Unit Delay – If both cores run MUL or DIV together, add extra latency to simulate execution unit contention.
```
I’ll now update the code to reflect these dependencies.

I’ve updated the simulation to include shared resource contention:
```
Memory contention: If both cores execute LOAD or STORE together, they experience a penalty (extra cycles).

Execution unit contention: If both cores run MUL or DIV at the same time, there's an additional delay. 
```
" 

I have now an heuristic dual-core simulator that takes basic assembly code as input and outputs execution times for both cores.

* Code mcpu5.py contains a function that simulates the dual core behavior. It takes two list of mnemonics as input and outputs execution time (in cycle) for both core.
```python
simulate_dual_core(core1_code:list[str], core2_code:list[str])->(int,int):
```

# Approach

Here two codes will be running at the same time, one for each core.
On **core 1**, the following will be running, and on **core 2**, we will synthetize disturbing codes, so that the execution time of **core 1** is sometimes elongated:
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
* I pick 1-Nearest Neighbor algorithm for the selection operator and I simply use a quadratic distance for the target Loss.

I would like to compare two main scenari for the implementation of a population based IMGEP:
* The mutation operator is implemented as a python function. See folder `imgep.OptimizationPolicy.light_code_mutation`. The first iterations of the imgep loop are performed by python function `utils.generate_random_code`.
* The mutation operator is a LLM that understands basic codes e.g Llama, gpt4 ext. This is done with a prompt such as bellow. Unfortunatly, I am currently unable to use this code on my laptop for many iterations because it takes too much power. Hopefully, **Jean Zay** or someone else should come and help me soon.

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

# Results

I can't show you interesting stuff with llm yet. Let's take a look at results for a short imgep with a mutation operator implemented as a python function. We can compare these results with a random exploration, meaning that for a same budget `N >>1`, we generate random assembly code at each iteration.

POP-IMGEP with python function mutator             |  Random exploration
:-------------------------:|:-------------------------:
![image](/imgep_with_homemade_mutation_operator/image/history_visual.png)  | ![image](/random_exploration_homemade_mutation_operator/image/history_visual.png) 

