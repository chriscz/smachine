import inspect

class Machine(object):
    """
    Base class for state machines.
    """
    # the initial state of the machine, should be overriden by
    # subclasses
    initial = None

    def run(self, initial=None, context=None):
        """
        Runs the machine, yielding on input.
        """
        self.reset()
        if initial is None:
            initial = self.initial

        if context is None:
            context = self.new_context()

        self.state = initial
        self.context = context

        for i in self._start():
            yield i

    def run_no_input(self, initial=None, context=None):
        """
        Runs the machine; raising an exception if it requires input
        at any point during its execution.
        """
        for _ in self.run(initial, context):
            raise RuntimeError("Machine requires input to continue!")


    def send(self, *args, **kwargs):
        """
        Sends (args, kwargs) as a value to the state function of the machine 
        that is waiting on input
        """
        if not self.paused():
            raise RuntimeError("Machine is not awaiting input")
        else:
            self.args = (args, kwargs)

    def _read_args(self):
        if self.args is None:
            raise RuntimeError("Machine awaiting input!")
        args = self.args
        self.args = None
        return args

    def _start(self):
        while not self.stopped():
            function = self.function(self.state)
            value = function(self.previous, self.context)

            if value is None:
                raise RuntimeError("State function `%s` did not yield a next state!" % self.state)

            if inspect.isgenerator(value):
                gen = value
                what = None
                while True:
                    try:
                        value = gen.send(what)
                    except StopIteration:
                        raise RuntimeError("State function `%s` did not yield a next state!" % self.state)
                    if value is None:
                        yield (self.state, self.context)
                        what = self._read_args()
                    else:
                        break
            self.previous = self.state
            self.state = value

        # Machine is done!
        # yield (self.current, self.context)
        # assert self.stopped()

    def reset(self):
        """Resets the state machine to its initial state. Should not be overridden in subclasses"""
        self.previous = None
        self.state = None
        self.args = None
        self.context = None

    def new_context(self):
        """Create a new context for the state machine"""
        return dict()

    def function(self, state):
        """Return a function for the given state object"""
        if state is None:
            raise RuntimeError("state cannot be None!")

        return getattr(self, 'state_' + state)

    def stopped(self):
        """Has the state machine stopped executing?"""
        return self.state == 'stop'

    def paused(self):
        """Is the state machine in a paused state, awating input?"""
        return self.state is not None and not self.stopped()
