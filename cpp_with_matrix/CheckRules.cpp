# ifndef CHECKRULES_HPP
# define CHECKRULES_HPP

# include "Game.hpp"

bool checkCondition(int x, int y, Game * g)
{
    return (g->board[y][x] == g->player
            && x >= 0
            && x < g->goban_size
            && y >= 0
            && y < g->goban_size);
}

coordSet hasLine(int x, int y, Game * g)
{
    int i = 1;
    int count = 1;
    coordSet result;
    result.insert(coord(x, y));
    while (i <= 4 && checkCondition(x - i, y, g))
    {
        count++;
        result.insert(coord(x - i, y));
        i++;
    }
    i = 1;
    while (i <= 4 && checkCondition(x + i, y, g))
    {
        count++;
        result.insert(coord(x + i, y));
        i++;
    }
    if (count >= 5)
        return result;
    return coordSet();
}

coordSet hasColumn(int x, int y, Game * g)
{
    int i = 1;
    int count = 1;
    coordSet result;
    result.insert(coord(x, y));
    while (i <= 4 && checkCondition(x, y - i, g))
    {
        count++;
        result.insert(coord(x, y - i));
        i++;
    }
    i = 1;
    while (i <= 4 && checkCondition(x, y + i, g))
    {
        count++;
        result.insert(coord(x, y + i));
        i++;
    }
    if (count >= 5)
        return result;
    return coordSet();
}

coordSet hasLeftDiagonal(int x, int y, Game * g)
{
    int i = 1;
    int count = 1;
    coordSet result;
    result.insert(coord(x, y));
    while (i <= 4 && checkCondition(x - i, y - i, g))
    {
        count++;
        result.insert(coord(x - i, y - i));
        i++;
    }
    i = 1;
    while (i <= 4 && checkCondition(x + i, y + i, g))
    {
        count++;
        result.insert(coord(x + i, y + i));
        i++;
    }
    if (count >= 5)
        return result;
    return coordSet();
}

coordSet hasRightDiagonal(int x, int y, Game * g)
{
    int i = 1;
    int count = 1;
    coordSet result;
    result.insert(coord(x, y));
    while (i <= 4 && checkCondition(x + i, y - i, g))
    {
        count++;
        result.insert(coord(x + i, y - i));
        i++;
    }
    i = 1;
    while (i <= 4 && checkCondition(x - i, y + i, g))
    {
        count++;
        result.insert(coord(x - i, y + i));
        i++;
    }
    if (count >= 5)
        return result;
    return coordSet();
}

coordSet getCaptures(int x, int y, Game * g, int player, int opponent)
{
    coordSet result;

    // vertical
    if (g->board[y][x + 1] == opponent
        && g->board[y][x + 2] == opponent
        && g->board[y][x + 3] == player)
    {
        result.insert(coord(x + 1, y));
        result.insert(coord(x + 2, y));
    }
    if (g->board[y][x - 1] == opponent
        && g->board[y][x - 2] == opponent
        && g->board[y][x - 3] == player)
    {
        result.insert(coord(x - 1, y));
        result.insert(coord(x - 2, y));
    }
    // horizontal
    if (g->board[y + 1][x] == opponent
        && g->board[y + 2][x] == opponent
        && g->board[y + 3][x] == player)
    {
        result.insert(coord(x, y + 1));
        result.insert(coord(x, y + 2));
    }
    if (g->board[y - 1][x] == opponent
        && g->board[y - 2][x] == opponent
        && g->board[y - 3][x] == player)
    {
        result.insert(coord(x, y - 1));
        result.insert(coord(x, y - 2));
    }
    // left diagonal
    if (g->board[y + 1][x + 1] == opponent
        && g->board[y + 2][x + 2] == opponent
        && g->board[y + 3][x + 3] == player)
    {
        result.insert(coord(x + 1, y + 1));
        result.insert(coord(x + 2, y + 2));
    }
    if (g->board[y - 1][x - 1] == opponent
        && g->board[y - 2][x - 2] == opponent
        && g->board[y - 3][x - 3] == player)
    {
        result.insert(coord(x - 1, y - 1));
        result.insert(coord(x - 2, y - 2));
    }
    // right diagonal
    if (g->board[y + 1][x - 1] == opponent
        && g->board[y + 2][x - 2] == opponent
        && g->board[y + 3][x - 3] == player)
    {
        result.insert(coord(x - 1, y + 1));
        result.insert(coord(x - 2, y + 2));
    }
    if (g->board[y - 1][x + 1] == opponent
        && g->board[y - 2][x + 2] == opponent
        && g->board[y - 3][x + 3] == player)
    {
        result.insert(coord(x + 1, y - 1));
        result.insert(coord(x + 2, y - 2));
    }
    return result;
}

