from imgep import IMGEP, GoalGenerator, OptimizationPolicy, History
import numpy as np
import re
from join_string import join_strings
import sys
sys.path.append("../")
import os
from simulators.mcpu5 import simulate_dual_core
import matplotlib.pyplot as plt
import pickle
from utils import generate_random_assembly
if __name__=="__main__":
    max_size = 10000 #max_size for the history
    N = 10000 #experimental budget
    N_init = 100 #Budget for random exploration at the begin
    Pi = OptimizationPolicy()
    G = GoalGenerator() 
    H = History(max_size = max_size)

    with open(os.path.join("../example","code.pickle"),"rb") as f:
        Code = pickle.load(f)
    Imgep = IMGEP(Code,N, N_init, H, G, Pi)
    print("Code len", len(Code))

    #Exploration
    Imgep()
    signtab = np.zeros((len(H.memory_signature["core1_exec_time"]), 2))
    signtab[:,0] = H.memory_signature["core1_exec_time"]
    signtab[:,1] = H.memory_signature["core2_exec_time"]
    var = [np.var(signtab[:j]) for j in range(len(signtab))]
    plt.figure()
    plt.plot(var)
    plt.show()
    H.representation("image/history_visual")
    plt.title(f"Imgep with experimental budget N={N} and Ninit = {N_init}")
    plt.ylabel("Core 1 execution time")
    plt.xlabel("Core 2 execution time")
    plt.savefig("image/history_visual.png")
    plt.show()
    with open("dict/imgep.pickle", "wb") as f:
        pickle.dump(H.memory_signature,f)
