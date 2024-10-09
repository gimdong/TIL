/** gimdong Ghaph(Adjacency matrix) Code.
 * \copyright Copyright 2024 gimdong All rights reserved.
 */

/**
 * 노드의 개수가 N 인 가중치 그래프에서 인접행렬(adjacency matrix)방법으로 
 * 간선을 추가(add_edge) / 삭제(delete_edge) 하는 기능을 추가 하고
 * 해당 노드의 차수(print_dgree), matrix 출력(print martix) 하는 기능을 추가한다.
 */
#include "./Fn_list.h"


#define INIT_GRAPGH     (100)
#define ADD_EDGE        (200)
#define DELETE_EDGE     (300)
#define PRINT_EDGE      (400)
#define PRINT_GRAPH     (500)
#define TERMINATE       (999)

#define MAX_N           (1000)

int gaanMatrix[MAX_N][MAX_N] = { 0,};

/**
 * @fn add_edge
 * @brief input(nDepatture -> nDestination with nWeight)
 * @return
 *      0 : matrix has already edge ...  and change a new _weight
 *      1 : fn makes a new edge
 */
int add_edge(void)
{
    int nDeparture, nDestination, nWeight;
    printf("-1. input (Depature, Destination, Weight)");
    scanf("%d %d %d",&nDeparture, &nDestination, &nWeight);
    printf("add edge (%d,%d) = %d \n",nDeparture, nDestination, nWeight);
    return 0;    
}

int graph_adjacency_matrix(void)
{
    int nCMD = 0;
    printf("Start [%s]\n",__FUNCTION__);

    while(TERMINATE != nCMD)
    {
        printf("input CMD :"); scanf("%d", &nCMD);

        switch (nCMD)
        {
        case ADD_EDGE:
            add_edge();
            break;
        
        default:
            printf("It was wrong CMD[%d]", nCMD);
            break;
        }
    }

    printf("Terminate [%s]\n",__FILE__);
    return 0;
}