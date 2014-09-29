clear all;

p = 45*pi/180;

% deterine controllability
A = [zeros(3) eye(3);
     zeros(3) zeros(3)];

B = [zeros(3,4);
     -sin(p) -sin(p) sin(p) sin(p);
     cos(p) -cos(p) -cos(p) cos(p);
     2 2 2 2];
     
R = [B A*B A^2*B A^3*B A^4*B A^5*B];

rank(R)

% Determine observability
% X = [x y rtheta vx vy romega]
% can measure theta and omega
% need KF for others
%C = eye(6);
C = [0 0 1 0 0 0;  % compass
     %0 0 0 1 0 0;  % integrate ax
     %0 0 0 0 1 0;  % integrate ay
     0 0 0 0 0 1]; % gyro
     
O = [C; C*A; C*A^2; C*A^3; C*A^4; C*A^5];

rank(O)