# actions
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

MAPS = {
    "3x4": [
        "EEEG",
        "EXEH",
        "SEEE",
    ],
    "4x4": [
        "GEEE",
        "EEEE",
        "EEEE",
        "EEEG",
    ],
    "5x4": [
        "GEEE",
        "EEEE",
        "EEEE",
        "EEEG",
        "XEXX",
    ]
}


class ClassicGridEnv(discrete.DiscreteEnv):
    """
    Example Gridworld:

        EEEG
        EXEH
        SEEE

    S : starting cell
    E : empty cell
    H : hole
    G : goal
    X : obstacle

    The episode ends when the agent reaches a terminal state (goal or pit). The agent
    receives a reward when transitioning in the environment. See below for details.

    Rewards r(s, a, s'):
        3x4:
            r(goal,any action, s') = 1
            r(pit, any action, s') = -1,
            r(nonterminal state, any action, s') =  -0.1

        4x4 or 5x4:
            r(nonterminal state, any action, s') =  -1
    """

    metadata = {'render.modes': ['human', 'ansi']}


    def __init__(self, desc=None, map_name=None, is_noisy=False, nrew=-0.1):
        if desc is None and map_name is None:
            raise ValueError('Must provide either desc or map_name')
        elif desc is None:
            desc = MAPS[map_name]
        self.desc = desc = np.asarray(desc, dtype='c')
        self.nrow, self.ncol = nrow, ncol = desc.shape
        self.reward_range = (-1, 1)

        nA = 4
        nS = nrow * ncol
        nS+=1

        #initial state distribution
        isd = np.array(desc == b'S').astype('float64').ravel()
        isd /= isd.sum()

        # Empty dict of dict of lists for environment dynamics
        P = {s: {a : [] for a in range(nA)} for s in range(nS)}
        # Terminal state
        P[-1] = {
        0: [(1.0, -1, 0.0, True)],
        1: [(1.0, -1, 0.0, True)],
        2: [(1.0, -1, 0.0, True)],
        3: [(1.0, -1, 0.0, True)]
        }

        def to_s(row, col):
            return row*ncol + col

        def inc(row, col, a):
            # left
            if a == 0:
                col = max(col-1, 0)
            # down
            if a == 1:
                row = min(row+1, nrow-1)
            # right
            if a == 2:
                col = min(col+1, ncol-1)
            if a == 3:
                row = max(row-1, 0)
            return (row, col)

        # create state-transition probabilities
        for row in range(nrow):
            for col in range(ncol):
                s = to_s(row, col)
                for a in range(nA):
                    li = P[s][a]
                    letter = desc[row, col]
                    if letter == b'G':
                        li.append((1.0, -1, 1, False))
                    elif letter == b'H':
                        li.append((1.0, -1, -1, False))
                    elif letter == b'X':
                        li.append((0.0, s, 0, False))
                    else:
                        if is_noisy:
                            for b in [(a-1)%4, a, (a+1)%4]:
                                newrow, newcol = inc(row, col, b)
                                newletter = desc[newrow, newcol]
                                if newletter == b'X':
                                    newrow, newcol = row, col
                                    newletter = desc[newrow, newcol]
                                newstate = to_s(newrow, newcol)
                                done = bytes(newletter) in b'GH'
                                done = False
                                rew = nrew
                                li.append((0.8 if b == a else 0.1, newstate, rew, done))
                        else:
                            newrow, newcol = inc(row, col, a)
                            newletter = desc[newrow, newcol]
                            if newletter == b'X':
                                newrow, newcol = row, col
                                newletter = desc[newrow, newcol]
                            newstate = to_s(newrow, newcol)
                            newletter = desc[newrow, newcol]
                            done = bytes(newletter) in b'GH'
                            if map_name == "3x4":
                                rew = float(newletter == b'G') - float(newletter == b'H') + nrew * (float(newletter != b'G') * float(newletter != b'H'))
                            else:
                                rew = float(newletter == b'G') - 1
                            li.append((1.0, newstate, rew, done))

        super(ClassicGridEnv, self).__init__(nS, nA, P, isd)

    def render(self, mode='human'):
        outfile = StringIO() if mode == 'ansi' else sys.stdout

        row, col = self.s // self.ncol, self.s % self.ncol
        desc = self.desc.tolist()
        desc = [[c.decode('utf-8') for c in line] for line in desc]
        desc[row][col] = utils.colorize(desc[row][col], "red", highlight=True)
        if self.lastaction is not None:
            outfile.write("  ({})\n".format(["Left","Down","Right","Up"][self.lastaction]))
        else:
            outfile.write("\n")
        outfile.write("\n".join(''.join(line) for line in desc)+"\n")

        if mode != 'human':
            return outfile


class ClassicGridEnv3x4(ClassicGridEnv):
    def __init__(self, nrew):
        super(ClassicGridEnv3x4, self).__init__(map_name="3x4", is_noisy=True, nrew=nrew)

class ClassicGridEnv4x4(ClassicGridEnv):
    def __init__(self):
        super(ClassicGridEnv4x4, self).__init__(map_name="4x4", is_noisy=False)

class ClassicGridEnv5x4Static(ClassicGridEnv):
    """
    Do not allow agent to move from cell 13 to cell 15 (17 in array).
    """
    def __init__(self):
        super(ClassicGridEnv5x4Static, self).__init__(map_name="5x4", is_noisy=False)
        self.P[13][1] =  [(1.0, 13, -1.0, False)]
        # State 15 is state 17
        self.P[17] = {
        0: [(1.0, 12, -1.0, False)],
        1: [(1.0, 17, -1.0, False)],
        2: [(1.0, 14, -1.0, False)],
        3: [(1.0, 13, -1.0, False)]
        }

class ClassicGridEnv5x4Dynamic(ClassicGridEnv):
    """
    Allow agent to move from cell 13 to cell 15 (17 in array).
    """
    def __init__(self):
        super(ClassicGridEnv5x4Dynamic, self).__init__(map_name="5x4", is_noisy=False)
        self.P[17] = {
        0: [(1.0, 12, -1.0, False)],
        1: [(1.0, 17, -1.0, False)],
        2: [(1.0, 14, -1.0, False)],
        3: [(1.0, 13, -1.0, False)]
        }
