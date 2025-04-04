import re
import numpy as np
def code_extractor(inputs)->list:
    #pattern = r'```(.*?)```'
    ## Using re.DOTALL to match across multiple lines
    #matches = re.findall(pattern, inputs, re.DOTALL)
    def extract_triple_backtick_text(text):
        match = re.search(r'```(.*)```', text, re.DOTALL)  # Matches everything after ```
        return match.group(1) if match else None
    match_ = extract_triple_backtick_text(inputs) 
    # Strip whitespace from each match
    #code_blocks = [match.strip() for match in matches]
    # Define a regex pattern to match instructions and their arguments
    pattern = re.compile(r'\b(MOVE|MOV|LOAD|LDR|LW|STORE|STR|SW|ADD|SUB|MUL|DIV)\b\s+([^\n]+)'    , re.IGNORECASE)

    # Find all occurrences of the instructions with arguments
    assert match_ !=None, "There is no map"
    instructions = pattern.findall(match_)
    assert len(instructions)>0, "no instruction"
    code_blocks = [" ".join(elem) for elem in instructions]

    print("inputs", match_)
    print(code_blocks)
#    exit()
    return code_blocks


def message2code(message,model,tokenizer)->list:
    inputs = tokenizer.apply_chat_template(
        message,
        tokenize = True,
        add_generation_prompt = True, # Must add for generation
        return_dict = True,
        return_tensors = "pt",
    ).to("cuda")
    n = 0
    while True:
        try:
            outputs = model.generate(input_ids = inputs["input_ids"],
                                attention_mask = inputs["attention_mask"],
                                max_new_tokens = 256,
                                use_cache = True)
            outputs = tokenizer.batch_decode(outputs)[0]
            print("outputs", outputs)
            out = code_extractor(outputs)
            break
        except: 
            n+=1
            if n>5:
                raise RuntimeError("More than 3 attempts for the LLM")
    return out


def make_random_code(model, tokenizer)->list:
    message_init = [
    {"from": "human", "value": f"""I have a cpu simulator with ten registers named from R1 to R10. The cpu takes assembly instructions STORE, LOAD, ADD, MUL as input. \n
    Here is an example of a list of instructions in this language:
    \n DIV R5, R6\n SUB R7, R8 \n LOAD R9, 30\nADD R9, R10\n
    Note that arithmetic operators take only two operands. For instance: "MUL R3, R2, R1" is not valid and "MUL R2, R1" is valid.

    Can you write a random list between 1 and 20 instructions ?
    Don't write python code. Your response has to contain only the list of instructions inside triple backticks with no more explanations.
        """},
    ]
    return message2code(message_init, model, tokenizer)
def make_random_code(model, tokenizer, nmax = 15):
    N = np.random.randint(0,nmax,1)[0]
import random
def generate_random_assembly(num_instructions:int)->list:
    
    # Available registers
    registers = [f"R{i}" for i in range(1, 11)]
    
    # Available instructions and their formats
    instructions = {
        "LOAD":  "LOAD {reg}, {imm}",   # LOAD R1, 10
        "STORE": "STORE {reg}, {imm}",  # STORE R2, 100
        "ADD":   "ADD {reg1}, {reg2}",   # ADD R3, R4
        "SUB":   "SUB {reg1}, {reg2}",   # SUB R5, R6
        "MUL":   "MUL {reg1}, {reg2}",   # MUL R7, R8
        "DIV":   "DIV {reg1}, {reg2}",   # DIV R9, R10
    }

    assembly_code = []
    for _ in range(num_instructions):
        # Choose a random instruction
        instr = random.choice(list(instructions.keys()))
        
        if instr in ["LOAD", "STORE"]:
            # For LOAD/STORE: pick a random register and a random immediate value (0-255)
            reg = random.choice(registers)
            imm = random.randint(0, 255)
            line = instructions[instr].format(reg=reg, imm=imm)
        else:
            # For arithmetic ops (ADD/SUB/MUL/DIV): pick two different registers
            reg1, reg2 = random.sample(registers, 2)
            line = instructions[instr].format(reg1=reg1, reg2=reg2)
        
        assembly_code.append(line)
    
    return assembly_code

## Generate random assembly (e.g., 10 instructions)
#random_code = generate_random_assembly(10)
#
## Print the generated code
#for line in random_code:
#    print(line)    
