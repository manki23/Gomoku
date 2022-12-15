# ifndef GLOBALS_HPP
# define GLOBALS_HPP

# include "Types.hpp"

class Game;

// CheckRules
coordSet wasCaptures(int x, int y, Game * g, int player, coordSet const & captures);
coordSet getCaptures(int x, int y, Game * g, int player, int opponnent);
coordSet hasLine(int x, int y, Game * g);
coordSet hasColumn(int x, int y, Game * g);
coordSet hasLeftDiagonal(int x, int y, Game * g);
coordSet hasRightDiagonal(int x, int y, Game * g);

bool checkCondition(int x, int y, Game * g);
bool inSubSet(coord const c, coordSet const first, coordSet const second);
bool inSet(coord const c, coordSet const s);
bool getOpponenetCaptures(int x, int y, Game * g);
bool hasVerticalFreeThree(int x, int y, Game * g, int player);
bool hasHorizontalFreeThree(int x, int y, Game * g, int player);
bool hasLeftDiagonalFreeThree(int x, int y, Game * g, int player);
bool hasRightDiagonalFreeThree(int x, int y, Game * g, int player);

// CheckHeuristic
bool isOutsideBoard(int x, int y, int size, coordSet const & forbidden_moves);
std::map<std::string, int > countPatterns(std::vector<std::string> const & patterns);
std::map<std::string, int > getPatternDict(Game * g, int player, int opponent);

// Bot
coord getNextMove(Game * g);

// Heuristic
std::map<std::string, int > getPatternDict(Game * g, int player, int opponent);
std::map<std::string, int > countPatterns(std::vector<std::string> const & patterns);
bool isOutsideBoard(int x, int y, int size, coordSet const & forbidden_moves);

bool inSet(coord const c, coordSet const s);
bool inSetPattern(std::string pattern, std::unordered_set<std::string> s);
# endif