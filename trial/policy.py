class OptimizationPolicy:
    """
    Selects a parameter based on a chosen goal and the history.
    Takes the code corresponding to the closest signature to the desired goal signature
    """
    def __init__(self):    
        pass
    def __call__(self,goal:dict[list],H:History):
        closest_code = H.select_closest_code(goal) #most promising sample from the history
        output = self.light_code_mutation(closest_code["program"]) #expansion strategie: small random mutation
        return output
    def light_code_mutation(self,program:list[str]):
        messages = [
        {"from": "human", "value": f"""I have a cpu simulator with registers R1 up to R10, and that takes assembly instructions STORE, LOAD, ADD, MUL as input. \n
        Here is an example of a list of instructions in this language:
        \n DIV R5, R6\n SUB R7, R8 \n LOAD R9, 30\nADD R9, R10\n
        
        A mutation of a list of instructions consists in inserting, deleting or replacing a few instruction in program. For instance, here is a mutation of the list above. I added a the instruction LOAD in the fist line and I have replaced the last instruction by an instruction STORE.
        
        \nLOAD R4, 30\n DIV R5, R6\n SUB R7, R8 \n LOAD R9, 30\nSTORE R1, 20\n
        
        Can you perform a single light mutation based on the following list of instructions bellow?     
        Your answer has to be in the following format:
        
            Mutated list of intructions, each presented inside quotation marks
            Reflexion on how you mutate it
        List of instructions:
        {join_strings(program)}
            """},
        ]
        return message2code(messages)
