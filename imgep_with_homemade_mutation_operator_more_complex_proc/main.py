from imgep import IMGEP, GoalGenerator, OptimizationPolicy, History
import numpy as np
import re
from join_string import join_strings
import sys
sys.path.append("../")
import os
from simulators.testsave import Simulate_8_cores
import matplotlib.pyplot as plt
import pickle
from utils import generate_random_assembly_list
if __name__=="__main__":
    max_size = 1000 #max_size for the history
    N = 10000 #experimental budget
    N_init = 100 #Budget for random exploration at the begin
    Pi = OptimizationPolicy()
    G = GoalGenerator() 
    H = History(max_size = max_size)

    #with open(os.path.join("../example","code.pickle"),"rb") as f:
    #    Code = pickle.load(f)
    #Imgep = IMGEP(Code,N, N_init, H, G, Pi)

    ##Exploration
    #Imgep()
    #print("memory program")
    #for h in H.memory_program:
    #    print(h)
    #print("memory signature",H.memory_signature)
    #H.representation("image/history_visual")
    #plt.title(f"Imgep with experimental budget N={N} and Ninit = {N_init}")
    #plt.ylabel("Core 1 execution time")
    #plt.xlabel("Core 2 execution time")
    #plt.savefig("image/history_visual.png")
    #plt.show()
    #with open("dict/imgep.pickle", "wb") as f:
    #    pickle.dump(H.memory_signature,f)
    for j in range(2):
        listprograms = generate_random_assembly_list(20) 
        #print(listprograms)
#        exit()
        out = Simulate_8_cores(listprograms)()
        #print("out", list(out.values()))
        sample = {"program":[listprograms],
                  "signatures":[list(out.values())]}
        H.store(sample)

    listprograms = generate_random_assembly_list(20) 
    signature = Simulate_8_cores(listprograms)()
    print("signature", signature)
    #print(H.select_closest_code(list(signature.values())))

    mutation = Pi.light_code_mutation_vec(listprograms)
    #print("mutation", mutation)
    print(Pi(signature, H))
