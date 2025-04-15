import threading
import time
import random
from collections import defaultdict


class Core(threading.Thread):
    global_metrics = {
        "total_cache_conflicts": 0,
        "total_memory_bus_contention": 0,
        "total_alu_contention": 0
    }
    def __init__(self, core_id, program):
        super().__init__()
        self.core_id = core_id
        self.program = program
        self.registers = defaultdict(int)
        self.pc = 0
        self.execution_time = 0
        self.cache_misses = 0
        self.memory_contention = 0
        self.alu_contention = 0
        self.INSTRUCTIONS = {"MOVE", "MOV", "LOAD", "STORE", "MUL", "DIV", "SUB", "ADD"}

        
        # Metrics for interference tracking
    def run(self):

        # Constants for simulation
        MEMORY_LATENCY = 2  # base latency for memory access
        CACHE_CONFLICT_PENALTY = 3  # penalty for cache conflicts
        MEMORY_BUS_PENALTY = 2  # penalty for concurrent memory access
        ALU_PENALTY = 4  # penalty for shared ALU usage
        
        # Instructions
        
        # Shared resources
        shared_cache = {}
        memory = defaultdict(int)
        cache_lock = threading.Lock()
        memory_bus_lock = threading.Lock()
        alu_lock = threading.Lock()
        
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
                with cache_lock:
                    if shared_cache.get(addr) != self.core_id:
                        self.cache_misses += 1
                        self.global_metrics["total_cache_conflicts"] += 1
                        latency += CACHE_CONFLICT_PENALTY
                        shared_cache[addr] = self.core_id
                if memory_bus_lock.locked():
                    latency += MEMORY_BUS_PENALTY
                    self.memory_contention += 1
                    self.global_metrics["total_memory_bus_contention"] += 1
                with memory_bus_lock:
                    latency += MEMORY_LATENCY
                    self.registers[args[0]] = memory[addr]

            elif op == "STORE":
                addr = int(args[1])
                if memory_bus_lock.locked():
                    latency += MEMORY_BUS_PENALTY
                    self.memory_contention += 1
                    self.global_metrics["total_memory_bus_contention"] += 1
                with memory_bus_lock:
                    latency += MEMORY_LATENCY
                    memory[addr] = self.registers[args[0]]

            elif op in {"MUL", "DIV", "SUB", "ADD"}:
                if alu_lock.locked():
                    latency += ALU_PENALTY
                    self.alu_contention += 1
                    self.global_metrics["total_alu_contention"] += 1
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
#if __name__ == "__main__":
#    # Assembly code for each core using two-operand syntax
#    program = [
#        "MOV R1, 5",
#        "MOV R2, 10",
#        "MUL R1, R2",
#        "STORE R1, 100",
#        "LOAD R4, 100",
#        "DIV R4, R1",
#        "ADD R4, R2",
#        "SUB R4, R1",
#    ]
#
    #self.cores = [Core(i, program) for i in range(8)]

    #for core in self.cores:
    #    core.start()
    #for core in self.cores:
    #    core.join()

    #for core in self.cores:
    #    print(f"Core {core.core_id}: Execution Time = {core.execution_time} cycles, Cache Misses = {core.cache_misses}, "
    #          f"Memory Contentions = {core.memory_contention}, ALU Contentions = {core.alu_contention}")

    #print("\nGlobal Interference Metrics:")
    #for metric, value in self.cores[0].global_metrics.items():
    #    print(f"{metric.replace('_', ' ').title()}: {value}")


class Simulate_8_cores:
    def __init__(self,program:list[str]):
        self.cores = [Core(i, program) for i in range(8)]
    def __call__(self):
        out = {"CoreExecutionTime":[],
               "CacheMisses":[],
               "MemoryContention":[],
               "ALUContentions": []}

#        "Memory Contentions = {core.memory_contention}, ALU Contentions = {core.alu_contention}
        for core in self.cores:
            core.start()
        for core in self.cores:
            core.join()
        for core in self.cores:
            print(f"Core {core.core_id}: Execution Time = {core.execution_time} cycles, Cache Misses = {core.cache_misses}, "
                  f"Memory Contentions = {core.memory_contention}, ALU Contentions = {core.alu_contention}")
            out["CoreExecutionTime"].append(core.execution_time)
            out["CacheMisses"].append(core.cache_misses)
            out["MemoryContention"].append(core.memory_contention)
            out["ALUContentions"].append(core.alu_contention)

#        print("\nGlobal Interference Metrics:")
#        for metric, value in self.cores[0].global_metrics.items():
#            print(f"{metric.replace('_', ' ').title()}: {value}")
        return out

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
listprograms = [program for i in range(8)]
simulate_8cores = Simulate_8_cores(listprograms)
simulate_8cores()

