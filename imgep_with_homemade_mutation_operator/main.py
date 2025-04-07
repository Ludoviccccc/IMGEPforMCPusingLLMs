from imgep import IMGEP, GoalGenerator, OptimizationPolicy, History
import numpy as np
import re
from join_string import join_strings
import sys
sys.path.append("../")
from mcpu5 import simulate_dual_core
import matplotlib.pyplot as plt
import pickle
if __name__=="__main__":
    max_size = 1000 #max_size for the history
    N = 1000 #experimental budget
    N_init = 100 #Budget for random exploration at the begin
    Pi = OptimizationPolicy()
    G = GoalGenerator() 
    H = History(max_size = max_size)
    Imgep = IMGEP(N, N_init, H, G, Pi)

    #Exploration
    Imgep()
    print("memory program")
    for h in H.memory_program:
        print(h)
    print("memory signature",H.memory_signature)
    H.representation("image/history_visual")
    plt.title(f"Imgep with experimental budget N={N} and Ninit = {N_init}")
    plt.ylabel("Core 1 execution time")
    plt.xlabel("Core 2 execution time")
    plt.savefig("image/history_visual.png")
    plt.show()
    with open("dict/imgep.pickle", "wb") as f:
        pickle.dump(H.memory_signature,f)
