================
The Project File
================

In the EV3-G software, projects are saved in a single file with the ``.ev3``
file extension. The **Project Properties** page shows all of the components
that make up the project: **Programs**, **Images**, **Sounds**, **My Blocks**
and **Variables**.

.. todo:: Screenshot of EV3-G Project Properties

To convert this to **µev3dev**, we will have a folder that contains our project
with the following contents:

* A ``.py`` file for each **Program**.
* A ``.bmp`` file for each **Image**
* A ``.wav`` file for each **Sound**
* A ``.py`` file for each **My Block**
* A special ``project.py`` file for **Variables** (and a few other things)

It should look something like this::

    .
    └── project
        ├── image.bmp
        ├── my_block.py
        ├── program.py
        ├── project.py
        └── sound.wav

.. tip:: It is conventional to use all lower-case file names with underscores
    in Python.


.. highlight:: python


Programs
========

The ``.py`` file for each program should follow this template::

    #!/usr/bin/env micropython

    # Import standard (micro)python modules if needed
    import utime

    # Import brick interface and global variables
    from project import brick
    from project import variables

    # Import any My Blocks used in this program
    from my_block import my_block

    # Define a function that will contain your program logic
    def program():
        pass

    # This will call the program when we run this file
    if __name__ == '__main__':
        program()

.. tip:: The first line is called a **shebang** (``#!``). It is a special header
    that says which program should be used to run this file. In this case we are
    using ``micropython``.

.. warning:: If you are writing your program on Windows, be sure to use a text
    editor that allows you to use "Unix" or "LF" line endings. If your file
    is saved with "Windows" or "CRLF" line endings, the magic shebang line
    will not work correctly and your program will not run.


Images
======

.. todo:: Images are not yet implemented in **µev3dev**.



Sounds
======

.. todo:: Sounds are not yet implemented in **µev3dev**.



My Blocks
=========

The ``.py`` file for each My Block should follow this template::

    # Import standard (micro)python modules if needed
    import utime

    # Import brick interface and global variables
    from project import brick
    from project import variables

    # Import any other My Blocks used in this My Block
    from my_block2 import my_block2

    # Define a function that will contain your My Block logic
    def my_block(in1, in2):
        return out1, out2

.. tip:: ``in1`` and ``in2`` represent input parameters to the My Block. Give
    them useful names or omit them if you don't have any input parameters.
    Likewise, ``out1`` and ``out2`` are output parameters. If you don't have
    any, omit the ``return`` statement.

Variables
=========

The global variables are defined as a dictionary in a special ``project.py``
file::

    # global variables
    variables = {
        'Text1': '',
        'Numeric1': 0,
        'Logic1': False,
        'NumericArray1': [],
        'LogicArray': [],
    }

.. tip:: Initialize text variables with an empty string (``''``), numeric
    variables with ``0``, logic variables with ``False`` and array variables
    (both numeric and logic) with an empty list (``[]``).


The Brick
=========

The programmable brick and all of its parts are inherent in the EV3-G software.
There is nothing like this built into **µev3dev**, so we create another
dictionary in ``project.py`` to represent the brick. The motors and sensors
should be configured to look like the **Port View** in EV3-G plus any any motor
combinations used by steering or tank blocks. The buttons, light and sound will
always be the same. It looks like this::

    from uev3dev.button import Buttons
    from uev3dev.led import StatusLight
    from uev3dev.motor import LargeMotor
    from uev3dev.motor import MediumMotor
    from uev3dev.motor import Tank
    from uev3dev.sensor import EV3ColorSensor
    from uev3dev.sound import Sound

    brick = {
        'motor': {
            'A': LargeMotor('A'),
            'B': LargeMotor('B'),
            'C': MediumMotor('C'),
            'D': None,
            'A+B': Tank('A', 'B'),
        },
        'sensor': {
            '1': None,
            '2': None,
            '3': None,
            '4': EV3ColorSensor('4'),
        },
        'buttons': Buttons(),
        'light': StatusLight(),
        'sound': Sound(),
    }
