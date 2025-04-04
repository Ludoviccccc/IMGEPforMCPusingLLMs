import torch
import sys
sys.path.append("../imgep_with_llm/")
sys.path.append("../imgep_with_llm")
from utils import code_extractor, make_random_code, message2code
from imgep import IMGEP, GoalGenerator, OptimizationPolicy, History

import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device", device)
from unsloth.chat_templates import get_chat_template
from datasets import load_dataset
import unsloth
import numpy as np

from unsloth import FastLanguageModel, is_bfloat16_supported
import torch
from transformers import Trainer, TrainingArguments
from trl import SFTTrainer
import re
from join_string import join_strings
from mcpu5 import simulate_dual_core
from model import make_model


if __name__=="__main__":
    print(__name__)
    class RandomExploration:
        def __init__(self,model,N:int,H:History):
            """
            N:int. Experimental budget
            pass
            """
            self.N = N
            self.model = model
            self.tokenizer = tokenizer
            self.H = H
        def __call__(self):
            for i in range(self.N):
                core1_code = make_random_code(self.model, tokenizer=self.tokenizer)
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
    N = 20
    max_size = 100
    H = History(max_size)
    model,tokenizer = make_model()
    randomexploration = RandomExploration(model,N, H)
    randomexploration()
    H.representation()