coordSet wasCaptures(int x, int y, Game * g, int player, coordSet const & captures)
{
    coordSet result;
    coordSet::const_iterator capEnd = captures.end();

    // vertical
    if (captures.find(coord(x + 1, y)) != capEnd
        && captures.find(coord(x + 2, y)) != capEnd
        && g->board[y][x + 3] == player)
    {
        result.insert(coord(x + 1, y));
        result.insert(coord(x + 2, y));
    }
    if (captures.find(coord(x -1, y)) != capEnd
        && captures.find(coord(x - 2, y)) != capEnd
        && g->board[y][x - 3] == player)
    {
        result.insert(coord(x - 1, y));
        result.insert(coord(x - 2, y));
    }
    // horizontal
    if (captures.find(coord(x, y + 1)) != capEnd
        && captures.find(coord(x, y + 2)) != capEnd
        && g->board[y + 3][x] == player)
    {
        result.insert(coord(x, y + 1));
        result.insert(coord(x, y + 2));
    }
    if (captures.find(coord(x, y - 1)) != capEnd
        && captures.find(coord(x, y - 2)) != capEnd
        && g->board[y - 3][x] == player)
    {
        result.insert(coord(x, y - 1));
        result.insert(coord(x, y - 2));
    }
    // left diagonal
    if (captures.find(coord(x + 1, y + 1)) != capEnd
        && captures.find(coord(x + 2, y + 2)) != capEnd
        && g->board[y + 3][x + 3] == player)
    {
        result.insert(coord(x + 1, y + 1));
        result.insert(coord(x + 2, y + 2));
    }
    if (captures.find(coord(x - 1, y - 1)) != capEnd
        && captures.find(coord(x - 2, y - 2)) != capEnd
        && g->board[y - 3][x - 3] == player)
    {
        result.insert(coord(x - 1, y - 1));
        result.insert(coord(x - 2, y - 2));
    }
    // right diagonal
    if (captures.find(coord(x - 1, y + 1)) != capEnd
        && captures.find(coord(x - 2, y + 2)) != capEnd
        && g->board[y + 3][x - 3] == player)
    {
        result.insert(coord(x - 1, y + 1));
        result.insert(coord(x - 2, y + 2));
    }
    if (captures.find(coord(x + 1, y - 1)) != capEnd
        && captures.find(coord(x + 2, y - 2)) != capEnd
        && g->board[y - 3][x + 3] == player)
    {
        result.insert(coord(x + 1, y - 1));
        result.insert(coord(x + 2, y - 2));
    }
    return result;
}

bool inSubSet(coord const c, coordSet const first, coordSet const second)
{
    coordSet::const_iterator posFirst = first.find(c);
    coordSet::const_iterator posSecond = second.find(c);
    return (posFirst != first.end() && posSecond == second.end());
}

bool inSet(coord const c, coordSet const s)
{
    coordSet::const_iterator pos = s.find(c);
    return (pos != s.end());
}

bool inSetPattern(std::string pattern, std::unordered_set<std::string> s)
{
    std::unordered_set<std::string>::const_iterator pos = s.find(pattern);
    return (pos != s.end());
}


