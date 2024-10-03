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

//이항연산자
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

int Ch01::Section02(void)
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

//단항연산자
const Point& Point::operator++()
{
    ++x;
    ++y;
    return *this;
}
const Point Point::operator++(int)
{
    Point pt(x,y);
    ++x;
    ++y;
    return pt;
}
const Point& Point::operator--()
{
    --x;--y;
    return *this;
}
const Point Point::operator--(int)
{
    Point temp = *this;
    --x;--y;
    return temp;
}
const bool Point::operator!()
{
    if((x == 0) && (y == 0)) return true;
    return false;
}
const Point& Point::operator*()
{
    return *this;
}

int Ch01::Section03(void)
{
    Point p1(2,3), p2(2,3), p3(0,0);
    Point result;

    cout << "p1 : "; p1.print();
    result = ++p1;
    cout << "result : "; result.print();
    cout << "++p1 :"; p1.print();
    
    cout << "p2 : "; p2.print();
    result = p2++; // p2.operator++(0) 과 동일
    cout << "result : "; result.print();
    cout << "p2++ :"; p2.print();


    p3.print();
    if(!p3) cout << "return true" << endl;
    else cout << "return false" << endl;

    p3.print();
    (*p3).print();

    return 0;
}