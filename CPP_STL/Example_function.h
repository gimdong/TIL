/**
 * 뇌를 자극 하는 C++ STL
 * exmple code
 * 한빛미디어
 */

#include <iostream>
using namespace std;

// Ch01
namespace Ch01 {

    class Point
    {
    private:
        int x, y;
    public:
        Point(int _x = 0, int _y = 0):x(_x),y(_y) {}
        void print() const { cout << x << ',' << y << endl;}
        
        const Point operator+(Point& arg);
        const Point operator-(Point& arg);
        const Point operator*(Point& arg);
        const Point operator/(Point& arg);
        const Point operator%(Point& arg);

        const Point& operator++(); // Prefix(전위)
        const Point operator++(int);  // Postfix(후위)
        const Point& operator--();
        const Point operator--(int);
        const bool operator!(); // Prefix(전위) x,y 둘 다 true(0이 아닌 경우) 인 경우에만 true 반

    };
    //Section 01 .. TIL #4
    int Ex01(void);
    int Ex02(void);
    //Section 02 .. TIL #5
    int Section02(void);
    //Section 03 .. TIL #6
    int Section03(void);
}

