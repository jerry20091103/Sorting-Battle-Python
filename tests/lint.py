#lint.py 
import sys 
from pylint import lint  

THRESHOLD = 8

run = lint.Run(["src/relu.py"], do_exit=False) 
score = run.linter.stats["global_note"]

if score < THRESHOLD: 
    print("Linter failed: Score:", score) 
    sys.exit(1) 
else:
    print("Linter passed: Score:", score)
    sys.exit(0)