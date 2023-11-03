from transformers import LlamaTokenizer

model_path = '/f_ndata/zekai/models/CodeLlama-7b-hf'
tokenizer = LlamaTokenizer.from_pretrained(model_path)

special_tokens = ["<face>","</face>","<loop>","</loop>",'type="outer"','type="inner"','<Line>','<Arc>','<Cricle>']
for i in range(20):
    special_tokens.append(f"<node{i}>")
for i in range(201):
    special_tokens.append(f"{i}")
    special_tokens.append(f"-{i}")
tokenizer.add_tokens(special_tokens,special_tokens=True)

code_str = """# define nodes
<node0> (-134,-42)
<node1> (-134,-134)
<node2> (89,-134)
<node3> (-22,-88)
<node4> (23,23)

# draw face
<face>
<loop type="outer"> <Line> <node0> <node1> </loop>
<loop type="outer"> <Line> <node1> <node2> </loop>
<loop type="outer"> <Arc> <node2> <node4> <node3> <node0> </loop>
</face>
"""

def tokenize(str):
    x = tokenizer.tokenize(str)
    return len(x)
    # print(f'Token Length = {len(x)}')
    # print(x)

# tokenize(code_str)





