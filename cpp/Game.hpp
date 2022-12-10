# ifndef GAME_HPP
# define GAME_HPP

# include "global.hpp"

# define EMPTY 0
# define BLACK 1
# define WHITE 2

// TODO add private functions

class Game
{
    public:
        std::map<int, coordSet >		stone_list;
        coordSet						possible_moves;
        coordSet						playable_area;
        std::map<int, coordSet >		forbidden_moves;
        std::map<int, int >				player_captures;
        std::map<int, coordStackSet >	stone_captured;
        std::map<int, coord >			last_winning_move;
        coordStack						move_history;
		std::map<int, coordSet >		playable_area_history;


        int							player;
        int							opponnent;
        int							goban_size;
        int							turn;

        bool						game_over;
    

        Game(int goban_size=19)
        {
			this->goban_size = goban_size;
			this->reset();
        }

        Game(Game const & g)
		{
			this->player = g.player;
			this->opponnent = g.opponnent;
			this->goban_size = g.goban_size;
			this->possible_moves = g.possible_moves;
			this->playable_area = g.playable_area;
			this->player_captures = g.player_captures;
			this->last_winning_move = g.last_winning_move;
			this->game_over = g.game_over;
			this->turn = g.turn;
			this->stone_list = g.stone_list;
			this->forbidden_moves = g.forbidden_moves;
			this->stone_captured = g.stone_captured;
			this->move_history = g.move_history;
			this->playable_area_history = g.playable_area_history;
		}

        ~Game(void) { return; }

        void reset(void)
		{
			this->player = BLACK;
            this->opponnent = WHITE;
            for (int i = 0; i < this->goban_size; i++)
                for (int j = 0; j < this->goban_size; j++)
					this->possible_moves.insert(coord(j, i));
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

			this->stone_list[this->player].insert(move);
			this->possible_moves.erase(move);
			coordSet::const_iterator pos = this->playable_area.find(move);
			if (pos != this->playable_area.end())
				this->playable_area.erase(move);
			
			this->updateStoneAreaCoordinates(move);
			this->updateForbiddenMoves();

			coordSet captures = CheckRules::getCaptures(move, &this, this->player, this->opponnent);
			this->stone_captured[this->player] = captures;
			this->clearCaptures(captures);
			this->player_captures[this->player] += captures.size();

			this->game_over = this->checkGameOver(xx, yy);
			this->opponnent = this->player;
			this->player = (this->opponnent == WHITE ? BLACK : WHITE);
			this->checkForWin();
			this->turn++;
			// REMOVE last move no necessary
			//this->last_move = move;
			this->move_history.push(move);
		}

		void revertLastMove(void)
		{
			coord move;

			this->opponnent = this->player;
			this->player = (this->opponnent == WHITE ? BLACK : WHITE);
			move = this->move_history.top();
			this->move_history.pop();
			if (this->last_winning_move[this->player] == move)
				this->last_winning_move[this->player] = coord(-1, -1);
			// Restore captured stones
			if (this->stone_captured[this->player]
				&& CheckRules::wasCaptures(move, this, this->player,
				this->opponnent, this->stone_captured[this->player].top()))
				{
					coordSet captures = this->stone_captured[this->player].top();
					this->stone_captured[this->player].pop();
					this->player_captures[this->player] -= captures.size();
					this->restoreCaptures(captures);
				}
			this->playable_area.erase(this->playable_area_history[this->turn].begin(), this->playable_area_history[this->turn].end());
			this->turn--;

			this->playable_area.insert(move);
			this->possible_moves.insert(move);

			this->stone_list[this->player].erase(move);

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
					coordSet::const_iterator pos_possible_moves = this->possible_moves.find(tmp);
					if (pos_possible_moves != this->possible_moves.end())
					{
						coordSet::const_iterator pos_playable_area = this->playable_area.find(tmp);
						if (pos_playable_area == this->playable_area.end())
						{
							this->playable_area.insert(tmp);
							this->playable_area_history[this->turn].insert(tmp);
						}
					}
				}
		}

		void updateForbiddenMoves(void)
		{
			this->forbidden_moves.clear();
			for (coordSet::const_iterator it = this->possible_moves.begin();
				it != this->possible_moves.end(); it++)
				{
					int x = it->first;
					int y = it->second;
					if (this->isCreatingDoubleThree(x, y, this->player))
						this->forbidden_moves[this->player].insert(*it);
					else if (this->isCreatingDoubleThree(x, y, this->opponnent))
						this->forbidden_moves[this->opponnent].insert(*it);
				}
		}

		bool isCreatingDoubleThree(int x, int y, int player)
		{
			return (	CheckRules::hasHorizontalFreeThree(x, y, &this, player)
					+ 	CheckRules::hasVerticalFreeThree(x, y, &this, player)
					+	CheckRules::hasRightDiagonalFreeThree(x, y, &this, player)
					+	CheckRules::hasLeftDiagonalFreeThree(x, y, &this, player));
		}

		void clearCaptures(coordSet const & captures)
		{
			for (coordSet::const_iterator it = captures.begin();
				it != captures.end(); it++)
			{
				this->possible_moves.insert(*it);
				this->playable_area.insert(*it);
				this->stone_list[this->opponnent].erase(*it);
				this->forbidden_moves[this->opponnent].erase(*it);
				this->forbidden_moves[this->player].erase(*it);
			}
		}

		void restoreCaptures(coordSet const & captures)
		{
			for (coordSet::const_iterator it = captures.begin();
				it != captures.end(); it++)
			{
				this->possible_moves.erase(*it);
				this->playable_area.erase(*it);
				this->stone_list[this->opponnent].insert(*it);
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
			coordSet::const_iterator pos = this->stone_list[this->player].find(coord(x, y));
			return (pos != this->stone_list[this->player].end()
					&& CheckRules::hasColumn(x, y, &this)
					&& CheckRules::hasLine(x, y, &this)
					&& CheckRules::hasLeftDiagonal(x, y, &this)
					&& CheckRules::hasRightDiagonal(x, y, &this));
		}

		bool letOpponentPlay(coordSet const & aligned, int x, int y)
		{
			for (coordSet::const_iterator it = aligned.begin();
				it != aligned.end(); it++)
			{
				int xx = it->first;
				int yy = it->second;

				if (CheckRules::getOpponenetCaptures(xx, yy, &this))
				{
					if (this->last_winning_move[this->player] != coord(-1, -1))
						return false;
					this->last_winning_move[this->player] = coord(x, y);
					return true;
				}
			}
			for (coordSet::const_iterator it = this->stone_list[this->player].begin();
				it != this->stone_list[this->player].end(); it++)
			{
				int xx = it->first;
				int yy = it->second;
				coordSet::const_iterator pos = aligned.find(*it);
				if (pos == aligned.end()
				&& this->player_captures[this->opponnent] == 8
				&& CheckRules::getOpponenetCaptures(xx, yy, &this))
					return true;

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

}

# endif