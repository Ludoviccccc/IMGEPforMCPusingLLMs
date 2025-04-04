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
* The mutation operator is implemented as a python function. See folder `imgep.OptimizationPolicy.light_code_mutation`. The first iterations of the imgep loop are performed by a python function `utils.generate_random_code`.
* The mutation operator is a LLM that understands basic codes e.g Llama, gpt4 ext. S
