#include<set>
#include<algorithm>
#include<cmath>
#include"helper.h"

extern double Linear(const double x){ return 1;}
extern double Const(const double x){ return 0;}
extern double Quadratic(const double x){ return 2*x+1;}


/*
Use 2 multisets (red-black trees) to keep track of the median. One tree for the larger (m) and 
one for the smaller (M) observations. Insertion and deletion in O(log(n)) and find 
the median in O(1), additional memory use is O(n).
*/

//insert x into the appropriate tree
extern void insert_element(std::multiset<double>& m, std::multiset<double, std::greater<double> >& M, double x){
	
	if(m.empty() || x < *(m.begin()))
		M.insert(x);
	else
		m.insert(x);
	if(m.size() > M.size() + 1){
		std::multiset<double>::iterator i;
		i = m.begin();
		M.insert(*i);
		m.erase(m.begin());
	}
	else if(M.size() > m.size() + 1){
		std::multiset<double, std::greater<double> >::iterator i;
		i = M.begin();
		m.insert(*i);
		M.erase(M.begin());
	}
}

//given a pair of trees obtain the median
extern double get_median(std::multiset<double>& m, std::multiset<double, std::greater<double> >& M){

	if(m.size() > M.size())
		return *(m.begin());
	else if(M.size() > m.size())
		return *(M.begin());
	else
		return ( *(M.begin()) + *(m.begin()) )/2;
}

//remove x from the tree, if multiple copies of x exist only remove 1
//since this method is never called by the user directly it is assumed 
//that there is at least 1 copy of x
extern void remove_element(std::multiset<double>& m, std::multiset<double, std::greater<double> >& M, const double x){

	if(x < *(m.begin())){
		std::multiset<double, std::greater<double> >::iterator i = M.find(x);
		M.erase(i);
	}
	else{
		std::multiset<double>::iterator i = m.find(x);
		m.erase(i);
	}
	if(m.size() > M.size() + 1){
		std::multiset<double>::iterator i;
		i = m.begin();
		M.insert(*i);
		m.erase(m.begin());
	}
	else if(M.size() > m.size() + 1){
		std::multiset<double, std::greater<double> >::iterator i;
		i = M.begin();
		m.insert(*i);
		M.erase(M.begin());
	}
}

EDMResult::EDMResult(const int best_loc, const double best_stat) {
	this->best_loc = best_loc;
	this->best_stat = best_stat;
}
