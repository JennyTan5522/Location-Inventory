import yaml

with open('PARAMETERS_INITIALIZATION.yml','r') as f:
    PARAMETERS_INITIALIZATION=yaml.safe_load(f)


for size,value in enumerate(PARAMETERS_INITIALIZATION['PROBLEM_SIZE']):
    print(size,value)


for type,value in enumerate(PARAMETERS_INITIALIZATION['SITUATION_TYPE']):
    print(type,value)

print(PARAMETERS_INITIALIZATION['SITUATION_TYPE'])
