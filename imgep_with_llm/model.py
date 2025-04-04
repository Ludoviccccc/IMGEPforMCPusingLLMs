import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
import sys
sys.path.append("../")
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



def make_model():    
    """
    returns model, tokenizer
    """
    max_seq_length = 512# Can increase for longer reasoning traces
    
    model, tokenizer = FastLanguageModel.from_pretrained(
    #model_name = "mistralai/Mistral-7B-v0.1",
    model_name = "meta-llama/meta-Llama-3.1-8B-Instruct",
    max_seq_length = max_seq_length,
    #load_in_4bit = True, # False for LoRA 16bit
    #fast_inference = True, # Enable vLLM fast inference
    #max_lora_rank = lora_rank,
    #gpu_memory_utilization = 0.1, # Reduce if out of memory
    )
    tokenizer = get_chat_template(
        tokenizer,
        chat_template = "chatml", # Supports zephyr, chatml, mistral, llama, alpaca, vicuna, vicuna_old, unsloth
        mapping = {"role" : "from", "content" : "value", "user" : "human", "assistant" : "gpt"}, # ShareGPT style
        map_eos_token = True, # Maps <|im_end|> to </s> instead
    )
    model = FastLanguageModel.get_peft_model(
        model,
    )
    return model, tokenizer
    #print("Maybe the model is already specified")
