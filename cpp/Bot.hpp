typedef std::map<std::string, int > mapEval;
typedef std::vector<std::vector<std::string > > debugArray;

# define DEBUG false

namespace Bot
{
    int getBoardEval(Game const * g)
    {
        mapEval player = CheckHeuristic::getPatternDict(g, g->player, g->opponent);
        mapEval opponent = CheckHeuristic::getPatternDict(g, g->opponent, g->player);

        int score = (600000 * (player["fiveInRow"] - opponent["fiveInRow"]) +
                    10000 * (player["liveFour"] - opponent["liveFour"]) +
                    1100 * (player["deadFour"] - opponent["deadFour"]) +
                    900 * (player["liveThree"] - opponent["liveThree"]) +
                    500 * (player["deadThree"] - opponent["deadThree"]) +
                    50 * (player["liveTwo"] - opponent["liveTwo"]) +
                    10 * (player["deadTwo"] - opponent["deadTwo"]) -
                    10 * (player["uselessOne"] - opponent["uselessOne"]) +
                    5000 * (player["captures"] - opponent["captures"])
                 )
        return score;
    }

    int minimax(Game * g, int depth, int alpha, int beta, bool maximizingPlayer)
    {
        if (depth == 0 || g->game_over)
        {
            int getBoardEval = getBoardEval(g);
            return getBoardEval;
        }
        
        coordSet playable_area_copy = g->playable_area;
        for (coordSet::const_iterator it = playable_area_copy;
            it != playable_area_copy.end(); it++)
        {
            g->playOneMove(it->first, it->second);

            score = minimax(g, depth - 1, alpha, beta, !maximizingPlayer);

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
        int best_score = -INF;

        debugArray debug(19);
        for (int i = 0; i < 19; i++)
            for (int j = 0; j < 19; j++)
                debug[i].push_back(0);

        int alpha = -INF;
        int beta = INF;

        coordSet playable_area_copy = g->playable_area;

        int score;
        int depth = 3;

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
            for (coordSet::const_iterator it = g->stone_list[g->player];
                it != g->stone_list[g->player].end(); it++)
                debug[it->second][it->first] = "[X]";
            for (coordSet::const_iterator it = g->stone_list[g->opponent];
                it != g->stone_list[g->opponent].end(); it++)
                debug[it->second][it->first] = "[O]";
            
            for (int i = 0; i < 19; i++)
            {
                // change to printf or see how to format strings
                for (int j = 0; j < 19; j++)
                    std::cout << vector[i][j] << " ";
                std::cout << std::endl;
            }
        }
        g->best_move = best_move;
        return best_move;

        

    }
}