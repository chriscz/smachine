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

print "Run machine (initial == default)"
machine.run_no_input()
print

print "Run machine (initial == 'cat')"
machine.run_no_input(initial='cat')
print

print "Run machine (initial == 'dog')"
machine.run_no_input(initial='dog')
