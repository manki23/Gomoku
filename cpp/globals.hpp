# ifndef GLOBALS_HPP
# define GLOBALS_HPP

# include <set>
# include <map>
# include <unordered_set>
# include <unordered_map>
# include <stack>
# include <iostream>
# include <bitset>
# include <vector>



typedef typename std::pair<int, int >			    coord;
typedef typename std::set< coord >		coordSet;
typedef typename std::bitset<361 >                  bset;
typedef typename std::stack< coord >				coordStack;
typedef typename std::stack< coordSet >			    coordStackSet;
# include "Game.hpp"

// class Game;

// CheckRules
coordSet wasCaptures(int x, int y, Game const * g, int player, coordSet const & captures);
coordSet getCaptures(int x, int y, Game const * g, int player, int opponnent);
coordSet hasLine(int x, int y, Game const * g);
coordSet hasColumn(int x, int y, Game const * g);
coordSet hasLeftDiagonal(int x, int y, Game const * g);
coordSet hasRightDiagonal(int x, int y, Game const * g);

bool checkCondition(int x, int y, Game const * g);
bool inSubSet(coord const c, coordSet const first, coordSet const second);
bool inSet(coord const c, coordSet const s);
bool getOpponenetCaptures(int x, int y, Game const * g);
bool hasVerticalFreeThree(int x, int y, Game const * g, int player);
bool hasVerticalFreeThree(int x, int y, Game const * g, int player);
bool hasLeftDiagonalFreeThree(int x, int y, Game const * g, int player);
bool hasRightDiagonalFreeThree(int x, int y, Game const * g, int player);

// CheckHeuristic
bool isOutsideBoard(int x, int y, int size, coordSet const & forbidden_moves);
std::map<std::string, int > countPatterns(std::vector<std::string> const & patterns);
std::map<std::string, int > getPatternDict(Game const * g, int player, int opponent);

//



# endif