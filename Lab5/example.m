a = 0;
b = 1;
while (b < 1000) {
    print b;
    b += a;
    a = b - a;
}

pi = 0.0;
n = 1;
for i = 1:100000 {
    pi += 4.0 / n - 4.0 / (n + 2);
    n += 4;
}
print pi;

for n = 2:100 {
    p = 1;
    for d = 2:(n-1) {
        nc = n;
        while (nc > 0) nc -= d;
        if (nc == 0) {
            p = 0;
            break;
        }
    }
    if (p == 1) {
        print n;
    }
}

for x = 1:9 {
    sqrt_x = 1.0;
    for i = 1:10000 sqrt_x = (sqrt_x + x / sqrt_x) / 2;
    print x, sqrt_x;
}

n = 10;
for i = 1:n print "*" * i;

A = eye(3);
B = ones(3);
C = A .+ B;
print C;

D = zeros(3, 4);
D[0, 0] = 42;
D[1:2, 1:2] = 7;
print D;
print D[2, 2];