#ifndef _EDM_PER_
#define _EDM_PER_
#include<vector>

using namespace std;

extern "C" vector<int> EDM_percent(const vector<double>& Z, int min_size, double beta, int degree);

#endif
