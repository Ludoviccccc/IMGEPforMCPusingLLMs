import time
import random

class DualCoreSimulator:
    def __init__(self):
        self.registers = {f'R{i}': 0 for i in range(4)}  # Shared registers R0-R3
        self.memory = {i: 0 for i in range(10)}  # Shared memory (address 0-9)
        self.cycles = {"MOV": 1, "ADD": 2, "SUB": 2, "MUL": 4, "DIV": 6, "LOAD": 3, "STORE": 3}
        self.core1_time = 0
        self.core2_time = 0
        self.memory_access_penalty = 5  # Simulating memory contention penalty
        self.cache = {}  # Simulating a simple cache

    def execute_instruction(self, core, instr):
        parts = instr.split()
        op = parts[0]
        
        if op == "MOV":
            reg, val = parts[1], int(parts[2])
            self.registers[reg] = val
        elif op in {"ADD", "SUB", "MUL", "DIV"}:
            reg1, reg2 = parts[1], parts[2]
            if op == "ADD":
                self.registers[reg1] += self.registers[reg2]
            elif op == "SUB":
                self.registers[reg1] -= self.registers[reg2]
            elif op == "MUL":
                self.registers[reg1] *= self.registers[reg2]
            elif op == "DIV":
                self.registers[reg1] //= self.registers[reg2] if self.registers[reg2] != 0 else 0
        elif op == "LOAD":
            reg, addr = parts[1], int(parts[2])
            if addr in self.cache:
                self.registers[reg] = self.cache[addr]  # Fast cache access
            else:
                self.registers[reg] = self.memory[addr]
                self.cache[addr] = self.memory[addr]  # Cache the value
                exec_time = self.cycles[op] + self.memory_access_penalty  # Cache miss penalty
        elif op == "STORE":
            addr, reg = int(parts[1]), parts[2]
            self.memory[addr] = self.registers[reg]
            self.cache[addr] = self.registers[reg]  # Update cache
            exec_time = self.cycles[op] + self.memory_access_penalty  # Cache coherence penalty
        else:
            exec_time = self.cycles[op]
        
        if core == 1:
            self.core1_time += exec_time
        else:
            self.core2_time += exec_time
        
        return exec_time

    def run(self, core1_instrs, core2_instrs):
        c1_idx, c2_idx = 0, 0
        total_time = 0
        
        while c1_idx < len(core1_instrs) or c2_idx < len(core2_instrs):
            if c1_idx < len(core1_instrs):
                total_time += self.execute_instruction(1, core1_instrs[c1_idx])
                c1_idx += 1
            if c2_idx < len(core2_instrs):
                total_time += self.execute_instruction(2, core2_instrs[c2_idx])
                c2_idx += 1
            
        print("Final Registers:", self.registers)
        print("Final Memory:", self.memory)
        print(f"Core 1 Execution Time: {self.core1_time} cycles")
        print(f"Core 2 Execution Time: {self.core2_time} cycles")
        print(f"Total Execution Time: {total_time} cycles")

# Example Usage
core1_program = ["MOV R0 5", "ADD R0 R1", "STORE 0 R0"]
core2_program = ["MOV R1 3", "MUL R1 R0", "LOAD R2 0"]

simulator = DualCoreSimulator()
simulator.run(core1_program, core2_program)

