# rmbc-chess-bot
Final Project for Georgia Tech CS {4,7}649 Recon Blind Multi Chess AI Bot.  
The bot comprises primarily of two parts, sensing and decision making.  
Sensing is modeled using exact inference with bayesian propagation of each individual chess piece probability. Particle filter is not employed due to the discrete and limited number of state space in the game. Sensing decision is made using the action that minimizes entropy across the board.  
Decision Making is implemented using adversarial search, aka Minimax search. Since the play time is limited, the search is limited by depth and time.   
Run python play_game.py [PLAYER 1 py FILE] [PLAYER 2 py FILE] to execute
