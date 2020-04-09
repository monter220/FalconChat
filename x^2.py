from math import *


a = int(input('a:'))
b = int(input('b:'))
c = int(input('c:'))

print('Уравнение имеет вид', a, 'x^2+', b, 'x+', c)

def _sqad(q, w, s):
    d: int = w**2-4*q*s
    print('Descriminant=', d)
    if d < 0:
        print('нет действительных корней')
    elif d > 0:
        x1 = (-w+d**1/2)/(2*q)
        x2 = (-w-d**1/2)/(2*q)
        print('x1 = ', x1, '\nx2 =', x2)
    else:
        x = -w/(2*q)
        print('x =', x)

_sqad(a,b,c)