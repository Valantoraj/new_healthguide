import json 
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\healthcare\\diseases_info.json") as f:
    data=json.load(f)
print(len(data))
f.close()
d={}
for k,v in data.items():
    d[k.lower()]=v
with open("C:\\Users\\valan\\Videos\\athish\\athish\\hackathon\\hackathon\\health_care\\healthcare\\diseases_info.json",'w') as f:
    json.dump(d,f,indent=4)