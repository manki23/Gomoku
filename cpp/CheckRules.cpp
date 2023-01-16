# ifndef CHECKRULES_HPP
# define CHECKRULES_HPP

# include "Game.hpp"

bool checkCondition(int x, int y, Game * g)
{
    coordSet::const_iterator pos = g->stone_list[g->player].find(coord(x, y));
    return (pos != g->stone_list[g->player].end()
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

coordSet getCaptures(int x, int y, Game * g, int player, int opponnent)
{
    coordSet result;
    coordSet::const_iterator oppEnd = g->stone_list[opponnent].end();
    coordSet::const_iterator pEnd = g->stone_list[player].end();
    // vertical
    if (g->stone_list[opponnent].find(coord(x + 1, y)) != oppEnd
        && g->stone_list[opponnent].find(coord(x + 2, y)) != oppEnd
        && g->stone_list[player].find(coord(x + 3, y)) != pEnd)
    {
        result.insert(coord(x + 1, y));
        result.insert(coord(x + 2, y));
    }
    if (g->stone_list[opponnent].find(coord(x - 1, y)) != oppEnd
        && g->stone_list[opponnent].find(coord(x - 2, y)) != oppEnd
        && g->stone_list[player].find(coord(x - 3, y)) != pEnd)
    {
        result.insert(coord(x - 1, y));
        result.insert(coord(x - 2, y));
    }
    // horizontal
    if (g->stone_list[opponnent].find(coord(x, y + 1)) != oppEnd
        && g->stone_list[opponnent].find(coord(x, y + 2)) != oppEnd
        && g->stone_list[player].find(coord(x, y + 3)) != pEnd)
    {
        result.insert(coord(x, y + 1));
        result.insert(coord(x, y + 2));
    }
    if (g->stone_list[opponnent].find(coord(x, y - 1)) != oppEnd
        && g->stone_list[opponnent].find(coord(x, y - 2)) != oppEnd
        && g->stone_list[player].find(coord(x, y - 3)) != pEnd)
    {
        result.insert(coord(x, y - 1));
        result.insert(coord(x, y - 2));
    }
    // left diagonal
    if (g->stone_list[opponnent].find(coord(x + 1, y + 1)) != oppEnd
        && g->stone_list[opponnent].find(coord(x + 2, y + 2)) != oppEnd
        && g->stone_list[player].find(coord(x + 3, y + 3)) != pEnd)
    {
        result.insert(coord(x + 1, y + 1));
        result.insert(coord(x + 2, y + 2));
    }
    if (g->stone_list[opponnent].find(coord(x - 1, y - 1)) != oppEnd
        && g->stone_list[opponnent].find(coord(x - 2, y - 2)) != oppEnd
        && g->stone_list[player].find(coord(x - 3, y - 3)) != pEnd)
    {
        result.insert(coord(x - 1, y - 1));
        result.insert(coord(x - 2, y - 2));
    }
    // right diagonal
    if (g->stone_list[opponnent].find(coord(x - 1, y + 1)) != oppEnd
        && g->stone_list[opponnent].find(coord(x - 2, y + 2)) != oppEnd
        && g->stone_list[player].find(coord(x - 3, y + 3)) != pEnd)
    {
        result.insert(coord(x - 1, y + 1));
        result.insert(coord(x - 2, y + 2));
    }
    if (g->stone_list[opponnent].find(coord(x + 1, y - 1)) != oppEnd
        && g->stone_list[opponnent].find(coord(x + 2, y - 2)) != oppEnd
        && g->stone_list[player].find(coord(x + 3, y - 3)) != pEnd)
    {
        result.insert(coord(x + 1, y - 1));
        result.insert(coord(x + 2, y - 2));
    }
    if (!result.empty())
        std::cout << "Dans get Captures : " << x << " " << y << std::endl;
    return result;
}

coordSet wasCaptures(int x, int y, Game * g, int player, coordSet const & captures)
{
    coordSet result;
    coordSet::const_iterator capEnd = captures.end();
    coordSet::const_iterator stoneEnd = g->stone_list[player].end();
    // vertical
    if (captures.find(coord(x + 1, y)) != capEnd
        && captures.find(coord(x + 2, y)) != capEnd
        && g->stone_list[player].find(coord(x + 3, y)) != stoneEnd)
    {
        result.insert(coord(x + 1, y));
        result.insert(coord(x + 2, y));
    }
    if (captures.find(coord(x - 1, y)) != capEnd
        && captures.find(coord(x - 2, y)) != capEnd
        && g->stone_list[player].find(coord(x - 3, y)) != stoneEnd)
    {
        result.insert(coord(x - 1, y));
        result.insert(coord(x - 2, y));
    }
    // horizontal
    if (captures.find(coord(x, y + 1)) != capEnd
        && captures.find(coord(x, y + 2)) != capEnd
        && g->stone_list[player].find(coord(x, y + 3)) != stoneEnd)
    {
        result.insert(coord(x, y + 1));
        result.insert(coord(x, y + 2));
    }
    if (captures.find(coord(x, y - 1)) != capEnd
        && captures.find(coord(x, y - 2)) != capEnd
        && g->stone_list[player].find(coord(x, y - 3)) != stoneEnd)
    {
        result.insert(coord(x, y - 1));
        result.insert(coord(x, y - 2));
    }
    // left diagonal
    if (captures.find(coord(x + 1, y + 1)) != capEnd
        && captures.find(coord(x + 2, y + 2)) != capEnd
        && g->stone_list[player].find(coord(x + 3, y + 3)) != stoneEnd)
    {
        result.insert(coord(x + 1, y + 1));
        result.insert(coord(x + 2, y + 2));
    }
    if (captures.find(coord(x - 1, y - 1)) != capEnd
        && captures.find(coord(x - 2, y - 2)) != capEnd
        && g->stone_list[player].find(coord(x - 3, y - 3)) != stoneEnd)
    {
        result.insert(coord(x - 1, y - 1));
        result.insert(coord(x - 2, y - 2));
    }
    // right diagonal
    if (captures.find(coord(x - 1, y + 1)) != capEnd
        && captures.find(coord(x - 2, y + 2)) != capEnd
        && g->stone_list[player].find(coord(x - 3, y + 3)) != stoneEnd)
    {
        result.insert(coord(x - 1, y + 1));
        result.insert(coord(x - 2, y + 2));
    }
    if (captures.find(coord(x + 1, y - 1)) != capEnd
        && captures.find(coord(x + 2, y - 2)) != capEnd
        && g->stone_list[player].find(coord(x + 3, y - 3)) != stoneEnd)
    {
        result.insert(coord(x + 1, y - 1));
        result.insert(coord(x + 2, y - 2));
    }

    std::cout << "[ ";
    for (coordSet::const_iterator it = captures.begin(); it != capEnd; it++)
        std::cout << it->first << " " << it->second << " ";
    std::cout << "]" <<std::endl;

    if (!result.empty())
        std::cout << "Les coord de la pierre qui a fait la capture : " <<  x << " " << y << std::endl;
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
    if (((inSet(coord(x - 1, y), g->stone_list[g->opponent])
        && inSubSet(coord(x + 2, y), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x + 2, y), g->stone_list[g->opponent])
        && inSubSet(coord(x - 1, y),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x + 1, y), g->stone_list[g->player]))
        return true;
    
    if (((inSet(coord(x - 1, y), g->stone_list[g->opponent])
        && inSubSet(coord(x - 2, y), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x - 2, y), g->stone_list[g->opponent])
        && inSubSet(coord(x + 1, y),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x - 1, y), g->stone_list[g->player]))
        return true;

    if (((inSet(coord(x, y + 1), g->stone_list[g->opponent])
        && inSubSet(coord(x, y - 2), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x, y - 2), g->stone_list[g->opponent])
        && inSubSet(coord(x, y + 1),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x, y - 1), g->stone_list[g->player]))
        return true;

    if (((inSet(coord(x, y + 1), g->stone_list[g->opponent])
        && inSubSet(coord(x, y - 2), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x, y - 2), g->stone_list[g->opponent])
        && inSubSet(coord(x, y + 1),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x, y - 1), g->stone_list[g->player]))
        return true;

    if (((inSet(coord(x, y - 1), g->stone_list[g->opponent])
        && inSubSet(coord(x, y + 2), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x, y + 2), g->stone_list[g->opponent])
        && inSubSet(coord(x, y - 1),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x, y + 1), g->stone_list[g->player]))
        return true;

    if (((inSet(coord(x - 1, y - 1), g->stone_list[g->opponent])
        && inSubSet(coord(x + 2, y + 2), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x + 2, y + 2), g->stone_list[g->opponent])
        && inSubSet(coord(x - 1, y - 1),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x + 1, y + 1), g->stone_list[g->player]))
        return true;

    if (((inSet(coord(x + 1, y + 1), g->stone_list[g->opponent])
        && inSubSet(coord(x - 2, y - 2), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x - 2, y - 2), g->stone_list[g->opponent])
        && inSubSet(coord(x + 1, y + 1),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x - 1, y - 1), g->stone_list[g->player]))
        return true;

    if (((inSet(coord(x - 1, y + 1), g->stone_list[g->opponent])
        && inSubSet(coord(x + 2, y - 2), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x + 2, y - 2), g->stone_list[g->opponent])
        && inSubSet(coord(x - 1, y + 1),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x + 1, y - 1), g->stone_list[g->player]))
        return true;
        
    if (((inSet(coord(x + 1, y - 1), g->stone_list[g->opponent])
        && inSubSet(coord(x - 2, y + 2), g->possible_moves, g->forbidden_moves[g->opponent]))
        || (inSet(coord(x - 2, y + 2), g->stone_list[g->opponent])
        && inSubSet(coord(x + 1, y - 1),g->possible_moves, g->forbidden_moves[g->opponent])))
        && inSet(coord(x - 1, y + 1), g->stone_list[g->player]))
        return true;

    return false;
}

bool hasVerticalFreeThree(int x, int y, Game * g, int player)
{
    // ######################### Pattern X000X
    if (inSet(coord(x, y + 1), g->stone_list[player])
        && inSet(coord(x, y + 2), g->stone_list[player])
        && inSet(coord(x, y + 3), g->possible_moves)
        && inSet(coord(x, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x, y - 1), g->stone_list[player])
        && inSet(coord(x, y - 2), g->stone_list[player])
        && inSet(coord(x, y - 3), g->possible_moves)
        && inSet(coord(x, y + 1), g->possible_moves))
        return true;

    if (inSet(coord(x, y - 1), g->stone_list[player])
        && inSet(coord(x, y + 1), g->stone_list[player])
        && inSet(coord(x, y + 2), g->possible_moves)
        && inSet(coord(x, y - 2), g->possible_moves))
        return true;                

    // ######################## Pattern X00X0X

    if (inSet(coord(x, y - 1), g->stone_list[player])
        && inSet(coord(x, y - 3), g->stone_list[player])
        && inSet(coord(x, y - 2), g->possible_moves)
        && inSet(coord(x, y - 4), g->possible_moves)
        && inSet(coord(x, y + 1), g->possible_moves))
        return true;

    if (inSet(coord(x, y + 1), g->stone_list[player])
        && inSet(coord(x, y - 2), g->stone_list[player])
        && inSet(coord(x, y + 2), g->possible_moves)
        && inSet(coord(x, y - 3), g->possible_moves)
        && inSet(coord(x, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x, y + 2), g->stone_list[player])
        && inSet(coord(x, y + 3), g->stone_list[player])
        && inSet(coord(x, y + 1), g->possible_moves)
        && inSet(coord(x, y + 4), g->possible_moves)
        && inSet(coord(x, y - 1), g->possible_moves))
        return true;

    // ######################### Pattern X0X00X

    if (inSet(coord(x, y + 1), g->stone_list[player])
        && inSet(coord(x, y + 3), g->stone_list[player])
        && inSet(coord(x, y + 2), g->possible_moves)
        && inSet(coord(x, y + 4), g->possible_moves)
        && inSet(coord(x, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x, y - 1), g->stone_list[player])
        && inSet(coord(x, y + 2), g->stone_list[player])
        && inSet(coord(x, y + 1), g->possible_moves)
        && inSet(coord(x, y - 2), g->possible_moves)
        && inSet(coord(x, y + 3), g->possible_moves))
        return true;

    if (inSet(coord(x, y - 2), g->stone_list[player])
        && inSet(coord(x, y - 3), g->stone_list[player])
        && inSet(coord(x, y + 1), g->possible_moves)
        && inSet(coord(x, y - 1), g->possible_moves)
        && inSet(coord(x, y - 4), g->possible_moves))
        return true;

    return false;
}

bool hasHorizontalFreeThree(int x, int y, Game * g, int player)
{
    // ######################### Pattern X000X
    if (inSet(coord(x + 1, y), g->stone_list[player])
        && inSet(coord(x + 2, y), g->stone_list[player])
        && inSet(coord(x + 3, y), g->possible_moves)
        && inSet(coord(x - 1, y), g->possible_moves))
        return true;

    if (inSet(coord(x - 1, y), g->stone_list[player])
        && inSet(coord(x - 2, y), g->stone_list[player])
        && inSet(coord(x - 3, y), g->possible_moves)
        && inSet(coord(x + 1, y), g->possible_moves))
        return true;

    if (inSet(coord(x - 1, y), g->stone_list[player])
        && inSet(coord(x + 1, y), g->stone_list[player])
        && inSet(coord(x + 2, y), g->possible_moves)
        && inSet(coord(x - 2, y), g->possible_moves))
        return true;                

    // ######################## Pattern X00X0X

    if (inSet(coord(x - 1, y), g->stone_list[player])
        && inSet(coord(x - 3, y), g->stone_list[player])
        && inSet(coord(x - 2, y), g->possible_moves)
        && inSet(coord(x - 4, y), g->possible_moves)
        && inSet(coord(x + 1, y), g->possible_moves))
        return true;

    if (inSet(coord(x + 1, y), g->stone_list[player])
        && inSet(coord(x - 2, y), g->stone_list[player])
        && inSet(coord(x + 2, y), g->possible_moves)
        && inSet(coord(x - 3, y), g->possible_moves)
        && inSet(coord(x - 1, y), g->possible_moves))
        return true;

    if (inSet(coord(x + 2, y), g->stone_list[player])
        && inSet(coord(x + 3, y), g->stone_list[player])
        && inSet(coord(x + 1, y), g->possible_moves)
        && inSet(coord(x + 4, y), g->possible_moves)
        && inSet(coord(x - 1, y), g->possible_moves))
        return true;

    // ######################### Pattern X0X00X

    if (inSet(coord(x + 1, y), g->stone_list[player])
        && inSet(coord(x + 3, y), g->stone_list[player])
        && inSet(coord(x + 2, y), g->possible_moves)
        && inSet(coord(x + 4, y), g->possible_moves)
        && inSet(coord(x - 1, y), g->possible_moves))
        return true;

    if (inSet(coord(x - 1, y), g->stone_list[player])
        && inSet(coord(x + 2, y), g->stone_list[player])
        && inSet(coord(x + 1, y), g->possible_moves)
        && inSet(coord(x - 2, y), g->possible_moves)
        && inSet(coord(x + 3, y), g->possible_moves))
        return true;

    if (inSet(coord(x - 2, y), g->stone_list[player])
        && inSet(coord(x - 3, y), g->stone_list[player])
        && inSet(coord(x + 1, y), g->possible_moves)
        && inSet(coord(x - 1, y), g->possible_moves)
        && inSet(coord(x - 4, y), g->possible_moves))
        return true;

    return false;
}


bool hasLeftDiagonalFreeThree(int x, int y, Game * g, int player)
{
    // ######################### Pattern X000X
    if (inSet(coord(x + 1, y + 1), g->stone_list[player])
        && inSet(coord(x + 2, y + 2), g->stone_list[player])
        && inSet(coord(x + 3, y + 3), g->possible_moves)
        && inSet(coord(x - 1, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x - 1, y - 1), g->stone_list[player])
        && inSet(coord(x - 2, y - 2), g->stone_list[player])
        && inSet(coord(x - 3, y - 3), g->possible_moves)
        && inSet(coord(x + 1, y + 1), g->possible_moves))
        return true;

    if (inSet(coord(x - 1, y - 1), g->stone_list[player])
        && inSet(coord(x + 1, y + 1), g->stone_list[player])
        && inSet(coord(x + 2, y + 2), g->possible_moves)
        && inSet(coord(x - 2, y - 2), g->possible_moves))
        return true;                

    // ######################## Pattern X00X0X

    if (inSet(coord(x - 1, y - 1), g->stone_list[player])
        && inSet(coord(x - 3, y - 3), g->stone_list[player])
        && inSet(coord(x - 2, y - 2), g->possible_moves)
        && inSet(coord(x - 4, y - 4), g->possible_moves)
        && inSet(coord(x + 1, y + 1), g->possible_moves))
        return true;

    if (inSet(coord(x + 1, y + 1), g->stone_list[player])
        && inSet(coord(x - 2, y - 2), g->stone_list[player])
        && inSet(coord(x + 2, y + 2), g->possible_moves)
        && inSet(coord(x - 3, y - 3), g->possible_moves)
        && inSet(coord(x - 1, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x + 2, y + 2), g->stone_list[player])
        && inSet(coord(x + 3, y + 3), g->stone_list[player])
        && inSet(coord(x + 1, y + 1), g->possible_moves)
        && inSet(coord(x + 4, y + 4), g->possible_moves)
        && inSet(coord(x - 1, y - 1), g->possible_moves))
        return true;

    // ######################### Pattern X0X00X

    if (inSet(coord(x + 1, y + 1), g->stone_list[player])
        && inSet(coord(x + 3, y + 3), g->stone_list[player])
        && inSet(coord(x + 2, y + 2), g->possible_moves)
        && inSet(coord(x + 4, y + 4), g->possible_moves)
        && inSet(coord(x - 1, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x - 1, y - 1), g->stone_list[player])
        && inSet(coord(x + 2, y + 2), g->stone_list[player])
        && inSet(coord(x + 1, y + 1), g->possible_moves)
        && inSet(coord(x - 2, y - 2), g->possible_moves)
        && inSet(coord(x + 3, y + 3), g->possible_moves))
        return true;

    if (inSet(coord(x - 2, y - 2), g->stone_list[player])
        && inSet(coord(x - 3, y - 3), g->stone_list[player])
        && inSet(coord(x + 1, y + 1), g->possible_moves)
        && inSet(coord(x - 1, y - 1), g->possible_moves)
        && inSet(coord(x - 4, y - 4), g->possible_moves))
        return true;

    return false;
}

bool hasRightDiagonalFreeThree(int x, int y, Game * g, int player)
{
    // ######################### Pattern X000X
    if (inSet(coord(x - 1, y + 1), g->stone_list[player])
        && inSet(coord(x - 2, y + 2), g->stone_list[player])
        && inSet(coord(x - 3, y + 3), g->possible_moves)
        && inSet(coord(x + 1, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x + 1, y - 1), g->stone_list[player])
        && inSet(coord(x + 2, y - 2), g->stone_list[player])
        && inSet(coord(x + 3, y - 3), g->possible_moves)
        && inSet(coord(x - 1, y + 1), g->possible_moves))
        return true;

    if (inSet(coord(x + 1, y - 1), g->stone_list[player])
        && inSet(coord(x - 1, y + 1), g->stone_list[player])
        && inSet(coord(x - 2, y + 2), g->possible_moves)
        && inSet(coord(x + 2, y - 2), g->possible_moves))
        return true;                

    // ######################## Pattern X00X0X

    if (inSet(coord(x + 1, y - 1), g->stone_list[player])
        && inSet(coord(x + 3, y - 3), g->stone_list[player])
        && inSet(coord(x + 2, y - 2), g->possible_moves)
        && inSet(coord(x + 4, y - 4), g->possible_moves)
        && inSet(coord(x - 1, y + 1), g->possible_moves))
        return true;

    if (inSet(coord(x - 1, y + 1), g->stone_list[player])
        && inSet(coord(x + 2, y - 2), g->stone_list[player])
        && inSet(coord(x - 2, y + 2), g->possible_moves)
        && inSet(coord(x + 3, y - 3), g->possible_moves)
        && inSet(coord(x + 1, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x - 2, y + 2), g->stone_list[player])
        && inSet(coord(x - 3, y + 3), g->stone_list[player])
        && inSet(coord(x - 1, y + 1), g->possible_moves)
        && inSet(coord(x - 4, y + 4), g->possible_moves)
        && inSet(coord(x + 1, y - 1), g->possible_moves))
        return true;

    // ######################### Pattern X0X00X

    if (inSet(coord(x - 1, y + 1), g->stone_list[player])
        && inSet(coord(x - 3, y + 3), g->stone_list[player])
        && inSet(coord(x - 2, y + 2), g->possible_moves)
        && inSet(coord(x - 4, y + 4), g->possible_moves)
        && inSet(coord(x + 1, y - 1), g->possible_moves))
        return true;

    if (inSet(coord(x + 1, y - 1), g->stone_list[player])
        && inSet(coord(x - 2, y + 2), g->stone_list[player])
        && inSet(coord(x - 1, y + 1), g->possible_moves)
        && inSet(coord(x + 2, y - 2), g->possible_moves)
        && inSet(coord(x - 3, y + 3), g->possible_moves))
        return true;

    if (inSet(coord(x + 2, y - 2), g->stone_list[player])
        && inSet(coord(x + 3, y - 3), g->stone_list[player])
        && inSet(coord(x - 1, y + 1), g->possible_moves)
        && inSet(coord(x + 1, y - 1), g->possible_moves)
        && inSet(coord(x + 4, y - 4), g->possible_moves))
        return true;
    
    return false;
}

# endif