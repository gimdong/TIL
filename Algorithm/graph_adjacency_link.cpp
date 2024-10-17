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

//#define VER_1 // Linked List 로 양방향 그래프 구현
//#define VER_1_2 // Linked List 로 방향+가중치 그래프 구현
#define VER_2 // vector 로 방향+가중치 그래프 구현

#ifdef VER_1
typedef struct Node{
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
    /*정점의 이름...배열의 인덱스는 (그래프에) 몇번째 등록된 정점인가를 의미*/char m_vertices[MAX_N];
    /*인접 리스트...배열의 인덱스는 (그래프에) 몇번째 등록된 정점인가를 의미*/Node* m_adjlist[MAX_N];
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

#endif

#ifdef VER_1_2

struct Node{
    char m_ID;
    Node* m_next;
    int m_weight;
};

class AdjList{
private:
    
    int m_TotalNodeCnt = 0;
    int m_TotalEdgeCnt = 0;
    Node* m_HeadNode[MAX_N];

public:
    AdjList(){
        m_TotalNodeCnt = 0;
        m_TotalEdgeCnt = 0;
    }
    ~AdjList(){}

    //insert Node
    void mInsertNode(char _ID){
        m_HeadNode[m_TotalNodeCnt] = new Node();
        m_HeadNode[m_TotalNodeCnt]->m_ID = _ID;
        m_HeadNode[m_TotalNodeCnt]->m_next = NULL;
        m_HeadNode[m_TotalNodeCnt]->m_weight = 0;
        m_TotalNodeCnt++;
    }
    //insert Edge
    void mInsertEdge(char _pID, char _dID, int _weight){
        f(i,0,m_TotalNodeCnt){
            if(_pID == m_HeadNode[i]->m_ID){
                Node* Head = m_HeadNode[i];
                while(NULL != Head->m_next){
                    Head = Head->m_next;
                }
                Head->m_next = new Node();
                Head->m_next->m_ID = _dID;
                Head->m_next->m_next = NULL;
                Head->m_next->m_weight = _weight;
                m_TotalEdgeCnt++;
                break;
            }
        }
    }

    //delete Node
    void mDeleteNode(char _ID){
        f(i,0,m_TotalNodeCnt)
            mDeleteEdge(_ID, m_HeadNode[i]->m_ID);

        f(i,0,m_TotalNodeCnt){
            if(_ID == m_HeadNode[i]->m_ID){
                m_HeadNode[i] = NULL;
                f(j,i,m_TotalNodeCnt){
                    m_HeadNode[j] = m_HeadNode[(j-i)+(i+1)];
                }
                m_TotalNodeCnt--;
                break;
            }
        }
    }
    
    //delete Edge
    void mDeleteEdge(char _pID, char _dID){
        f(i,0,m_TotalNodeCnt){
            Node* head = m_HeadNode[i];
            if(_pID == head->m_ID){
                while(NULL != head->m_next){
                    if(_dID == head->m_next->m_ID){
                        Node* temp = head->m_next->m_next;
                        head->m_next = temp;
                        m_TotalEdgeCnt--;
                        return;
                    }
                    else{
                        head = head->m_next;
                    }
                }
            }
        }        
    }

    //Display
    void mDisplay(void){
        cout << "Total Node Count : " << m_TotalNodeCnt << endl;
        cout << "Total Edge Count : " << m_TotalEdgeCnt << endl;

        f(i,0,m_TotalNodeCnt){
            if(NULL == m_HeadNode[i])   continue;
            
            cout << m_HeadNode[i]->m_ID;
            Node* head = m_HeadNode[i];
            while(NULL != (head->m_next)){
                cout << "->" << head->m_next->m_ID << "(" << head->m_next->m_weight << ")"; 
                head = head->m_next;
            }
            cout << endl;
        }
    }
};


int graph_adjacency_list(void)
{
    AdjList graph;

    graph.mInsertNode('A');
    graph.mInsertNode('B');
    graph.mInsertNode('C');
    graph.mInsertNode('D');
    graph.mInsertNode('E');
    graph.mInsertNode('F');
    graph.mDisplay();
    H_LINE

    graph.mInsertEdge('A','B',4);
    graph.mInsertEdge('B','C',3);
    graph.mInsertEdge('B','D',2);
    graph.mInsertEdge('C','E',7);
    graph.mInsertEdge('D','E',9);
    graph.mInsertEdge('E','F',5);
    graph.mDisplay();
    H_LINE

    graph.mDeleteEdge('B','D');
    graph.mDisplay();
    H_LINE

    graph.mDeleteNode('D');
    graph.mDisplay();
    H_LINE

    return 0;
}
#endif

#ifdef VER_2

#include <vector>
using namespace std;

/**
 * 아래를 구현해 보자
 * A→(4)→B→(3)→C→(7)→E→(5)→F
 *        ↘︎︎        ↗️  ️
 *         (2)   (9)
 *            ↘ ↗️
 *             D︎ ︎
 */


class AdjList
{
private :

    int _nNode_count;
    char _cNode[MAX_N];
    vector<pair<char,int>> _vMap[MAX_N]; // char : _name, int : _weight

public :
    AdjList(){
        _nNode_count = 0;
        f(i,0,MAX_N){
            _cNode[i] = '\0';
            _vMap[i].clear();
        }
    }

    //InsertNode
    void mInsertNode(char _ID){
        _cNode[_nNode_count++] = _ID;
    }
    //InsertEdge
    void mInsertEdge(char _pID, char _dID, int _weight){
        f(i,0,_nNode_count){
            if(_cNode[i] == _pID){
                //_vMap[i].push_back(make_pair(_dID,_weight));
                _vMap[i].push_back({_dID,_weight});
            }
        }
    }
    //DeleteNode
    void mDeleteNode(char _ID){
        f(i,0,_nNode_count){
            for(auto iter = _vMap[i].begin(); iter != _vMap[i].end(); ++iter){
                if(iter->first == _ID){ // 여기서 Error : BAD_ACCESS // iter가 ???? 으로 확인됨. Todo...
                    _vMap[i].erase(iter);
                    break; 
                    // Error의 원인은 지워야 되는 부분이 마지막에 있을 경우 iter가 for문의 조건문에서 end를 넘어간 상태가 되므로 무한 Loop에 빠지게 된다.
                    // 그러므로 vertor의 erase는 주의 해야 한다.
                }
            }
        }
        f(i,0,_nNode_count){
            if(_cNode[i] == _ID){
                f(j,i,_nNode_count){

                    if(j+1 != _nNode_count){
                        _cNode[j] = _cNode[j+1];
                        _vMap[j] = _vMap[j+1];
                    }
                    else{
                        _cNode[j] = '\0';
                        _vMap[j].clear();
                    }
                }
                _nNode_count--;
                return;
            }
        }
    }
    //DeleteEdge
    void mDeleteEdge(char _pID, char _dID){
        f(i,0,_nNode_count){
            if(_cNode[i] == _pID){
                for(auto iter = _vMap[i].begin(); iter != _vMap[i].end(); ++iter){
                    if(iter->first == _dID){
                        _vMap[i].erase(iter);
                        return;
                    }
                }
            }
        }
    }
    //Display
    void mDisplay(void){
        cout << "Total Node Count : " << _nNode_count << endl;

        f(i,0,_nNode_count){
            cout << _cNode[i];
            for(auto iter=_vMap[i].begin(); iter != _vMap[i].end(); ++iter){
                cout << "->" << iter->first << "(" << iter->second << ")"; 
            }
            cout << endl;
        }      
    }

};



int graph_adjacency_list(void)
{
    AdjList graph;

    graph.mInsertNode('A');
    graph.mInsertNode('B');
    graph.mInsertNode('C');
    graph.mInsertNode('D');
    graph.mInsertNode('E');
    graph.mInsertNode('F');
    graph.mDisplay();
    H_LINE

    graph.mInsertEdge('A','B',4);
    graph.mInsertEdge('B','C',3);
    graph.mInsertEdge('B','D',2);
    graph.mInsertEdge('C','E',7);
    graph.mInsertEdge('D','E',9);
    graph.mInsertEdge('E','F',5);
    graph.mDisplay();
    H_LINE

    graph.mDeleteEdge('B','D');
    graph.mDisplay();
    H_LINE

    graph.mDeleteNode('D');
    graph.mDisplay();
    H_LINE




    return 0;
}
#endif