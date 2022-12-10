# ifndef GLOBAL_HPP
# define GLOBAL_HPP

# include <set>
# include <map>
# include <unordered_set>
# include <unordered_map>
# include <stack>
# include <iostream>

# include "CheckRules.hpp"
# include "CheckHeuristic.hpp"


typedef std::pair<int, int >			coord;
typedef std::unordored_set< coord >		coordSet;
typedef std::stack< coord >				coordStack;
typedef std::stack< coordSet >			coordStackSet;
// Not sure
typedef std::unordered_map				hashMap;

# endif