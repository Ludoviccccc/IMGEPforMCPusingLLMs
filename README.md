I have to focus on the expension operator and on the selection operator


I have noted some key points from ETCHEVERRY manuscript that could be useful for the current problem.
Models that are used in popIMGEP are often non-parametric.
k-NN is a common example for the selection operator. The model learns during the exploration. It is also based on the expension of the history


# Simulator

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

I would like to compare two main scenari for the implementation of a population based IMGEP:
* The mutation operator is implemented as a python function. See folder `imgep.OptimizationPolicy.light_code_mutation`. The first iterations of the imgep loop are performed by python function `utils.generate_random_code`.
* The mutation operator is a LLM that understands basic codes e.g Llama, gpt4 ext. This is done with a prompt. Unfortunatly, I am currently unable to use this code on my laptop because it takes too much power. Jean Zay or someone else should help me soon.

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
