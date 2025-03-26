import queue

def simulate_dual_core(core1_code, core2_code):
    instruction_times = {"LOAD": 2, "STORE": 2, "ADD": 1, "SUB": 1, "MUL": 3, "DIV": 4}
    
    core1_queue = queue.Queue()
    core2_queue = queue.Queue()
    core1_time = 0
    core2_time = 0
    
    # Load instructions into respective core queues
    for instruction in core1_code:
        parts = instruction.split()
        if parts[0] in instruction_times:
            core1_queue.put(instruction_times[parts[0]])
    
    for instruction in core2_code:
        parts = instruction.split()
        if parts[0] in instruction_times:
            core2_queue.put(instruction_times[parts[0]])
    
    # Simulate execution in parallel
    while not core1_queue.empty() or not core2_queue.empty():
        if not core1_queue.empty():
            core1_time += core1_queue.get()
        if not core2_queue.empty():
            core2_time += core2_queue.get()
    
    return core1_time, core2_time

# Example input assembly codes for each core
core1_code = [
    "LOAD R1, 10",
    "ADD R1, R2",
    "MUL R3, R4",
    "MUL R3, R4",
    "MUL R3, R4",
    "STORE R1, 20"
]

core2_code = [
    "DIV R5, R6",
    "SUB R7, R8",
    "LOAD R9, 30",
    "ADD R9, R10"
]

core1_exec_time, core2_exec_time = simulate_dual_core(core1_code, core2_code)
print(f"Core 1 Execution Time: {core1_exec_time} cycles")
print(f"Core 2 Execution Time: {core2_exec_time} cycles")

