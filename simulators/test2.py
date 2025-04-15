import threading
import time
import random
from collections import defaultdict

# Constants for simulation
MEMORY_LATENCY = 2  # base latency for memory access
CACHE_CONFLICT_PENALTY = 3  # penalty for cache conflicts
MEMORY_BUS_PENALTY = 2  # penalty for concurrent memory access
ALU_PENALTY = 4  # penalty for shared ALU usage

# Instructions
INSTRUCTIONS = {"MOVE", "MOV", "LOAD", "STORE", "MUL", "DIV", "SUB", "ADD"}

# Shared resources
shared_cache = {}
memory = defaultdict(int)
cache_lock = threading.Lock()
memory_bus_lock = threading.Lock()
alu_lock = threading.Lock()

class Core(threading.Thread):
    def __init__(self, core_id, program):
        super().__init__()
        self.core_id = core_id
        self.program = program
        self.registers = defaultdict(int)
        self.pc = 0
        self.execution_time = 0
        self.cache_misses = 0

    def run(self):
        while self.pc < len(self.program):
            instr_line = self.program[self.pc].strip()
            if not instr_line or instr_line.split()[0] not in INSTRUCTIONS:
                self.pc += 1
                continue

            parts = instr_line.replace(',', '').split()
            op = parts[0]
            args = parts[1:]

            latency = 1  # base latency for an instruction

            if op in {"MOVE", "MOV"}:
                self.registers[args[0]] = self.registers[args[1]] if args[1] in self.registers else int(args[1])

            elif op == "LOAD":
                addr = int(args[1])
                with cache_lock:
                    if shared_cache.get(addr) != self.core_id:
                        self.cache_misses += 1
                        latency += CACHE_CONFLICT_PENALTY
                        shared_cache[addr] = self.core_id
                if memory_bus_lock.locked():
                    latency += MEMORY_BUS_PENALTY
                with memory_bus_lock:
                    latency += MEMORY_LATENCY
                    self.registers[args[0]] = memory[addr]

            elif op == "STORE":
                addr = int(args[1])
                if memory_bus_lock.locked():
                    latency += MEMORY_BUS_PENALTY
                with memory_bus_lock:
                    latency += MEMORY_LATENCY
                    memory[addr] = self.registers[args[0]]

            elif op in {"MUL", "DIV", "SUB", "ADD"}:
                if alu_lock.locked():
                    latency += ALU_PENALTY
                with alu_lock:
                    src1 = self.registers[args[0]]
                    src2 = self.registers[args[1]]
                    if op == "MUL":
                        self.registers[args[0]] = src1 * src2
                    elif op == "DIV":
                        self.registers[args[0]] = src1 // src2 if src2 != 0 else 0
                    elif op == "SUB":
                        self.registers[args[0]] = src1 - src2
                    elif op == "ADD":
                        self.registers[args[0]] = src1 + src2

            self.execution_time += latency
            self.pc += 1

# Example usage
if __name__ == "__main__":
    # Assembly code for each core using two-operand syntax
    program = [
        "MOV R1, 5",
        "MOV R2, 10",
        "MUL R1, R2",
        "STORE R1, 100",
        "LOAD R4, 100",
        "DIV R4, R1",
        "ADD R4, R2",
        "SUB R4, R1",
    ]

    cores = [Core(i, program) for i in range(8)]

    for core in cores:
        core.start()
    for core in cores:
        core.join()

    for core in cores:
        print(f"Core {core.core_id}: Execution Time = {core.execution_time} cycles, Cache Misses = {core.cache_misses}")

