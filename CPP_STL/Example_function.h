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
    };
    //Section 01 .. TIL #4
    int Ex01(void);
    int Ex02(void);
    //Section 02 .. TIL #5
    int Ex03_04_05_06(void);
    int Ex_const_member_function(void);
}

