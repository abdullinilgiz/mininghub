import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
CONF_DIR = os.path.join(ROOT_DIR, 'data', 'active', 'not_confident')

files = os.listdir(CONF_DIR)
output = open('train.txt', 'w')
for file in files:
    split = file.split('.')
    if split[1] == 'png':
        file = 'data/obj_train_data/' + file + '\n'
        output.write(file)
