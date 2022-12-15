# include "globals.hpp"
# include "Game.hpp"

void printStoneList(std::map<int, coordSet> m)
{
	for (std::map<int, coordSet>::const_iterator it = m.begin();
	it != m.end(); it++)
	{
		std::cout << "PLAYER : " << it->first << std::endl;
		for (coordSet::const_iterator its = it->second.begin();
		its != it->second.end(); its++)
			std::cout << "(" << its->first << ", " << its->second << ") ";
		std::cout << "\n\n";
	}
}

void printPossibleMoves(coordSet pmoves)
{
	std::cout << "POSSIBLE MOVES : [ ";
	for (coordSet::const_iterator it = pmoves.begin();
	it != pmoves.end(); it++)
		std::cout << "( " << it->first << ", " << it->second << ") ";
	std::cout << "]" << std::endl;
}

void resetPlayers(Game * g)
{
	g->player = 1;
	g->opponent = 2;
}

int main()
{
	Game * g = new Game();

	//sd::cout << g->goban_size << std::endl;

	//printPossibleMoves(g->possible_moves);
	coord move;
	for (int i = 0; i < 10; i++)
	{
 		move = getNextMove(g);
		std::cout << move.first << " " << move.second << std::endl;
		g->playOneMove(move.first, move.second);
		printStoneList(g->stone_list);
	}


	delete g;

	return 0;
}