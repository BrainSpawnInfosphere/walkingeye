function out=system(in)
% Modelling and assessing of omni-directional robots with 3 and 4 wheels
% intechopen.com
% sys2 = soccer2(1)
% pp=[-20-20i -20+20i -100];
% f=place(sys2,pp)
% sys3 = ss(sys2.a-sys2.b*f,sys2.b)

p = degToRad(45.0); % wheel angle
M = 5; % robot mass
d = in_to_mm(7.0/2.0)/1000.0; % radius robot
m = .5; % wheel+stator mass
r = in_to_mm(2.5/2.0)/1000.0; % wheel radius
Jw = m*r*r/2.0; % inertia wheel
J = M*d*d/2.0; % inertia robot
Kt = .5; % Motor torque const
R = 1.52; % Motor resistance
Bv = 1; % viscous coeff
Bvn = 1; % viscous coeff
Bw = 1; % viscous coeff
l = 5; % gearbox reduction


A11 = -(2*Kt^2*l^2)/(r^2*R*M)-Bv/M;
A22 = -(2*Kt^2*l^2)/(2*r^2*R*M)-Bvn/M;
A33 = -(4*d^2*Kt^2*l^2)/(r^2*R*J)-Bw/J;
A = diag([A11 A22 A33]);

B = (l*Kt)/(r*R)*[0 -1/M 0 1/M;
                  1/M 0 -1/M 0;
                   d/J d/J d/J d/J];


out=ss(A,B);

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function out=degToRad(in)
out = in*pi/180;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function out=in_to_mm(in)
out = 25.4*in;
end

