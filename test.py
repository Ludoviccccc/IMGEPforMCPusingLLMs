import sys
sys.path.append("../")
from mcpu5 import simulate_dual_core

core1_exec_time, core2_exec_time = simulate_dual_core(
core1_code = "",
core2_code =["MUL R3, R4",
            "STORE R1, 20",
            "MOV R5, R6",
            "LOAD R1, 10",
            "ADD R1, R2",
            "MUL R3, R4",])
print("core1_exec_time", core1_exec_time)
print("core2_exec_time", core2_exec_time)
