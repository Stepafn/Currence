import os

env_variables = os.environ

for key, value in env_variables.items():
    print(f'{key}={value}')