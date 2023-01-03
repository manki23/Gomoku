# include "globals.hpp"
# include "Game.hpp"

# include <chrono>

typedef std::map<std::string, int > mapEval;
typedef std::vector<std::vector<std::string > > debugArray;

# define DEBUG false

int getBoardEval(Game * g)
{
    /*
    std::ostringstream ss;
    for (std::map<int, coordSet>::const_iterator it = g->stone_list.begin();
    it != g->stone_list.end(); it++)
    {
        for (coordSet::const_iterator its = it->second.begin();
        its != it->second.end(); its++)
            ss << std::to_string(it->first) << std::to_string(its->first) << std::to_string(its->second);
    }

    std::map<std::string, int>::const_iterator pos = g->transposition_table.find(ss.str());
    if (pos != g->transposition_table.end())
        return (pos->second);

    std::cout << ss.str() << std::endl;
    */
	mapEval player = getPatternDict(g, g->player, g->opponent);
	mapEval opponent = getPatternDict(g, g->opponent, g->player);

	int score = (600000 * (player["fiveInRow"] - opponent["fiveInRow"]) +
				10000 * (player["liveFour"] - opponent["liveFour"]) +
				2100 * (player["deadFour"] - opponent["deadFour"]) +
				2000 * (player["liveThree"] - opponent["liveThree"]) +
				700 * (player["deadThree"] - opponent["deadThree"]) +
				250 * (player["liveTwo"] - opponent["liveTwo"]) +
				10 * (player["deadTwo"] - opponent["deadTwo"]) -
				5 * (player["uselessOne"] - opponent["uselessOne"]) +
				1000 * (player["captures"] - opponent["captures"])
			);

    //g->transposition_table[ss.str()] = score;
	return score;
}

int minimax(Game * g, int depth, int alpha, int beta, bool maximizingPlayer, int * count)
{
    *count += 1;
	if (depth == 0 || g->game_over)
	{
		int boardEval = getBoardEval(g);
		return boardEval;
	}
	
	coordSet playable_area_copy = g->playable_area;
    int score;
	for (coordSet::const_iterator it = playable_area_copy.begin();
		it != playable_area_copy.end(); it++)
	{
		g->playOneMove(it->first, it->second);

        if (maximizingPlayer)
		    score = minimax(g, depth - 1, alpha, beta, !maximizingPlayer, count);
        else
            score = minimax(g, depth - 1, alpha, beta, !maximizingPlayer, count);
        
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
    int count = 0;

    debugArray debug(19, std::vector<std::string>(19));
    if (DEBUG)
    {
        for (int i = 0; i < 19; i++)
            for (int j = 0; j < 19; j++)
                debug[i][j] = "0";
    }

    auto start = std::chrono::high_resolution_clock::now();

	int alpha = INT_MIN;
	int beta = INT_MAX;

	coordSet playable_area_copy = g->playable_area;

	int score;
	int depth = 3;

    int numberOfMoves = 0;

	for (coordSet::const_iterator it = playable_area_copy.begin();
		it != playable_area_copy.end(); it++)
	{
		int x = it->first;
		int y = it->second;

		g->playOneMove(x, y);

        numberOfMoves += 1;

		score = minimax(g, depth - 1, alpha, beta, false, &count);

        if (DEBUG)
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

    std::cout << "NODES VISITED : " << count << std::endl;

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
				std::cout << debug[i][j] << "\t";
			std::cout << std::endl;
		}
        std::cout << "NUMBER OF MOVES : " << numberOfMoves << " / " << playable_area_copy.size() << std::endl;
        int brk;
        std::cin >> brk;
        for (coordSet::const_iterator it = g->playable_area.begin();
        it != g->playable_area.end(); it++)
            std::cout << " " << it->first << " " << it->second << " ";
        std::cout << std::endl;
	}
    //int brk;
    //std::cin >> brk;
	std::cout << "NUMBER OF MOVES : " << numberOfMoves << " / " << playable_area_copy.size() << std::endl;	
	g->best_move = best_move;
	auto stop = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration<double>(stop - start);
    std::cout << "Elapsped time : " << duration.count() << std::endl;
	return best_move;

	

}