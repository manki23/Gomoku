#include <set>
#include <iostream>
#include <map>

typedef std::set<std::pair<int, int > > coordSet;
typedef std::pair<int, int> coord;

std::set<int> test_return_set(void)
{
	std::set<int> test { 1, 2, 3 };

	return test;
}

int main()
{
	std::set<int> test = test_return_set();
	std::set<int> test2 = test;

	test2.erase(2);

	for (std::set<int>::const_iterator it = test.begin();
	it != test.end(); it++)
		std::cout << *it << std::endl;

	for (std::set<int>::const_iterator it = test2.begin();
	it != test2.end(); it++)
		std::cout << *it << std::endl; 

}
