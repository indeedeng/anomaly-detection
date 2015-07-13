#ifndef _EDM_TAIL_
#define _EDM_TAIL_
#include<vector>
#include"helper.h"

using namespace std;

extern "C" EDMResult EDM_tail(vector<double>& Z, int min_size, double beta, int degree);

#endif
