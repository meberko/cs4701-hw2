********************************************************************************
*           Artificial Intelligence (COMS W4701) Assignment 2: 2048            *
*                          Michael Berkowitz (meb2235)                         *
********************************************************************************

Comparison of Vanilla Minimax vs. Alpha-Beta Pruned Minimax

Overall, I was surprised at the relatively small size of the performance
increase in comparing vanilla minimax to A-B pruned minimax. Vanilla minimax
was consistently able to completely search a game state space of depth 3 but no
greater depth. Even "nervous" algorithmic optimizations in which the depth was
increased when there were less open cells on the board were unable to complete
without breaking the time limit. However, once A-B pruning was implemented,
although the algorithm was still unable to completely search a game state space
of depth > 3, it was possible to implement "nervous" optimizations and search
deeper into the state space by up to depth = 6 for 1 tile on the board.

However, as mentioned earlier, the performance increase was smaller than I
expected it to be and there would undoubtedly be benefits to trying to find
other methods of either speeding up the algorithm or minimizing the search
space.