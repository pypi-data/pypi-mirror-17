Genedoku
========

Solve sudokus of any size using genetic algorithms with an easy approach

Basic usage
-----------

.. code:: python

    from genedoku.Evolution import Evolution
    from genedoku.SudokuChromosome import SudokuChromosome

    e = Evolution(problem, SudokuChromosome, 50, 20000)
    r = e.start()

Where problem contains an array of NxN representing the sudoku and using
0 in the empty spaces.

Test
----

.. code:: bash

    python tests/test_genedoku.py [options] < tests/example.txt

Where example.txt it's an input file containing the matrix in the
following format:

Each row it's separated by '', each element in row per ' ' and the final
line should be blank. Empty spaces are 0


