# ChangeTools (Python)

Change evaluation functions and decorators.

## Direct example:

```
>>> from pathlib import Path
>>> from functools import partial
>>> from changetools import ChangeEvaluator
>>> hello_path = Path('hello.txt')
>>> _ = hello_path.write_text('hello')
>>> change_evaluator = ChangeEvaluator(partial(hello_path.read_text))
>>> change_evaluator.changed
True
>>> change_evaluator.changed
False
>>> _ = hello_path.write_text('hi')
>>> change_evaluator.changed
True
>>> change_evaluator.changed
False
```

## While example:

```
>>> hello_path = Path('hello.txt')
>>> change_evaluator.changed
KeyboardInterrupt
>>> _ = hello_path.write_text('hello')
>>> change_evaluator = ChangeEvaluator(partial(hello_path.read_text))
>>> while change_evaluator.changed:
...   _ = hello_path.write_text('hi')
...
```

## For example using `cycle`:

```
>>> hello_path = Path('hello.txt')
>>> change_evaluator = ChangeEvaluator(partial(hello_path.read_text))
>>> _ = hello_path.write_text('hello')
>>> for i in change_evaluator.cycle(10):
...   print(i)
...   _ = hello_path.write_text('hi')
...
0
1
```
