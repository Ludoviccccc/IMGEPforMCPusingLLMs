import threading
import time
import random
from collections import defaultdict

# Constants for simulation
#MEMORY_LATENCY = 2  # base latency for memory access
#MEMORY_BUS_PENALTY = 2  # penalty for concurrent memory access

# Instructions

# Shared resources
#shared_cache = {}
#memory = defaultdict(int)
#cache_lock = threading.Lock()
#memory_bus_lock = threading.Lock()


class Core(threading.Thread):
    # Metrics for interference tracking
    global_metrics = {
        "total_cache_conflicts": 0,
        "total_memory_bus_contention": 0,
        "total_alu_contention": 0
    }
    shared_cache = {}
    cache_lock = threading.Lock()
    memory_bus_lock = threading.Lock()
    alu_lock = threading.Lock()
    memory = defaultdict(int)
    def __init__(self, core_id, program):
        super().__init__()
        
        self.ALU_PENALTY = 4  # penalty for shared ALU usage
        self.MEMORY_LATENCY = 2  # base latency for memory access
        self.CACHE_CONFLICT_PENALTY = 3  # penalty for cache conflicts
        self.MEMORY_BUS_PENALTY = 2  # penalty for concurrent memory access
        self.core_id = core_id
        self.program = program
        self.registers = defaultdict(int)
        self.pc = 0
        self.execution_time = 0
        self.cache_misses = 0
        self.memory_contention = 0
        self.alu_contention = 0
        self.INSTRUCTIONS = {"MOVE", "MOV", "LOAD", "STORE", "MUL", "DIV", "SUB", "ADD"}

    def run(self):
        while self.pc < len(self.program):
            instr_line = self.program[self.pc].strip()
            if not instr_line or instr_line.split()[0] not in self.INSTRUCTIONS:
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
                with self.cache_lock:
                    if self.shared_cache.get(addr) != self.core_id:
                        self.cache_misses += 1
                        self.global_metrics["total_cache_conflicts"] += 1
                        latency += self.CACHE_CONFLICT_PENALTY
                        self.shared_cache[addr] = self.core_id
                if self.memory_bus_lock.locked():
                    latency += self.MEMORY_BUS_PENALTY
                    self.memory_contention += 1
                    self.global_metrics["total_memory_bus_contention"] += 1
                with self.memory_bus_lock:
                    latency += self.MEMORY_LATENCY
                    self.registers[args[0]] = self.memory[addr]

            elif op == "STORE":
                addr = int(args[1])
                if self.memory_bus_lock.locked():
                    latency += self.MEMORY_BUS_PENALTY
                    self.memory_contention += 1
                    self.global_metrics["total_memory_bus_contention"] += 1
                with self.memory_bus_lock:
                    latency += self.MEMORY_LATENCY
                    self.memory[addr] = self.registers[args[0]]

            elif op in {"MUL", "DIV", "SUB", "ADD"}:
                if self.alu_lock.locked():
                    latency += self.ALU_PENALTY
                    self.alu_contention += 1
                    self.global_metrics["total_alu_contention"] += 1
                with self.alu_lock:
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


class Simulate_8_cores:
    def __init__(self,listprograms):
        self.cores = [Core(i, program) for (i,program) in enumerate(listprograms)]
    def __call__(self):
        out = {}
        out = {"executiontime":[],
            "cachemiss":[],
            "memorycontention":[],
            "alucontention":[]}
        for core in self.cores:
            core.start()
        for core in self.cores:
            core.join()
        for core in self.cores:
            out["executiontime"].append(core.execution_time)
            out["cachemiss"].append(core.cache_misses)
            out["memorycontention"].append(core.memory_contention)
            out["alucontention"].append(core.alu_contention)
        return out
# Example usage
# Assembly code for each core using two-operand syntax
#program = [
#    "MOV R1, 5",
#    "MOV R2, 10",
#    "MUL R1, R2",
#    "STORE R1, 100",
#    "LOAD R4, 100",
#    "DIV R4, R1",
#    "ADD R4, R2",
#    "SUB R4, R1",
#]
#
#listprograms = [program  for i in range(8)]
#print(listprograms)
#
#S = Simulate_8_cores(listprograms)
#print(S())
