#lint.py 
import sys 
from pylint import lint  

THRESHOLD = 7

run = lint.Run(["sorting_battle_gym/relu.py"], do_exit=False) 
score = run.linter.stats.global_note

if score < THRESHOLD: 
    print("Linter failed: Score:", score) 
    sys.exit(1) 
else:
    print("Linter passed: Score:", score)
    sys.exit(0)