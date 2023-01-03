
# include <set>
# include <iostream>
# include "Types.hpp"

typedef std::pair<int, int > coord;

int main()
{

    bset    a;
    bset    b;

    b = ~a;

    std::cout << "================================================" << std::endl;
    a[3 + (1 * 19)] = 'R';
    a[4 + (10 * 19)] = 'R';
    a[18 + (18 * 19)] = 'R';
    // a[0 + (3 * 19)] = 'U';
    for (int i = 0; i < a.size(); i++) {
        if (i != 0 && i % 19 == 0) {
            std::cout << std::endl;
        }
        std::cout << "\t" << a[i];
    }
    std::cout << std::endl;
    std::cout << a.size() << std::endl;

    std::cout <<"================================================" << std::endl;
    std::cout << a << std::endl;
    std::cout <<"================================================" << std::endl;
    std::cout << a.count() << std::endl;
    std::cout <<"================================================" << std::endl;
    std::cout <<  b << std::endl;
    std::cout <<"================================================" << std::endl;


    std::set<coord> s;
    std::set<coord> s2;

    s.insert(coord(1, 1));
    s.insert(coord(1, 2));
    s.insert(coord(1, 3));

    s2.insert(coord(1, 2));
    s2.insert(coord(1, 3));
    // std::cout << sizeof(s) << std::endl;

    // for (std::set<coord>::const_iterator it = s2.begin(); it != s2.end(); it++)
    //     std::cout << it->first << " " << it->second;
    // std::cout << std::endl;

    // for (std::set<coord>::const_iterator it = s2.begin(); it != s2.end(); it++)
    //     s.erase(*it);

    // for (std::set<coord>::const_iterator it = s.begin(); it != s.end(); it++)
    //     std::cout << "(" << it->first << " " << it->second << ") ";
    // std::cout << std::endl;

    return 0;

}