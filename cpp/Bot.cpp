# include "globals.hpp"
# include "Game.hpp"

typedef std::map<std::string, int > mapEval;
typedef std::vector<std::vector<std::string > > debugArray;

# define DEBUG false

int getBoardEval(Game * g)
{
	mapEval player = getPatternDict(g, g->player, g->opponent);
	mapEval opponent = getPatternDict(g, g->opponent, g->player);

	int score = (600000 * (player["fiveInRow"] - opponent["fiveInRow"]) +
				10000 * (player["liveFour"] - opponent["liveFour"]) +
				1100 * (player["deadFour"] - opponent["deadFour"]) +
				900 * (player["liveThree"] - opponent["liveThree"]) +
				500 * (player["deadThree"] - opponent["deadThree"]) +
				50 * (player["liveTwo"] - opponent["liveTwo"]) +
				10 * (player["deadTwo"] - opponent["deadTwo"]) -
				10 * (player["uselessOne"] - opponent["uselessOne"]) +
				5000 * (player["captures"] - opponent["captures"])
			);

	return score;
}

int minimax(Game * g, int depth, int alpha, int beta, bool maximizingPlayer)
{
	if (depth == 0 || g->game_over)
	{
		int boardEval = getBoardEval(g);
		return boardEval;
	}
	
	coordSet playable_area_copy = g->playable_area;

	for (coordSet::const_iterator it = playable_area_copy.begin();
		it != playable_area_copy.end(); it++)
	{
		g->playOneMove(it->first, it->second);

		int score = minimax(g, depth - 1, alpha, beta, !maximizingPlayer);
        
        g->revertLastMove();
        if (maximizingPlayer)
			alpha = std::max(alpha, score);
		else
			beta = std::min(beta, score);
		
		if (beta <= alpha)
			return (maximizingPlayer ? alpha : beta);
	}
	return (maximizingPlayer ? alpha : beta);
}

coord getNextMove(Game * g)
{
	coord best_move;
	int best_score = INT_MIN;

    debugArray debug(19, std::vector<std::string>(19));
	for (int i = 0; i < 19; i++)
    {
        for (int j = 0; j < 19; j++)
            debug[i][j] = "0";
    }

	int alpha = INT_MIN;
	int beta = INT_MAX;

	coordSet playable_area_copy = g->playable_area;

	int score;
	int depth = 1;

	for (coordSet::const_iterator it = playable_area_copy.begin();
		it != playable_area_copy.end(); it++)
	{
		int x = it->first;
		int y = it->second;

		g->playOneMove(x, y);

		score = minimax(g, depth - 1, alpha, beta, false);

		debug[y][x] = std::to_string(score);

		g->revertLastMove();

		if (score > best_score)
		{
			best_score = score;
			best_move = coord(x, y);
			alpha = std::max(alpha, best_score);
		}

		if (alpha >= beta)
			break ;
	}

	if (DEBUG)
	{
		for (coordSet::const_iterator it = g->stone_list[g->player].begin();
			it != g->stone_list[g->player].end(); it++)
			debug[it->second][it->first] = "[X]";
		for (coordSet::const_iterator it = g->stone_list[g->opponent].begin();
			it != g->stone_list[g->opponent].end(); it++)
			debug[it->second][it->first] = "[O]";
		
		for (int i = 0; i < 19; i++)
		{
			// change to printf or see how to format strings
			for (int j = 0; j < 19; j++)
				std::cout << debug[i][j] << " ";
			std::cout << std::endl;
		}
	}
	g->best_move = best_move;
	return best_move;

	

}