bool getOpponenetCaptures(int x, int y, Game * g)
{
    if (((g->board[y][x - 1] == g->opponent
        && g->board[y][x + 2] == 0 && inSet(coord(x + 2, y), g->forbidden_moves[g->opponent]))
        || (g->board[y][x + 2] == g->opponent
        && g->board[y][x - 1] == 0 && inSet(coord(x - 1, y), g->forbidden_moves[g->opponent])))
        && g->board[y][x + 1] == g->player)
        return true;
    
    if (((g->board[y][x - 1] == g->opponent
        && g->board[y][x - 2] == 0 && inSet(coord(x - 2, y), g->forbidden_moves[g->opponent]))
        || (g->board[y][x - 2] == g->opponent
        && g->board[y][x + 1] == 0 && inSet(coord(x + 1, y), g->forbidden_moves[g->opponent])))
        && g->board[y][x - 1] == g->player)
        return true;

    if (((g->board[y + 1][x] == g->opponent
        && g->board[y - 2][x] == 0 && inSet(coord(x, y - 2), g->forbidden_moves[g->opponent]))
        || (g->board[y - 2][x] == g->opponent
        && g->board[y + 1][x] == 0 && inSet(coord(x, y + 1), g->forbidden_moves[g->opponent])))
        && g->board[y - 1][x] == g->player)
        return true;

    if (((g->board[y + 1][x] == g->opponent
        && g->board[y - 2][x] == 0 && inSet(coord(x, y - 2), g->forbidden_moves[g->opponent]))
        || (g->board[y - 2][x] == g->opponent
        && g->board[y + 1][x] == 0 && inSet(coord(x, y + 1), g->forbidden_moves[g->opponent])))
        && g->board[y - 1][x] == g->player)
        return true;

    if (((g->board[y - 1][x] == g->opponent
        && g->board[y + 2][x] == 0 && inSet(coord(x, y + 2), g->forbidden_moves[g->opponent]))
        || (g->board[y + 2][x] == g->opponent
        && g->board[y - 1][x] == 0 && inSet(coord(x, y - 1), g->forbidden_moves[g->opponent])))
        && g->board[y + 1][x] == g->player)
        return true;

    if (((g->board[y - 1][x - 1] == g->opponent
        && g->board[y + 2][x + 2] == 0 && inSet(coord(x + 2, y + 2), g->forbidden_moves[g->opponent]))
        || (g->board[y + 2][x + 2] == g->opponent
        && g->board[y - 1][x - 1] == 0 && inSet(coord(x - 1, y - 1), g->forbidden_moves[g->opponent])))
        && g->board[y - 1][x - 1] == g->player)
        return true;

    if (((g->board[y + 1][x + 1] == g->opponent
        && g->board[y - 2][x - 2] == 0 && inSet(coord(x - 2, y - 2), g->forbidden_moves[g->opponent]))
        || (g->board[y - 2][x - 2] == g->opponent
        && g->board[y + 1][x + 1] == 0 && inSet(coord(x + 1, y + 1), g->forbidden_moves[g->opponent])))
        && g->board[y - 1][x - 1] == g->player)
        return true;

    if (((g->board[y + 1][x - 1] == g->opponent
        && g->board[y - 2][x + 2] == 0 && inSet(coord(x + 2, y - 2), g->forbidden_moves[g->opponent]))
        || (g->board[y - 2][x + 2] == g->opponent
        && g->board[y + 1][x - 1] == 0 && inSet(coord(x - 1, y + 1), g->forbidden_moves[g->opponent])))
        && g->board[y - 1][x + 1] == g->player)
        return true;
        
    if (((g->board[y - 1][x + 1] == g->opponent
        && g->board[y + 2][x - 2] == 0 && inSet(coord(x - 2, y + 2), g->forbidden_moves[g->opponent]))
        || (g->board[y + 2][x - 2] == g->opponent
        && g->board[y - 1][x + 1] == 0 && inSet(coord(x + 1, y - 1), g->forbidden_moves[g->opponent])))
        && g->board[y + 1][x - 1] == g->player)
        return true;

    return false;
}

