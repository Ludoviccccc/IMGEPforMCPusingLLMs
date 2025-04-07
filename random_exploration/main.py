import torch
import sys
import matplotlib.pyplot as plt
sys.path.append("../imgep_with_homemade_mutation_operator/")
sys.path.append("../")
from utils import generate_random_assembly
from imgep import History
import numpy as np
import re
from join_string import join_strings
from mcpu5 import simulate_dual_core
import pickle


if __name__=="__main__":
    print(__name__)
    class RandomExploration:
        def __init__(self,N:int,H:History):
            """
            N:int. Experimental budget
            """
            self.N = N
            self.H = H
        def __call__(self):
            for i in range(self.N):
                core1_code = generate_random_assembly(np.random.randint(0,20,1)[0])
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
    N = 1000
    max_size = 1000
    H = History(max_size)
    randomexploration = RandomExploration(N, H)
    randomexploration()
    print("signatures:",H.memory_signature)
    H.representation()
    plt.title(f"Random Exploration with experimental budget N={N}")
    plt.ylabel("Core 1 execution time")
    plt.xlabel("Core 2 execution time")
    plt.savefig("image/history_visual.png")
    plt.show()
    with open("dict/randomexploration.pickle", "wb") as f:
        pickle.dump(H.memory_signature,f)
