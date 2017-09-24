=====
Wires
=====


There are two types of wires in the EV3-G software. **Data Wires** connect the
output parameter of one block to the input parameter of another block.
**Sequence Wires** control which block is next in the sequence of program
execution.


.. highlight:: python


Data Wires
==========

In Python, we use local variables (as opposed to global variables) to represent
**Data Wires**.

.. todo:: Add example with screenshot from EV3-G that shows how you would do
    this. The example should show something with a timer so we can explain
    when local variables are needed and when direct assignment can be used
    without a local variable. Example::

        start_value = sensor['A'].read_value()
        time.sleep(1)
        end_value = sensor['A'].read_value()
        change = end_value - start_value
        display.draw_text(change)


Sequence Wires
==============

In Python, the program flow is from one line to the next from top to bottom.
To perform two things in parallel, use the :py:meth:`uev3dev.util.fork`
function. To do this, you will need to create a function for each "chunk" of
code, like this::

    from uev3dev.util import fork

    def program():
        # maybe some other code here first

        def thread1():
            # first chunk of code
            pass

        def thread2():
            # second chunk of code
            pass

        # this runs thread1 and thread2 at the same time
        fork(thread1, thread2)
        # the program below here will not continue until both thread1
        # and thread 2 have finished

        # maybe some more code here