bool hasVerticalFreeThree(int x, int y, Game * g, int player)
{
    // ######################### Pattern X000X
    if (g->board[y + 1][x] == player
        && g->board[y + 2][x] == player
        && g->board[y + 3][x] == 0
        && g->board[y - 1][x] == 0)
        return true;

    if (g->board[y - 1][x] == player
        && g->board[y - 2][x] == player
        && g->board[y - 3][x] == 0
        && g->board[y + 1][x] == 0)
        return true;

    if (g->board[y - 1][x] == player
        && g->board[y + 1][x] == player
        && g->board[y + 2][x] == 0
        && g->board[y - 2][x] == 0)
        return true;                

    // ######################## Pattern X00X0X

    if (g->board[y - 1][x] == player
        && g->board[y - 3][x] == player
        && g->board[y - 2][x] == 0
        && g->board[y - 4][x] == 0
        && g->board[y + 1][x] == 0)
        return true;

    if (g->board[y + 1][x] == player
        && g->board[y - 2][x] == player
        && g->board[y + 2][x] == 0
        && g->board[y - 3][x] == 0
        && g->board[y - 1][x] == 0)
        return true;

    if (g->board[y + 2][x] == player
        && g->board[y + 3][x] == player
        && g->board[y + 1][x] == 0
        && g->board[y + 4][x] == 0
        && g->board[y - 1][x] == 0)
        return true;

    // ######################### Pattern X0X00X

    if (g->board[y + 1][x] == player
        && g->board[y + 3][x] == player
        && g->board[y + 2][x] == 0
        && g->board[y + 4][x] == 0
        && g->board[y - 1][x] == 0)
        return true;

    if (g->board[y - 1][x] == player
        && g->board[y + 2][x] == player
        && g->board[y + 1][x] == 0
        && g->board[y - 2][x] == 0
        && g->board[y + 3][x] == 0)
        return true;

    if (g->board[y - 2][x] == player
        && g->board[y - 3][x] == player
        && g->board[y + 1][x] == 0
        && g->board[y - 1][x] == 0
        && g->board[y - 4][x] == 0)
        return true;

    return false;
}

bool hasHorizontalFreeThree(int x, int y, Game * g, int player)
{
    // ######################### Pattern X000X
    if (g->board[y][x + 1] == player
        && g->board[y][x + 2] == player
        && g->board[y][x + 3] == 0
        && g->board[y][x - 1] == 0)
        return true;

    if (g->board[y][x - 1] == player
        && g->board[y][x - 2] == player
        && g->board[y][x - 3] == 0
        && g->board[y][x + 1] == 0)
        return true;

    if (g->board[y][x - 1] == player
        && g->board[y][x + 1] == player
        && g->board[y][x + 2] == 0
        && g->board[y][x - 2] == 0)
        return true;                

    // ######################## Pattern X00X0X

    if (g->board[y][x - 1] == player
        && g->board[y][x - 3] == player
        && g->board[y][x - 2] == 0
        && g->board[y][x - 4] == 0
        && g->board[y][x + 1] == 0)
        return true;

    if (g->board[y][x + 1] == player
        && g->board[y][x - 2] == player
        && g->board[y][x + 2] == 0
        && g->board[y][x - 3] == 0
        && g->board[y][x - 1] == 0)
        return true;

    if (g->board[y][x + 2] == player
        && g->board[y][x + 3] == player
        && g->board[y][x + 1] == 0
        && g->board[y][x + 4] == 0
        && g->board[y][x - 1] == 0)
        return true;

    // ######################### Pattern X0X00X

    if (g->board[y][x + 1] == player
        && g->board[y][x + 3] == player
        && g->board[y][x + 2] == 0
        && g->board[y][x + 4] == 0
        && g->board[y][x - 1] == 0)
        return true;

    if (g->board[y][x - 1] == player
        && g->board[y][x + 2] == player
        && g->board[y][x + 1] == 0
        && g->board[y][x - 2] == 0
        && g->board[y][x + 3] == 0)
        return true;

    if (g->board[y][x - 2] == player
        && g->board[y][x - 3] == player
        && g->board[y][x + 1] == 0
        && g->board[y][x - 1] == 0
        && g->board[y][x - 4] == 0)
        return true;

    return false;
}


