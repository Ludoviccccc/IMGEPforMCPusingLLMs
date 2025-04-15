import torch
import sys
import matplotlib.pyplot as plt
sys.path.append("../imgep_with_homemade_mutation_operator/")
sys.path.append("../")
#sys.path.append("../")V
from utils import generate_random_assembly
from imgep import History
import numpy as np
import re
from join_string import join_strings
from simulators.mcpu5 import simulate_dual_core
import pickle


if __name__=="__main__":
    print(__name__)
    class RandomExploration:
        def __init__(self,code:list[str],N:int,H:History):
            """
            N:int. Experimental budget
            """
            self.N = N
            self.H = H
            self.code = code
        def __call__(self):
            for i in range(self.N):
                core1_code = generate_random_assembly(np.random.randint(0,100,1)[0])
                core1_exec_time, core2_exec_time = simulate_dual_core(
                                                    core1_code = core1_code,
                                                    core2_code = self.code)
                self.H.store({"program":[core1_code],
                             "signature": [{"core1_exec_time": core1_exec_time,
                                            "core2_exec_time": core2_exec_time}]})
    N = 10000
    max_size = 10000
    H = History(max_size)

    with open("../example/code.pickle", "rb") as f:
        Code = pickle.load(f)
    #print("code", len(Code))
    #exit()
    randomexploration = RandomExploration(Code,N, H)
    randomexploration()
    H.representation()
    plt.title(f"Random Exploration with experimental budget N={N}")
    plt.ylabel("Core 1 execution time")
    plt.xlabel("Core 2 execution time")
    plt.savefig("image/history_visual.png")
    plt.show()
    with open("dict/randomexploration.pickle", "wb") as f:
        pickle.dump(H.memory_signature,f)
