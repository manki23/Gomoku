# ifndef GAME_HPP
# define GAME_HPP

# include "globals.hpp"

# define EMPTY 0
# define BLACK 1
# define WHITE 2

// TODO add private functions

class Game
{
	public:
		int			 					board[19][19];
		mapCoordSet						forbidden_moves;
		coordSet						playable_area;
		std::map<int, int >				player_captures;
		std::map<int, coordStackSet >	stone_captured;
		std::map<int, coord >			last_winning_move;
		coordStack						move_history;
		mapCoordSet						playable_area_history;

		std::map<std::string, int > transposition_table;


		int								player;
		int								opponent;
		int								goban_size;
		int								turn;

		bool							game_over;
	
		coord							best_move;

		Game(int goban_size=19)
		{
			this->goban_size = goban_size;
			this->reset();
		}

		~Game(void) { return; }

		void reset(void)
		{
			this->player = BLACK;
			this->opponent = WHITE;
			for (int i = 0; i < this->goban_size; i++)
				for (int j = 0; j < this->goban_size; j++)
					board[i][j] = EMPTY;
			int low = (this->goban_size / 2) - 1;
			int high = (this->goban_size / 2) + 2;
			for (int i = low; i < high; i++)
				for (int j = low; j < high; j++)
					this->playable_area.insert(coord(j, i));
			this->player_captures[BLACK] = 0;
			this->player_captures[WHITE] = 0;
			this->last_winning_move[BLACK] = coord(-1, -1);
			this->last_winning_move[WHITE] = coord(-1, -1);
			this->game_over = false;
			this->turn = 0;
		}

		void playOneMove(int xx, int yy)
		{
			coord	move = coord(xx, yy);

			this->board[yy][xx] = this->player;
			
			this->updateStoneAreaCoordinates(coord(xx, yy));
			this->updateForbiddenMoves();

			coordSet captures = getCaptures(xx, yy, this, this->player, this->opponent);
			this->stone_captured[this->player].push(captures);
			this->clearCaptures(captures);
			this->player_captures[this->player] += captures.size();

			this->game_over = this->checkGameOver(xx, yy);
			this->opponent = this->player;
			this->player = (this->opponent == WHITE ? BLACK : WHITE);
			this->checkForWin();
			this->turn++;
			this->move_history.push(move);
		}

		// DEBUG
		void printPlayableAreaHist(mapCoordSet m)
		{
			for (mapCoordSet::const_iterator it = m.begin();
			it != m.end(); it++)
			{
				std::cout << "TURN : " << it->first << std::endl;
				for (coordSet::const_iterator its = it->second.begin();
				its != it->second.end(); its++)
					std::cout << "(" << its->first << ", " << its->second << ") ";
				std::cout << "\n\n";
			}
		}

		// DEBUG
		void printPlayableArea(coordSet playableArea)
		{
			std::cout << "PLAYABLE AREA : " << std::endl;
			for (coordSet::const_iterator it = playableArea.begin();
			it != playableArea.end(); it++)
			{
				std::cout << "(" << it->first << ", " << it->second << ") ";
			}
			std::cout << "\n\n";
		}

		void revertLastMove(void)
		{
			coord move;

			this->opponent = this->player;
			this->player = (this->opponent == WHITE ? BLACK : WHITE);
			move = this->move_history.top();
			this->move_history.pop();
			if (this->last_winning_move[this->player] == move)
				this->last_winning_move[this->player] = coord(-1, -1);
			// Restore captured stones
			if (!this->stone_captured[this->player].empty()
				&& !wasCaptures(move.first, move.second, this, this->player, this->stone_captured[this->player].top()).empty())
				{
					coordSet captures = this->stone_captured[this->player].top();
					this->stone_captured[this->player].pop();
					this->player_captures[this->player] -= captures.size();
					this->restoreCaptures(captures);
				}

			
			for (coordSet::const_iterator it = this->playable_area_history[this->turn].begin(); it != this->playable_area_history[this->turn].end(); it++)
				this->playable_area.erase(coord(it->first, it->second));
			this->playable_area.clear();
			
			this->playable_area_history[this->turn].clear();
			this->turn--;

			this->playable_area.insert(move);
			this->board[move.second][move.first] = 0;

			this->updateForbiddenMoves();
		}

