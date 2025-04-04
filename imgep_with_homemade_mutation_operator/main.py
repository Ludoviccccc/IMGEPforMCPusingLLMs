from utils import code_extractor, make_random_code, message2code
from imgep import IMGEP, GoalGenerator, OptimizationPolicy, History
import numpy as np
import torch
import re
from join_string import join_strings
import sys
sys.path.append("../")
from mcpu5 import simulate_dual_core
if __name__=="__main__":
    max_size = 100
    N = 200
    N_init = 50
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
