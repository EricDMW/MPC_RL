function x0=SolverOfThreeOrderFunction(a,b,c,d,K)
if d>=1.2179*K
    x0=1.2;
elseif d==0
    x0=0;
else
x1 = 0;
x2 = 1.2;

fx1 = ((a * x1 + b) * x1 + c) * x1 + d;
fx2 = ((a * x2 + b) * x2 + c) * x2 + d;

flag2=1;
while flag2
    x0=(x1+x2)/2;
    fx0=((a*x0+b)*x0+c)*x0+d;
    
    if fx0*fx1 < 0
        x2 = x0;
        fx2 = fx0;
    else 
        x1 = x0;
        fx1 = fx0;
    end
    if abs(fx0) < 1e-2
        flag2=0;
    end
end
end
% x0=(-1*c-sqrt(c*c-4*b*d))/(4*b);
end