#ifndef _EDM_MULTI_
#define _EDM_MULTI_
#include<vector>

using namespace std;

extern "C" vector<int> EDM_multi(const vector<double>& Z, int min_size, double beta, int degree);

#endif
