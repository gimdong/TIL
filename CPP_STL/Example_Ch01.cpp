#include "./Example_function.h"
using namespace Ch01;

int Ch01::Ex01(void)
{
    int n1 = 10, n2 = 20;
    cout << n1 + n2 << endl; // 기본 연산자
    return 0;
}
int Ch01::Ex02(void)
{
    class Temp_Point{};
    Temp_Point p1, p2;
    //p1 + p2; // Error! 이러한 피연산자와 일치하는 연산자 + 가 없습니다.
    return 0;
}


const Point Point::operator+(Point& arg)
{
    Point pt; 
    cout << "operator + 호출" << endl; 
    pt.x = this->x + arg.x;
    pt.y = this->y + arg.y;
    return pt;
}
const Point Point::operator-(Point& arg)
{
    Point pt; 
    cout << "operator - 호출" << endl; 
    pt.x = this->x - arg.x;
    pt.y = this->y - arg.y;
    return pt;
}
const Point Point::operator*(Point& arg)
{
    Point pt; 
    cout << "operator * 호출" << endl; 
    pt.x = this->x * arg.x;
    pt.y = this->y * arg.y;
    return pt;
}
const Point Point::operator/(Point& arg)
{
    Point pt; 
    cout << "operator / 호출" << endl; 
    pt.x = this->x / arg.x;
    pt.y = this->y / arg.y;
    return pt;
}
const Point Point::operator%(Point& arg)
{
    Point pt; 
    cout << "operator % 호출" << endl; 
    pt.x = this->x % arg.x;
    pt.y = this->y % arg.y;
    return pt;
}

int Ch01::Ex03_04_05_06(void)
{
    Point p1(2,3);
    Point p2(4,5);
    Point p3;

    p3 = p1 + p2;
    p3.print();
    p3 = p1 - p2;
    p3.print();
    p3 = p1 * p2;
    p3.print();
    p3 = p1 / p2;
    p3.print();
    p3 = p1 % p2;
    p3.print();




    return 0;
}