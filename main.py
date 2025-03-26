import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("device", device)
from unsloth.chat_templates import get_chat_template
from datasets import load_dataset
import unsloth


from unsloth import FastLanguageModel, is_bfloat16_supported
import torch
from transformers import Trainer, TrainingArguments
from trl import SFTTrainer
import re
from history import History
from join_string import join_strings
from mcpu5 import simulate_dual_core


train  = False
max_seq_length = 512# Can increase for longer reasoning traces
lora_rank = 32 # Larger rank = smarter, but slower

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
    #r = lora_rank, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    #target_modules = [
    #    "q_proj", "k_proj", "v_proj", "o_proj",
    #    "gate_proj", "up_proj", "down_proj",
    #], # Remove QKVO if out of memory
    #lora_alpha = lora_rank,
    #use_gradient_checkpointing = "unsloth", # Enable long context finetuning
    #random_state = 3407,
)






#FastLanguageModel.for_inference(model) # Enable native 2x faster inference
program1 = ["MOV R1, R2",
    "LOAD R1, 10",
    "ADD R1, R2",
    "MUL R3, R4",
    "STORE R1, 20",
    "MOV R5, R6",
    "LOAD R1, 10",
    "ADD R1, R2",
    "MUL R3, R4",
    "STORE R1, 20",
    "DIV R5, R6",
    "SUB R7, R8",
    "LOAD R9, 30",
    "ADD R9, R10"]

messages = [
    {"from": "human", "value": f"""I have a cpu simulator with registers R1 up to R10, and that takes assembly instructions STORE, LOAD, ADD, MUL as input. \n
Here is an example of a list of instructions in this language:
\n DIV R5, R6\n SUB R7, R8 \n LOAD R9, 30\nADD R9, R10\n

A mutation of a list of instructions consists in inserting, deleting or replacing a few instruction in program. For instance, here is a mutation of the list above. I added a the instruction LOAD in the fist line and I have replaced the last instruction by an instruction STORE.

\nLOAD R4, 30\n DIV R5, R6\n SUB R7, R8 \n LOAD R9, 30\nSTORE R1, 20\n

Can you perform a single light mutation based on the following list of instructions bellow?     
Your answer has to be in the following format:

    Mutated list of intructions inside quotation marks
    Reflexion on how you mutate it
List of instructions:
{join_strings(program1)}
    """},
]
inputs = tokenizer.apply_chat_template(
    messages,
    tokenize = True,
    add_generation_prompt = True, # Must add for generation
    return_dict = True,
    return_tensors = "pt",
).to("cuda")


#print("inputs", inputs)
outputs = model.generate(input_ids = inputs["input_ids"],
                        attention_mask = inputs["attention_mask"],
                        max_new_tokens = 256, 
                        use_cache = True)
outputs = tokenizer.batch_decode(outputs)[0]
print("outputs", outputs)



# Regular expression to capture multiple code blocks
#pattern = r"```(.*?)```"
pattern = r'"(.*?)"'

# Using re.DOTALL to match across multiple lines
matches = re.findall(pattern, outputs, re.DOTALL)

# Strip whitespace from each match
code_blocks = [match.strip() for match in matches]

# Output the extracted code blocks
print("Extracted Code Blocks:")
#    print(f"Code Block {i}:")
for i, block in enumerate(code_blocks, 1):
    print(block)
    print("-" * 20)
print(code_blocks)
H = History(max_size=100)
core1_exec_time, core2_exec_time = simulate_dual_core(
    core1_code = code_blocks[0].split(),
    core2_code = 
    ["MUL R3, R4",
    "STORE R1, 20",
    "MOV R5, R6",
    "LOAD R1, 10",
    "ADD R1, R2",
    "MUL R3, R4",])
H.store({"program":[block], 
        "signature": [{"core1_exec_time":core1_exec_time,"core2_exec_time": core2_exec_time}]})
#    print(f"Code Block {i}:")
