import queue

def simulate_dual_core(core1_code, core2_code):
    instruction_times = {
        "LOAD": 2, "STORE": 2, "ADD": 1, "SUB": 1, 
        "MUL": 3, "DIV": 4, "MOV": 1  # MOV default to 1 cycle unless memory is involved
    }
    
    memory_penalty = 2  # Extra cycles if both cores do LOAD, STORE, or memory-based MOV
    execution_unit_penalty = 2  # Extra cycles if both cores run MUL or DIV together
    cache_penalty = 3  # Extra cycles if same memory is accessed by both cores
    
    core1_queue = queue.Queue()
    core2_queue = queue.Queue()
    
    core1_time = 0
    core2_time = 0
    shared_memory_access = {}

    # Helper function to check if MOV involves memory and extract address
    def get_memory_address(instr):
        parts = instr.split()
        if len(parts) > 1 and "[" in parts[1]:  
            return parts[1].strip("[],")  # Extract memory address
        elif len(parts) > 2 and "[" in parts[2]:  
            return parts[2].strip("[],")  # Extract memory address
        return None

    # Load instructions into respective core queues
    for instruction in core1_code:
        parts = instruction.split()
        op = parts[0]
        if op in instruction_times:
            mem_addr = get_memory_address(instruction)
            cycles = instruction_times[op]
            if op == "MOV" and mem_addr:  # Memory-based MOV behaves like LOAD/STORE
                cycles = 2
            core1_queue.put((op, cycles, mem_addr))

    for instruction in core2_code:
        parts = instruction.split()
        op = parts[0]
        if op in instruction_times:
            mem_addr = get_memory_address(instruction)
            cycles = instruction_times[op]
            if op == "MOV" and mem_addr:
                cycles = 2
            core2_queue.put((op, cycles, mem_addr))

    # Simulate execution in parallel with contention handling
    while not core1_queue.empty() or not core2_queue.empty():
        core1_instr = core1_queue.get() if not core1_queue.empty() else (None, 0, None)
        core2_instr = core2_queue.get() if not core2_queue.empty() else (None, 0, None)
        
        core1_op, core1_cycles, core1_mem = core1_instr
        core2_op, core2_cycles, core2_mem = core2_instr

        # Detect shared memory contention
        if (core1_op in ["LOAD", "STORE", "MOV"] and core1_mem) and \
           (core2_op in ["LOAD", "STORE", "MOV"] and core2_mem):
            core1_cycles += memory_penalty
            core2_cycles += memory_penalty

        # Detect execution unit contention
        if core1_op in ["MUL", "DIV"] and core2_op in ["MUL", "DIV"]:
            core1_cycles += execution_unit_penalty
            core2_cycles += execution_unit_penalty
        
        # Detect cache conflicts
        if core1_mem and core2_mem and core1_mem == core2_mem:
            core1_cycles += cache_penalty
            core2_cycles += cache_penalty

        core1_time += core1_cycles
        core2_time += core2_cycles

    return core1_time, core2_time

# Example input assembly codes for each core with MOV instructions
core1_code = [
    "MOV R1, R2",
    "LOAD R3, [100]",
    "MOV R4, [200]",
    "ADD R1, R3",
    "MUL R5, R6",
    "MOV [300], R7",
    "STORE R8, [400]"
]

core2_code = [
    "DIV R9, R10",
    "SUB R11, R12",
    "MOV R13, [100]",  # Shared memory access with Core 1
    "MOV [300], R14"  # Shared memory write
]

core1_exec_time, core2_exec_time = simulate_dual_core(core1_code, core2_code)
print(f"Core 1 Execution Time: {core1_exec_time} cycles")
print(f"Core 2 Execution Time: {core2_exec_time} cycles")

