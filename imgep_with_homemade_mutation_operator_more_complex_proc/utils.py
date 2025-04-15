import re
import numpy as np
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
def generate_random_assembly_list(n:int=50,ncores:int=8)->list[list[str]]:
                                                                out = [generate_random_assembly(np.random.randint(1,n,1)[0]) for j in range(ncores)] 
                                                                return out

## Generate random assembly (e.g., 10 instructions)
#random_code = generate_random_assembly(10)
#
## Print the generated code
#for line in random_code:
#    print(line)    