bool hasLeftDiagonalFreeThree(int x, int y, Game * g, int player)
{
    // ######################### Pattern X000X
    if (g->board[y + 1][x + 1] == player
        && g->board[y + 2][x + 2] == player
        && g->board[y + 3][x + 3] == 0
        && g->board[y - 1][x - 1] == 0)
        return true;

    if (g->board[y - 1][x - 1] == player
        && g->board[y - 2][x - 2] == player
        && g->board[y - 3][x - 3] == 0
        && g->board[y + 1][x + 1] == 0)
        return true;

    if (g->board[y - 1][x - 1] == player
        && g->board[y + 1][x + 1] == player
        && g->board[y + 2][x + 2] == 0
        && g->board[y - 2][x - 2] == 0)
        return true;                

    // ######################## Pattern X00X0X

    if (g->board[y - 1][x - 1] == player
        && g->board[y - 3][x - 3] == player
        && g->board[y - 2][x - 2] == 0
        && g->board[y - 4][x - 4] == 0
        && g->board[y + 1][x + 1] == 0)
        return true;

    if (g->board[y + 1][x + 1] == player
        && g->board[y - 2][x - 2] == player
        && g->board[y + 2][x + 2] == 0
        && g->board[y - 3][x - 3] == 0
        && g->board[y - 1][x - 1] == 0)
        return true;

    if (g->board[y + 2][x + 2] == player
        && g->board[y + 3][x + 3] == player
        && g->board[y + 1][x + 1] == 0
        && g->board[y + 4][x + 4] == 0
        && g->board[y - 1][x - 1] == 0)
        return true;

    // ######################### Pattern X0X00X

    if (g->board[y + 1][x + 1] == player
        && g->board[y + 3][x + 3] == player
        && g->board[y + 2][x + 2] == 0
        && g->board[y + 4][x + 4] == 0
        && g->board[y - 1][x - 1] == 0)
        return true;

    if (g->board[y - 1][x - 1] == player
        && g->board[y + 2][x + 2] == player
        && g->board[y + 1][x + 1] == 0
        && g->board[y - 2][x - 2] == 0
        && g->board[y + 3][x + 3] == 0)
        return true;

    if (g->board[y - 2][x - 2] == player
        && g->board[y - 3][x - 3] == player
        && g->board[y + 1][x + 1] == 0
        && g->board[y - 1][x - 1] == 0
        && g->board[y - 4][x - 4] == 0)
        return true;

    return false;
}

bool hasRightDiagonalFreeThree(int x, int y, Game * g, int player)
{
    // ######################### Pattern X000X
    if (g->board[y + 1][x - 1] == player
        && g->board[y + 2][x - 2] == player
        && g->board[y + 3][x - 3] == 0
        && g->board[y - 1][x + 1] == 0)
        return true;

    if (g->board[y - 1][x + 1] == player
        && g->board[y - 2][x + 2] == player
        && g->board[y - 3][x + 3] == 0
        && g->board[y + 1][x - 1] == 0)
        return true;

    if (g->board[y - 1][x + 1] == player
        && g->board[y + 1][x - 1] == player
        && g->board[y + 2][x - 2] == 0
        && g->board[y - 2][x + 2] == 0)
        return true;                

    // ######################## Pattern X00X0X

    if (g->board[y - 1][x + 1] == player
        && g->board[y - 3][x + 3] == player
        && g->board[y - 2][x + 2] == 0
        && g->board[y - 4][x + 4] == 0
        && g->board[y + 1][x - 1] == 0)
        return true;

    if (g->board[y + 1][x - 1] == player
        && g->board[y - 2][x + 2] == player
        && g->board[y + 2][x - 2] == 0
        && g->board[y - 3][x + 3] == 0
        && g->board[y - 1][x + 1] == 0)
        return true;

    if (g->board[y + 2][x - 2] == player
        && g->board[y + 3][x - 3] == player
        && g->board[y + 1][x - 1] == 0
        && g->board[y + 4][x - 4] == 0
        && g->board[y - 1][x + 1] == 0)
        return true;

    // ######################### Pattern X0X00X

    if (g->board[y + 1][x - 1] == player
        && g->board[y + 3][x - 3] == player
        && g->board[y + 2][x - 2] == 0
        && g->board[y + 4][x - 4] == 0
        && g->board[y - 1][x + 1] == 0)
        return true;

    if (g->board[y - 1][x + 1] == player
        && g->board[y + 2][x - 2] == player
        && g->board[y + 1][x - 1] == 0
        && g->board[y - 2][x + 2] == 0
        && g->board[y + 3][x - 3] == 0)
        return true;

    if (g->board[y - 2][x + 2] == player
        && g->board[y - 3][x + 3] == player
        && g->board[y + 1][x - 1] == 0
        && g->board[y - 1][x + 1] == 0
        && g->board[y - 4][x + 4] == 0)
        return true;
    
    return false;
}

# endif