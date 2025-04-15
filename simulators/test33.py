from test3 import Simulate_8_cores



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
simulate_8cores = Simulate_8_cores(program)
out = simulate_8cores()
print(out)


