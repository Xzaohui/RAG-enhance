import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM

device='cuda:2'

# tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-70b-chat-hf")
# model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-70b-chat-hf",device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-13b-chat-hf")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-13b-chat-hf",device_map="auto")
# model.to(device)


p_qag="""
You are a Query/Answer generator that generates new multiple Query or Answers based on origen Query, old Query and known KV informations.Continue generating queries if the Answer is not clear, and generate Answers if the Answer is clear. The Answer must be based on origen Query. Now give the old Query and KV information:
Query:{}
spo informations:{}
"""

p_kve="""
You are a Subject-Predicate-Object extractor.I will give you a Doc you will extract Subject-Predicate-Object from the Doc. If no information is available then reply []
{}
Doc:{}
SPO:
"""

p_judge="""
You are a Query and answer evaluator, and you will use one Query and two answers to determine whether their conclusions are consistent.
Query:{}
answer1:{}
answer2:{}
"""

def spo_extract(doc):
    example="""
Doc:One Law for the Woman is a 1924 American silent western film directed by Dell Henderson and starring Cullen Landis, Mildred Harris and Cecil Spooner.
SPO:
[
{"Subject":"One Law for the Woman","Predicate":"director","Object":"Dell Henderson"},
{"Subject":"One Law for the Woman","Predicate":"starring role","Object":"Cullen Landis"},
{"Subject":"One Law for the Woman","Predicate":"starring role","Object":"Mildred Harris"},
{"Subject":"One Law for the Woman","Predicate":"starring role","Object":"Cecil Spooner"},
{"Subject":"One Law for the Woman","Predicate":"premiere date","Object":"1924"},
{"Subject":"One Law for the Woman","Predicate":"country","Object":"American"},
{"Subject":"One Law for the Woman","Predicate":"theme","Object":"silent western film"},
]
"""
    input_text=p_kve.format(example,doc)
    inputs=tokenizer(input_text, return_tensors="pt")
    out = model.generate(
        input_ids=inputs["input_ids"]
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
    spo_extract(doc)
    pass
