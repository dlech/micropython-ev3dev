
from project import motor
from project import variables

# My Blocks
from print_a import print_a
from print_b import print_b
from print_c import print_c
from print_d import print_d
from print_e import print_e
from print_f import print_f
from print_g import print_g
from print_h import print_h
from print_i import print_i
from print_j import print_j
from print_k import print_k
from print_l import print_l
from print_m import print_m
from print_n import print_n
from print_o import print_o
from print_p import print_p
from print_q import print_q
from print_r import print_r
from print_s import print_s
from print_t import print_t
from print_u import print_u
from print_v import print_v
from print_w import print_w
from print_x import print_x
from print_y import print_y
from print_z import print_z
from print_space import print_space
from carriage_move import carriage_move
from line_feed import line_feed


def print_letter(letter):
    """Prints a letter. The input variable is the index of the letter to print.

    The letters from A to Z are indexed at 0 (so A=0, B=1, etc).

    There are currently 2 addition special 'characters'.

    26 will 'print' a space
    27 will execute a 'new line'

    You are free to add any additional special characters here.

    The pen should be positioned at the top left corner of the letter box
    before calling this myblock.

    After printing the letter, the pen will be moved to the position of the
    next letter. If it is at the end of the line, it will automatically move
    the pen to the beginning of the next line.
    """
    variables['LastLetterWidth'] = variables['Seg4']
    variables['LetterSpacing'] = 20
    if letter == 0:
        print_a(1)
    elif letter == 1:
        print_b(1)
    elif letter == 2:
        print_c(1)
    elif letter == 3:
        print_d(1)
    elif letter == 4:
        print_e(1)
    elif letter == 5:
        print_f(1)
    elif letter == 6:
        print_g(1)
    elif letter == 7:
        print_h(1)
    elif letter == 8:
        print_i(1)
        variables['LastLetterWidth'] = 0
    elif letter == 9:
        print_j(1)
    elif letter == 10:
        print_k(1)
    elif letter == 11:
        print_l(1)
    elif letter == 12:
        print_m(1)
    elif letter == 13:
        print_n(1)
    elif letter == 14:
        print_o(1)
    elif letter == 15:
        print_p(1)
    elif letter == 16:
        print_q(1)
    elif letter == 17:
        print_r(1)
    elif letter == 18:
        print_s(1)
    elif letter == 19:
        print_t(1)
    elif letter == 20:
        print_u(1)
    elif letter == 21:
        print_v(1)
    elif letter == 22:
        print_w(1)
    elif letter == 23:
        print_x(1)
    elif letter == 24:
        print_y(1)
    elif letter == 25:
        print_z(1)
    elif letter == 26:
        if variables['LinePosition'] == 0:
            variables['LetterSpacing'] = 0
            variables['LastLetterWidth'] = 0
        else:
            print_space(1)
    elif letter == 27:
        carriage_move(0)
        line_feed()
        variables['LetterSpacing'] = 0

    # Move the pen to accommodate the letter spacing, and update all the
    # variables tracking the position of the pen on the line.
    letter_spacing = variables['LetterSpacing']
    motor['A'].on_for_degrees(20, letter_spacing)
    line_position = (variables['LastLetterWidth'] + variables['LinePosition'] +
                     letter_spacing)
    variables['LinePosition'] = line_position
    # Do an automatic new line if we are at the end of the current line.
    if line_position > variables['LineWidth']:
        carriage_move(0)
        line_feed()
