Simple state machine implementation using generators.

## Examples
A state machine that does not require any input
```python
from smachine import Machine
class NeighbourhoodMachine(Machine):
    initial = 'bird'

    def state_dog(self, pstate, context):
        if pstate is None:
            print 'dog chases cat'
            return 'cat'
        elif pstate == 'bird':
            print 'dog catches bird'
            return 'stop'

    def state_cat(self, pstate, context):
        if pstate is 'dog':
            print 'cat runs'
        else:
            print 'cat pounces bird'
        return 'bird'

    def state_bird(self, pstate, context):
        if pstate == 'cat':
            print 'bird flies away'
            return 'stop'
        elif pstate == 'dog':
            print 'bird dies'
            return 'stop'
        else:
            print 'bird pecks seeds'
            return 'dog'


machine = NeighbourhoodMachine() 

print "Run machine (initial == default i.e. 'bird')"
machine.run_no_input()
print

print "Run machine (initial == 'cat')"
machine.run_no_input(initial='cat')
print

print "Run machine (initial == 'dog')"
machine.run_no_input(initial='dog')
```

Running it from the commandline yields:
```
Run machine (initial == default i.e. 'bird')
bird pecks seeds
dog catches bird

Run machine (initial == 'cat')
cat pounces bird
bird flies away

Run machine (initial == 'dog')
dog chases cat
cat runs
bird flies away
```

And one that plays a guessing game with the user.

```python
from smachine import Machine

class GuessingGame(Machine):
    initial = 'start'

    def __init__(self, secret):
        self.secret = secret

    def state_start(self, pstate, context):
        print 'Guess the secret number: ',
        (args, kwargs) = yield # Await input from outside 
        if args[0] == self.secret:
            yield 'correct'
        else:
            context['less'] = args[0] < self.secret
            yield 'incorrect'

    def state_incorrect(self, pstate, context):
        if context['less']:
            print 'Wrong, try going larger.'
        else:
            print 'Wrong, try going smaller.'
        return 'start'

    def state_correct(self, pstate, context):
        print 'You guessed it!'
        return 'stop'

game = GuessingGame(10)

for (state, context) in game.run():
    game.send(int(raw_input()))

```

Supposing we run it with the input 5, 14 and 10.

```
Guess the secret number:  5
Wrong, try going larger.
Guess the secret number:  14
Wrong, try going smaller.
Guess the secret number:  10
You guessed it!
```

## API

```
def run(self, initial=None, context=None):
    """ Runs the machine, yielding on input."""

def run_no_input(self, initial=None, context=None):
    """
    Runs the machine; raising an exception if it requires input at any point during its execution.
    """

def send(self, *args, **kwargs):
    """
    Sends (args, kwargs) as a value to the state function of the machine 
    that is waiting on input
    """
```

## Extension
The functions `new_context`, `function`, `stopped` and `paused` can be overriden with
custom alternatives. 

