# coding=utf-8
__author__ = 'infgeoax'

class Tape(object):
    def __init__(self, tape_right=None, tape_left=None, cursor=0):
        if not tape_left: tape_left = [None]
        if not tape_right: tape_right = [None]

        self.__tape_right = tape_right
        self.__tape_left = tape_left
        self.__cursor = cursor

    def __str__(self):
        return 'Tape(cursor={0}, right_tape={1}, left_tape={2}'.format(self.__cursor, self.__tape_right, self.__tape_left)

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

    def TapeString(self):
        right_str = ''.join(filter(lambda x: x, self.__tape_right))
        left_str = ''.join(reversed(filter(lambda x: x, self.__tape_left)))
        return left_str + right_str

    def Forward(self, steps = 1):
        self.__cursor += steps

    def Backward(self, steps = 1):
        self.Forward(-steps)

    def Decode(self, encoded_tape):
        self.__cursor, self.__tape_right, self.__tape_left = eval(encoded_tape)

    def Encode(self):
        return '({0},{1},{2})'.format(self.__cursor, self.__tape_right, self.__tape_left)

    P = Print
    P0 = (P, '0')
    P1 = (P, '1')
    P2 = (P, '2')
    P3 = (P, '3')
    P4 = (P, '4')
    P5 = (P, '5')
    P6 = (P, '6')
    P7 = (P, '7')
    P8 = (P, '8')
    P9 = (P, '9')

    Px = (P, 'x')
    Py = (P, 'y')
    Pz = (P, 'z')

    R  = Forward
    R2,R3,R4,R5,R6,R7,R8,R9 = (R,2),(R,3),(R,4),(R,5),(R,6),(R,7),(R,8),(R,9)

    L  = Backward
    L2,L3,L4,L5,L6,L7,L8,L9 = (L,2),(L,3),(L,4),(L,5),(L,6),(L,7),(L,8),(L,9)

    NOP = lambda x: x

INSTRUCTION_TABLE_CONTEXT = {'Tape': Tape}
INSTRUCTION_TABLE_CONTEXT.update(Tape.__dict__)

class TuringMachine(object):

    EMPTY_INSTRUCTION_TABLE = {None:(Tape.NOP,None)}

    def __init__(self, initial_state=None, instruction_table_desc=None, tape=None):
        """
        """
        self.__tape         = Tape() if not tape else tape
        self.__cur_state    = initial_state
        self.__program_counter        = 0
        self.LoadInstructionTable(instruction_table_desc)

    def __str__(self):
        return 'Turing Machine(steps={2}, state=`{0}`, tape={1})'.format(self.__cur_state, self.__tape, self.__program_counter)

    def __get_tape__(self):
        return self.__tape

    tape = property(fget=__get_tape__)

    def cleanup_input_string(self, str):
        if str:
            return str.replace('\n', '').strip()
        else:
            return str

    def LoadInstructionTable(self, inst_tab_desc):
        inst_tab_desc = self.cleanup_input_string(inst_tab_desc)
        self.__inst_table = eval(inst_tab_desc, INSTRUCTION_TABLE_CONTEXT) \
                                if inst_tab_desc \
                                else TuringMachine.EMPTY_INSTRUCTION_TABLE
        self.__inst_table_str = inst_tab_desc if inst_tab_desc else ''

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
                elif isinstance(action, (list,tuple)):
                    action[0](self.__tape, *action[1:])
                else:
                    raise Exception()
        self.__cur_state = final_state
        self.__program_counter += 1

    def Encode(self):
        return '({0},{1},{2},{3})'.format(repr(self.__cur_state), repr(self.__program_counter), repr(self.__inst_table_str), repr(self.__tape.Encode()))

    def Decode(self, tm_encode):
        tm_encode = self.cleanup_input_string(tm_encode)
        tm_tuple = eval(tm_encode)

        tape_encode, inst_table_desc = None, None

        if len(tm_tuple) == 4:
            self.__cur_state, inst_table_desc, self.__program_counter, tape_encode = tm_tuple
        elif len(tm_tuple) == 3:
            self.__cur_state, inst_table_desc, tape_encode = tm_tuple
        elif len(tm_tuple) == 2:
            self.__cur_state, inst_table_desc = tm_tuple

        if tape_encode:
            self.__tape.Decode(tape_encode)
        if inst_table_desc:
            self.LoadInstructionTable(inst_table_desc)

import codecs
def read_encoded_tm(f):
    if not isinstance(f, file):
        f = file(f)
    lines = []
    utf8_file = codecs.getreader('utf-8')(f)
    with utf8_file:
        for line in utf8_file:
            i = line.find('#')
            if i >= 0:
                line = line[:i]
            lines.append(line)
    return ''.join(lines)


if __name__=='__main__':
    import sys

    tm = TuringMachine()

    max_steps = 10

    if len(sys.argv) > 1:
        tm.Decode(read_encoded_tm(sys.argv[1]))

        if len(sys.argv) > 2:
            max_steps = int(sys.argv[2])

        for i in range(max_steps):
            tm.Step()

        sys.stderr.write(tm.tape.TapeString())

    else:
        print 'Usage: python %s encoded_tm_file(utf-8) [max steps, default 10]' % __file__


