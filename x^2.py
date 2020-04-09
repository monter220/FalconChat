a = int(input('a:'))
b = int(input('b:'))
c = int(input('c:'))

print('Уравнение имеет вид', a, 'x^2+', b, 'x+', c)

d: int = b**2-4*a*c
if d < 0:
    print('нет действительных корней')
elif d > 0:
    x1 = (-b+d**1/2)/(2*a)
    x2 = (-b-d**1/2)/(2*a)
    print('x1 = ', x1, '\nx2 =', x2)
else:
    x = -b/(2*a)
    print('x =', x)