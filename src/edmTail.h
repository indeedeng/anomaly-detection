#ifndef _EDM_TAIL_
#define _EDM_TAIL_
#include<vector>
#include"helper.h"


extern "C" EDMResult EDM_tail(std::vector<double>& Z, const int min_size, const double alpha, const double quant);

#endif
