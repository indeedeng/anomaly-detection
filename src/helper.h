#ifndef my_help_func
#define my_help_func

#include<set>
#include<algorithm>
#include<cmath>


double get_median(std::multiset<double>&, std::multiset<double, std::greater<double> >&);
void insert_element(std::multiset<double>&, std::multiset<double, std::greater<double> >&, const double);
void remove_element(std::multiset<double>&, std::multiset<double, std::greater<double> >&, const double);

extern double Linear(const double x);
extern double Const(const double x);
extern double Quadratic(const double x);

class EDMResult {
public:
    int best_loc;
    double best_stat;
    EDMResult(const int, const double);
};

#endif
