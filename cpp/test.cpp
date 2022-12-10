
# include "globals.hpp"

int main()
{
	Game g = Game();

	std::cout << g.goban_size << std::endl;
	/*
	std::bitset<361> p1;
	std::bitset<361> p2;
	std::vector<int> v;
	std::set<int> s;

	for (int i = 0; i < 361; i++)
		v.push_back(i);

 	int x = 2, y = 1;
	std::cout << sizeof(p1) << std::endl;
	std::cout << sizeof(v) << std::endl;
	std::cout << sizeof(s) << std::endl;

	p1[y * 19 + x] = 1;
	p2[y * 19 + 1] = 1;

 	
	std::cout << (p2 | p1) << std::endl;
	for (int i = 0; i < 361; i++) {
		std::cout << p1[i] << "\t";
		if ((i + 1) % 19 == 0)
			std::cout << std::endl;
	}
	*/
}
