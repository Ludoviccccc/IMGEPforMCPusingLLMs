Discussion we had with GPT
Me:

"Can you detail shared resources between the cores so that the execution time on one core depends on what is running on the other core ? "

ChatGPT said:

V"To introduce shared resources between the cores, we need to model contention for components like:
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
