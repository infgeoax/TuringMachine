# Anything after '#' is a comment.

# The programming model is too prevalent to be repeated here.
# It is time for implementation-specific details.

# A TuringMachine Program :: ( <Initial State>, <Instruction Table>, [<Program Counter>,] [<Tape Description>] )
# Initial State:: A key to the instruction table, the initial state of the TM.
# Program Counter:: Optional field, default 0, remembers the number of steps a TM has run.
# Instruction Table:: { <TM State>: <Symbol-Actions-State Table>, ... }
#   Symbol-Actions-State Table:: { <Symbol at cursor>: (<Actions>, <Next-State>), ... }
#   Actions:: [<Instruction>, ...]
#   Instruction:: NOP,R,R2~R9,L,L2~L9,Print,P0~P9,Px,Py,Pz,Erase/E,(R|L|P,<Arg>)
# Tape Description:: (<Cursor Position>, <Right Tape>, <Left Tape>)

# Instruction Reference
# * Print & Erase at cursor
#   (Print, s) - Prints symbol s under cursor, where s is usually a string of length 1, or any valid python value.
#       -- P0~P9, Px, Py, Pz are short-hands for (Print, 0), (Print, 1), ..., (Print, 9), (Print, 'x'), (Print, 'y'), (Print, 'z')
#   E/Erase - Removes symbol under cursor, the same as (Print, None).
# * Tape cursor movement
#   Forward/R - Moves cursor one step to the right;
#   Backward/L - Moves cursor one step to the left;
#   (R/L, x) - Moves cursor x steps.
#   R2~R9 - are short-hands for (R,2), (R,3), ..., (R,9)
#   L2~L9 - are short-hands for (L,2), (L,3), ..., (L,9)
# * NOP - does nothing.

# Here is a program that calculates the binary representation of 1/3.
(
    # initial state
    'b',
    # Instruction table
    u"{ 'b': { None: ([P0,],    'b'),
               '0':  ([R2,P1], 'b'),
               '1':  ([R2,P0], 'b'), } }",

    # Program counter, optional, default 0.
    # 0,
    # Tape description, optional, default: '(0,[None],[None])'
    # '(0,[None],[None])'
)
