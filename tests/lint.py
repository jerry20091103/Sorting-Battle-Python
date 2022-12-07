#lint.py 
import sys 
import os
from pylint import lint  

THRESHOLD = 7

test_files = [os.path.join('sorting_battle_gym', file) for file in os.listdir('sorting_battle_gym')]
test_files.extend([os.path.join('training', file) for file in os.listdir('training')])
# get every .py file
test_files = [file for file in test_files if file.endswith('.py') and not file.startswith('__init__')]
# add the path to the files
#test_files = [os.path.join('sorting_battle_gym', file) for file in test_files]

run = lint.Run(test_files, do_exit=False) 
score = run.linter.stats.global_note

if score < THRESHOLD: 
    print("Linter failed: Score:", score) 
    sys.exit(1) 
else:
    print("Linter passed: Score:", score)
    sys.exit(0)