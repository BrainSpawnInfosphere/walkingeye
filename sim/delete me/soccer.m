function out=system(in)

p = radToDeg(45.0); % wheel angle
M = 5; % robot mass
R = in_to_mm(7.0/2.0)/1000.0; % radius robot
m = .5; % wheel+stator mass
r = in_to_mm(2.5/2.0)/1000.0; % wheel radius
Jw = m*r*r/2.0; % inertia wheel
Jr = M*R*R/2.0; % inertia robot
a = .5; % wheel viscous friction factor
k = .5; % driving gain of motor

e = eye(3);

one = [sin(p)  0  0;
	   0 cos(p) 0;
	   0 0 1];

gamma = [-1 -1 1 1;
		  1 -1 -1 1;
		  1 1 1 1];

beta = [1/M 0 0;
		0 1/M 0;
		0 0 1/Jr];


M = e + Jw/(r*r)*beta*one*one;

B = k/r*beta*one*gamma;

A = a/(r*r)*beta*one*one;

out=ss(inv(M)*A,inv(M)*B);

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function out=radToDeg(in)
out = in*180/pi;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function out=in_to_mm(in)
out = 25.4*in;
end

