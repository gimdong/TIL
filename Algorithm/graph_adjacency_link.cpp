/** gimdong ghaph(adjacency matrix) code.
 * \copyright copyright 2024 gimdong all rights reserved.
 */

/**
 * 노드의 개수가 n 인 가중치 그래프에서 인접 리스트(adjacency list)방법으로 
 * 간선을 추가(add_edge) / 삭제(delete_edge) 하는 기능을 추가 하고
 * 해당 노드의 차수(print_dgree), matrix 출력(print martix) 하는 기능을 추가한다.
 */
#include "./Fn_list.h"


#define MAX_N           (1000)
#define MAX_WEIGHT      (10)
#define f(i,s,e)        for(int i = s; i < e; ++i)
#define H_LINE          f(i, 0, 10) printf("-"); printf("\n");
struct Node{
    /*정점의 id*/int m_nId;
    /*인접 Node*/Node* m_nNode;

    Node(int _id, Node* _node){ // 초기화 함수
        m_nId = _id;
        m_nNode = _node;
    }
    ~Node(){};

    //getter setter
    int mGetID(){return m_nId;}
    Node* mGetNextNode(){return m_nNode;}  
    void mSetID(int _id){m_nId = _id;}
    void mSetNextNode(Node* _node){m_nNode = _node;}
};

class AdjListGraph{
private:
    /*정점의 개수*/int m_size;
    /*정점의 이름*/char m_vertices[MAX_N];
    /*인접 리스트*/Node* m_adjlist[MAX_N];
public:
    AdjListGraph(){
        m_size = 0;
    }
    ~AdjListGraph(){}

    //getter setter
    int mGetSize(){return m_size;}
    char mGetVertex(int _i){return m_vertices[_i];}
    int mGetVertex(char _name){
        int ret;
        f(i,0,m_size){
            if(_name == m_vertices[i]) ret = i;
        }
        return ret; // the value 'ret' is being used without being initialized.
    }
    Node* mGetAdjlist(int _i){return m_adjlist[_i];}
    void mSetVertex(char _name){
        m_vertices[m_size] = _name;
        m_adjlist[m_size++] = NULL;
    }
    void mSetEdge(int _a, int _b){
       m_adjlist[_a] = new Node(_b, m_adjlist[_a]); // <_a,_b> directed graph
       m_adjlist[_b] = new Node(_a, m_adjlist[_b]); // (_a,_b) undirected graph
    }


    //그래프 정보 출력
    void mDisplay(){
        printf("node(vertex) size : %d\n",mGetSize());
        f(i,0,mGetSize()){
            printf("%c : ",mGetVertex(i));
            Node* head = mGetAdjlist(i);
            while(head != NULL){
                printf("%c ",mGetVertex(head->mGetID()));
                head = head->mGetNextNode();
            }
            printf("\n");
        }
    }

    //insert node
    void mInsertNode(char _name){
        if(MAX_N <= m_size){
            printf("Graph is Full\n");
            return;
        }
        mSetVertex(_name);
    }
    //insert edge
    void mInsertEdge(int _u, int _v){

    }
    //delete node

    //delete edge

};

int graph_adjacency_list(void)
{
    AdjListGraph graph;

    graph.mInsertNode('0');
    graph.mInsertNode('1');
    graph.mInsertNode('2');
    graph.mInsertNode('3');

    graph.mDisplay();
    H_LINE

    graph.mSetEdge(graph.mGetVertex('0'),graph.mGetVertex('1'));
    graph.mSetEdge(graph.mGetVertex('1'),graph.mGetVertex('2'));
    graph.mSetEdge(graph.mGetVertex('1'),graph.mGetVertex('3'));
    graph.mSetEdge(graph.mGetVertex('2'),graph.mGetVertex('3'));
    //graph.mSetEdge(0,1);
    graph.mDisplay();

    return 0;
}