import re
def code_extractor(inputs):
    #pattern = r'```(.*?)```'
    ## Using re.DOTALL to match across multiple lines
    #matches = re.findall(pattern, inputs, re.DOTALL)
    def extract_triple_backtick_text(text):
        match = re.search(r'```(.*)```', text, re.DOTALL)  # Matches everything after ```
        return match.group(1) if match else None
    match_ = extract_triple_backtick_text(inputs) 
    # Strip whitespace from each match
    #code_blocks = [match.strip() for match in matches]
    # Define a regex pattern to match instructions and their arguments
    pattern = re.compile(r'\b(MOVE|MOV|LOAD|LDR|LW|STORE|STR|SW|ADD|SUB|MUL|DIV)\b\s+([^\n]+)'    , re.IGNORECASE)

    # Find all occurrences of the instructions with arguments
    assert match_ !=None, "There is no map"
    instructions = pattern.findall(match_)
    assert len(instructions)>0, "no instruction"
    code_blocks = [" ".join(elem) for elem in instructions]

    print("inputs", match_)
    print(code_blocks)
#    exit()
    return code_blocks


def message2code(message,model,tokenizer):
    inputs = tokenizer.apply_chat_template(
        message,
        tokenize = True,
        add_generation_prompt = True, # Must add for generation
        return_dict = True,
        return_tensors = "pt",
    ).to("cuda")
    n = 0
    while True:
        try:
            outputs = model.generate(input_ids = inputs["input_ids"],
                                attention_mask = inputs["attention_mask"],
                                max_new_tokens = 256,
                                use_cache = True)
            outputs = tokenizer.batch_decode(outputs)[0]
            print("outputs", outputs)
            out = code_extractor(outputs)
            break
        except: 
            n+=1
            if n>5:
                raise RuntimeError("More than 3 attempts for the LLM")
    return out


def make_random_code(model, tokenizer):
    message_init = [
    {"from": "human", "value": f"""I have a cpu simulator with ten registers named from R1 to R10. The cpu takes assembly instructions STORE, LOAD, ADD, MUL as input. \n
    Here is an example of a list of instructions in this language:
    \n DIV R5, R6\n SUB R7, R8 \n LOAD R9, 30\nADD R9, R10\n
    Note that arithmetic operators take only two operands. For instance: "MUL R3, R2, R1" is not valid and "MUL R2, R1" is valid.

    Can you write a random list between 1 and 20 instructions ?
    Don't write python code. Your response has to contain only the list of instructions inside triple backticks with no more explanations.
        """},
    ]
    return message2code(message_init, model, tokenizer)