		void updateStoneAreaCoordinates(const coord & move)
		{
			int width = 1;
			for (int i = -width; i < width + 1; i++)
				for (int j = -width; j < width + 1; j++)
				{
					coord tmp = move;
					tmp.first += i;
					tmp.second += j;
					coordSet::const_iterator pos_forbidden = this->forbidden_moves[this->player].find(tmp);
					if (this->board[tmp.second][tmp.first] == 0
					&& pos_forbidden == this->forbidden_moves[this->player].end())
					{
						this->playable_area.insert(tmp);
						this->playable_area_history[this->turn].insert(tmp);
					}
				}
		}

		void updateForbiddenMoves(void)
		{
			this->forbidden_moves.clear();
			for (int y = 0; y < this->goban_size; y++)
			{
				for (int x = 0; x < this->goban_size; x++)
				{
					if (!this->board[y][x])
					{
						if (this->isCreatingDoubleThree(x, y, this->player))
							this->forbidden_moves[this->player].insert(coord(x, y));
						else if (this->isCreatingDoubleThree(x, y, this->opponent))
							this->forbidden_moves[this->opponent].insert(coord(x, y));
					}
				}
			}
		}

		bool isCreatingDoubleThree(int x, int y, int player)
		{
			return (	hasHorizontalFreeThree(x, y, this, player)
					+ 	hasVerticalFreeThree(x, y, this, player)
					+	hasRightDiagonalFreeThree(x, y, this, player)
					+	hasLeftDiagonalFreeThree(x, y, this, player));
		}

		void clearCaptures(coordSet const & captures)
		{
			for (coordSet::const_iterator it = captures.begin();
				it != captures.end(); it++)
			{
				this->board[it->second][it->first] = 0;
				this->playable_area.insert(*it);
				this->forbidden_moves[this->opponent].erase(*it);
				this->forbidden_moves[this->player].erase(*it);
			}
		}

		void restoreCaptures(coordSet const & captures)
		{
			for (coordSet::const_iterator it = captures.begin();
				it != captures.end(); it++)
			{
				this->board[it->second][it->first] = this->opponent;
				this->playable_area.erase(*it);
			}
		}

		bool checkGameOver(int xx, int yy)
		{
			coordSet aligned = this->hasFiveAligned(xx, yy);

			if (this->player_captures[this->player] >= 10
			|| (aligned.size() && !this->letOpponentPlay(aligned, xx, yy)))
			{
				std::cout << "PLAYER " << this->player << " WON !" << std::endl;
				return true;
			}
			return false;
		}

		coordSet hasFiveAligned(int x, int y)
		{
			coordSet returnedSet;
			if (this->board[y][x] == EMPTY)
				return coordSet();
			returnedSet = hasColumn(x, y, this);
			if (!returnedSet.empty())
				return returnedSet;
			returnedSet = hasLine(x, y, this);
			if (!returnedSet.empty())
				return returnedSet;
			returnedSet = hasLeftDiagonal(x, y, this);
			if (!returnedSet.empty())
				return returnedSet;
			returnedSet = hasRightDiagonal(x, y, this);
			if (!returnedSet.empty())
				return returnedSet;
			return coordSet();
		}

		bool letOpponentPlay(coordSet const & aligned, int x, int y)
		{
			int xx;
			int yy;
			for (coordSet::const_iterator it = aligned.begin();
				it != aligned.end(); it++)
			{
				xx = it->first;
				yy = it->second;

				if (getOpponenetCaptures(xx, yy, this))
				{
					if (this->last_winning_move[this->player] != coord(-1, -1))
						return false;
					this->last_winning_move[this->player] = coord(x, y);
					return true;
				}
			}
			for (yy = 0; y < this->goban_size; y++)
			{
				for (xx = 0; x < this->goban_size; x++)
				{
					coordSet::const_iterator pos = aligned.find(coord(xx, yy));
					if (pos == aligned.end()
					&& this->player_captures[this->opponent] == 8
					&& getOpponenetCaptures(xx, yy, this))
						return true;
				}
			}
			return false;
		}

		bool checkForWin(void)
		{
			if (this->last_winning_move[this->player] != coord(-1, -1)
			&& this->checkGameOver(this->last_winning_move[this->player].first, this->last_winning_move[this->player].second))
				this->game_over = true;
			else if (this->last_winning_move[this->player] != coord(-1, -1))
				this->last_winning_move[this->player] = coord(-1, -1);
			return this->game_over;
		}

};

# endif