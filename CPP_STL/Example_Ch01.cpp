#include "./Example_function.h"

int Ch01::Ex01(void)
{
    int n1 = 10, n2 = 20;
    cout << n1 + n2 << endl; // 기본 연산자
    return 0;
}

class Point { };

int Ch01::Ex02(void)
{
    Point p1, p2;

    //p1 + p2; // Error! 이러한 피연산자와 일치하는 연산자 + 가 없습니다.

    return 0;
}