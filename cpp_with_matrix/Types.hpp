# ifndef TYPES_HPP
# define TYPES_HPP

# include <set>
# include <map>
# include <unordered_set>
# include <unordered_map>
# include <stack>
# include <iostream>
# include <bitset>
# include <vector>
# include <sstream>



struct pairhash {
public:
  template <typename T, typename U>
  std::size_t operator()(const std::pair<T, U> &x) const
  {
	return std::hash<T>()(x.first) ^ std::hash<U>()(x.second);
  }
};

typedef typename std::pair<int, int >			    coord;

typedef typename std::unordered_set<coord, pairhash>	    coordSet;
//typedef typename std::set<coord>	    coordSet;
typedef typename std::unordered_map<int, coordSet >			mapCoordSet;
typedef typename std::stack< coord >				coordStack;
typedef typename std::stack< coordSet >			    coordStackSet;

# endif