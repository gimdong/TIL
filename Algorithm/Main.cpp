#include <iostream>
#include "Fn_list.h"

using namespace std;    

VEC_FN gVc_list; 
#define REG_ITEM(_A,_B) gVc_list.push_back({_A,_B})

int main(void)
{
    
    REG_ITEM("graph adjacency matrix", graph_adjacency_matrix);
    
    
    int nIter_ix = 0;
    for(auto it = gVc_list.begin(); it != gVc_list.end(); ++it)
    {
        cout <<"["<< nIter_ix++ <<"] " << it->first << endl;
    }

    cout << "select item : ";
    cin >> nIter_ix;

    gVc_list[nIter_ix].second();

    return 0;
}