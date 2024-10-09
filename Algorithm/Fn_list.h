#ifndef _FN_LIST_H_
#define _FN_LIST_H_


#include <stdio.h>
#include <vector>

using namespace std;

typedef int(* FN)(void);
typedef vector<pair<string,FN>> VEC_FN;


int graph_adjacency_matrix(void);


#endif