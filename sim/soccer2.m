function out=system(in)

% sys2 = soccer2(1)
% pp=[-200-200i -200+200i -575];
% f=place(sys2,pp)
% sys3 = ss(sys2.a-sys2.b*f,sys2.b)
% for i=1:length(y), for j=1:3, yy(i,j) = sum(y(i,j,:)); endfor endfor
% for i=1:3, subplot(3,1,i);plot(t,yy(:,i));endfor

p = degToRad(45.0); % wheel angle
M = 5; % robot mass
R = in_to_mm(7.0/2.0)/1000.0; % radius robot
m = .5; % wheel+stator mass
r = in_to_mm(2.5/2.0)/1000.0; % wheel radius
Jw = m*r*r/2.0; % inertia wheel
Jr = M*R*R/2.0; % inertia robot
a = .5; % wheel viscous friction factor
k = .5; % driving gain of motor

e = eye(3);


beta = [1/M 0 0;
		0 1/M 0;
		0 0 1/Jr];

C = [-1  1 1;
     -1 -1 1;
      1 -1 1;
      1  1 1]*diag([sin(p) cos(p) R]);

% [-1 -1  1 1; 1 -1 -1 1; 1  1  1 1];
D = diag([sin(p) cos(p) R])*[-1 -1  1 1;
      1 -1 -1 1;
      1  1  1 1];

Mass = e + Jw/(r*r)*beta*D*C

B = k/r*beta*D;

A = -a/(r*r)*beta*D*C;

out=ss(inv(Mass)*A,inv(Mass)*B);

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function out=degToRad(in)
out = in*pi/180;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function out=in_to_mm(in)
out = 25.4*in;
end

