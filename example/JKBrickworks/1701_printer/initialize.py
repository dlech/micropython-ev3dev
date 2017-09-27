
# project
from project import status_light
from project import variables

# My Blocks
from text_size import text_size


def initialize():
    """Initialize all of the variables that are used by the program. MUST be
     called before doing anything else.
    """

    # You can customize the 'LetterSpacing' and 'text_size' variables,
    # but should probably leave the others as they are.
    status_light.off()
    variables['LinePosition'] = 525
    variables['LineWidth'] = 1050
    variables['LetterSpacing'] = 20
    text_size(10)

    # These are all the pre-programmed text arrays for the 'PrintTestPage'
    # program. As well as some that are unused. They are just arrays of letter
    # index values that can be copied into the letter queue for processing.
    variables['QuickFox'] = (19, 7, 4, 26, 16, 20, 8, 2, 10, 26, 1, 17, 14,
                             22, 13, 26, 5, 14, 23, 26, 9, 20, 12, 15, 4, 3,
                             26, 14, 21, 4, 17, 26, 19, 7, 4, 27, 11, 0, 25,
                             24, 26, 3, 14, 6, 27)
    variables['JKBrickworks'] = (9, 10, 26, 1, 17, 8, 2, 10, 22, 14, 17, 10,
                                 18, 27)
    variables['KeepBuilding'] = (10, 4, 4, 15, 26, 14, 13, 26, 1, 20, 8, 11,
                                 3, 8, 13, 6, 27)
    variables['Alphabet'] = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
                             15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25)
    variables['Mindstorms'] = (12, 8, 13, 3, 18, 19, 14, 17, 12, 18, 27)
    variables['HelloWorld'] = (7, 4, 11, 11, 14, 26, 22, 14, 17, 11, 3, 27)
    variables['QPosition'] = 0
    variables['Queue'] = ()
    variables['QCount'] = len(variables['Queue'])

    # These variables are used to manage the state of the program. They should
    # not be changed.
    variables['Code'] = (0,)
    variables['Encoding'] = False
    variables['NewCharacter'] = 0
    variables['EStop'] = False
