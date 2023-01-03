
# include <set>
# include <iostream>

typedef std::pair<int, int > coord;

int main()
{
    std::set<coord> s;
    std::set<coord> s2;

    s.insert(coord(1, 1));
    s.insert(coord(1, 2));
    s.insert(coord(1, 3));

    s2.insert(coord(1, 2));
    s2.insert(coord(1, 3));

    for (std::set<coord>::const_iterator it = s2.begin();
    it != s2.end(); it++)
        s.erase(*it);

    for (std::set<coord>::const_iterator it = s.begin();
    it != s.end(); it++)
        std::cout << "(" << it->first << " " << it->second << ") ";
    std::cout << std::endl;



}