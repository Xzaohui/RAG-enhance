import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

device='cuda:2'

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-chat-hf")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-70b-chat-hf",device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
model.to(device)


p_qag="""
You are a Query/Answer generator that generates new multiple Query or Answers based on origen Query, old Query and known KV informations.Continue generating queries if the Answer is not clear, and generate Answers if the Answer is clear. The Answer must be based on origen Query. Now give the old Query and KV information:
Query:{}
KV informations:{}
"""

p_kve="""
You are a KV extractor. I will provide a Query, and you will extract relevant key-value pairs from the document. The key-value pairs here may not be direct Answers to the Query.
Doc:{}
Query:{}
"""

p_judge="""
You are a Query and answer evaluator, and you will use one Query and two answers to determine whether their conclusions are consistent.
Query:{}
answer1:{}
answer2:{}
"""

def kv_extract(doc,query):
    input_text=p_kve.format(doc,query)
    inputs=tokenizer(input_text, return_tensors="pt")
    out = model.generate(
        input_ids=inputs["input_ids"].to(device)
    )
    out_text = tokenizer.decode(out[0])
    print(out_text)

def qa_generate(query,kv):
    input_text=p_kve.format(query,kv)
    inputs=tokenizer(input_text, return_tensors="pt")
    out = model.generate(
        input_ids=inputs["input_ids"]
    )
    out_text = tokenizer.decode(out[0])
    print(out_text)

# def evaluator(query,ans,ground_truth):
#     input_text=p_kve.format(query,ans,ground_truth)
#     inputs=tokenizer(input_text, return_tensors="pt")
#     out = model.generate(
#         input_ids=inputs["input_ids"].to(device)
#     )
#     out_text = tokenizer.decode(out[0])
#     print(out_text)

if __name__ == '__main__':
    doc="One Law for the Woman is a 1924 American silent western film directed by Dell Henderson and starring Cullen Landis, Mildred Harris and Cecil Spooner."
    query="Which country the director of film One Law For The Woman is from?"
    kv_extract(doc,query)
    pass
