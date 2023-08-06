Game of life
============

A simple pygame-based implementation of Conway's game of life.

Cmd::

    $ game-of-life


As library::

    from game_of_life import Board, run

    board = Board(30, 30)

    # Diagonal line
    for i in range(30:
        board[i, i] = 1

    run('conway')

This implementation requires Python3 and pygame.