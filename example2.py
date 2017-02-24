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
