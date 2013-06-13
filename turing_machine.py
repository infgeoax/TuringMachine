# coding=utf-8
__author__ = 'infgeoax'

class Tape:
    def __init__(self, tape_right=None, tape_left=None, cursor=0):
        if not tape_left: tape_left = [None]
        if not tape_right: tape_right = [None]

        self.__tape_right = tape_right
        self.__tape_left = tape_left
        self.__cursor = cursor

    def __str__(self):
        return 'Cursor: {0}.\nRight Tape: {1}\nLeft Tape: {2}'.format(self.__cursor, self.__tape_right, self.__tape_left)


    def __ensure_tape_size__(self):
        """
        Called in the beginning of Print to make sure that there's enough tape for cursor not to go over the cliff.
        """
        while self.__cursor >= len(self.__tape_right):
            self.__tape_right.extend([None]*len(self.__tape_right))
        while self.__cursor < -len(self.__tape_left):
            self.__tape_left.extend([None]*len(self.__tape_left))

    def Read(self):
        """
        Read the symbol under cursor. None if it is out of the tape.
        """
        if self.__cursor >= 0:
            if self.__cursor < len(self.__tape_right):
                return self.__tape_right[self.__cursor]
            else:
                return None
        else:
            c = -(self.__cursor+1)
            if c < len(self.__tape_left):
                return self.__tape_left[c]
            else:
                return None

    def Erase(self):
        self.Print(None)

    def Print(self, symbol):
        self.__ensure_tape_size__()
        if self.__cursor >= 0:
            self.__tape_right[self.__cursor] = symbol
        else:
            c = -(self.__cursor+1)
            self.__tape_left[c] = symbol


    def Forward(self, steps = 1):
        self.__cursor += steps

    def Backward(self, steps = 1):
        self.Forward(-steps)

    P0 = (Print, '0')
    P1 = (Print, '1')
    P2 = (Print, '2')
    P3 = (Print, '3')
    P4 = (Print, '4')
    P5 = (Print, '5')
    P6 = (Print, '6')
    P7 = (Print, '7')
    P8 = (Print, '8')
    P9 = (Print, '9')

    Px = (Print, 'x')
    Py = (Print, 'y')
    Pz = (Print, 'z')

    R  = Forward
    L  = Backward


class TuringMachine:

    def __init__(self, initial_state, instruction_table):
        """
        """
        self.__tape = Tape()
        self.__cur_state  = initial_state
        self.__inst_table = instruction_table

    def Step(self):
        s = self.__tape.Read()
        inst = self.__inst_table[self.__cur_state]
        if isinstance(inst, dict):
            actions, final_state = inst[s] if inst.has_key(s) else inst[None]
        else:
            actions, final_state = inst
        if callable(actions):
            actions(self.__tape)
        else:
            for action in actions:
                if callable(action):
                    action(self.__tape)
                elif isinstance(action, tuple) or isinstance(action, list):
                    action[0](self.__tape, *action[1:])
                else:
                    raise Exception()
        self.__cur_state = final_state

    def __str__(self):
        return 'Turing Machine\nTM State: {0}\n{1}'.format(self.__cur_state, self.__tape)

if __name__=='__main__':
    it ={
        'b':{
            None:  ((Tape.P0,),
                    'b'),
            '0':    ([Tape.R, Tape.R, Tape.P1],
                     'b'),
            '1':    ((Tape.R, Tape.R, Tape.P0),
                     'b')
            }
        }
    tm = TuringMachine(initial_state='b', instruction_table=it)

    for i in range(20):
        tm.Step()
        print tm
        print '-'*20
