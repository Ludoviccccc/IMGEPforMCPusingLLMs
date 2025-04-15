import threading
import time

# === Instruction Costs ===
INSTRUCTION_COST = {
    'LOAD': 3,
    'STORE': 3,
    'ADD': 1,
    'SUB': 1,
    'MUL': 2,
    'DIV': 2
}

# === Shared Resource Contention Model ===
class ContendedResource:
    def __init__(self, name, base_latency, penalty_per_access):
        self.name = name
        self.lock = threading.Lock()
        self.current_users = 0
        self.base_latency = base_latency
        self.penalty_per_access = penalty_per_access

    def access(self):
        with self.lock:
            self.current_users += 1
            penalty = self.penalty_per_access * (self.current_users - 1)
        return self.base_latency + penalty

    def release(self):
        with self.lock:
            self.current_users -= 1


# === Create Shared Resources ===
memory_bus = ContendedResource("Memory Bus", base_latency=3, penalty_per_access=2)
shared_cache = ContendedResource("L3 Cache", base_latency=1, penalty_per_access=1)
alu_fpu = ContendedResource("ALU/FPU", base_latency=1, penalty_per_access=1)

# === Simulate Cores ===
NUM_CORES = 8
execution_times = [0 for _ in range(NUM_CORES)]

def parse_instruction(instr):
    return instr.strip().split()[0].upper()

def simulate_core(core_id, instructions):
    time_elapsed = 0
    for instr in instructions:
        op = parse_instruction(instr)

        if op in ['LOAD', 'STORE']:
            # Access shared memory + cache
            mem_latency = memory_bus.access()
            cache_latency = shared_cache.access()
            time_elapsed += mem_latency + cache_latency
            time.sleep(0.01)  # Simulate time delay
            memory_bus.release()
            shared_cache.release()

        elif op in ['ADD', 'SUB', 'MUL', 'DIV']:
            # Use shared ALU/FPU
            base_cost = INSTRUCTION_COST.get(op, 1)
            alu_latency = alu_fpu.access()
            time_elapsed += base_cost + alu_latency
            time.sleep(0.005)
            alu_fpu.release()

        else:
            time_elapsed += INSTRUCTION_COST.get(op, 1)

    execution_times[core_id] = time_elapsed

# === Sample Instruction Sets for Each Core ===
core_programs = [
    ["LOAD R1, 100", "ADD R2, R1, 5", "MUL R3, R2, R2", "STORE R3, 200"],
    ["LOAD R1, 150", "SUB R2, R1, 2", "DIV R3, R2, 3", "STORE R3, 250"],
    ["ADD R1, R2, 5", "MUL R1, R1, 4", "DIV R2, R1, 2"],
    ["LOAD R2, 120", "STORE R2, 220", "MUL R2, R2, 2"],
    ["MUL R1, R2, R3", "ADD R4, R1, 1", "SUB R4, R4, 2"],
    ["LOAD R4, 101", "STORE R4, 102", "MUL R4, R4, 3"],
    ["ADD R1, R2, 3", "DIV R3, R1, 2", "MUL R3, R3, 4"],
    ["LOAD R3, 160", "STORE R3, 170", "SUB R3, R3, 1"]
]

# === Start Simulation ===
threads = []
for core_id in range(NUM_CORES):
    thread = threading.Thread(target=simulate_core, args=(core_id, core_programs[core_id]))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# === Report Execution Times ===
print("\n--- Core Execution Results ---")
for i, cycles in enumerate(execution_times):
    print(f"Core {i}: {cycles} cycles")

