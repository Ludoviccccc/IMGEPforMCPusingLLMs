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
    max_size = 100
    N = 5
    N_init = 1
    model, tokenizer = make_model()
    Pi = OptimizationPolicy(model , tokenizer)
    G = GoalGenerator() 
    H = History(max_size = max_size)
    Imgep = IMGEP(model,tokenizer, N, N_init, H, G, Pi)

    #Exploration
    Imgep()
