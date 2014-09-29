% motors(phi, angles)
% phi = motor angle in degrees
% angles = 0 ... 2pi
function out=motors(phi,angles)

phi = phi*pi/180;

for i=1:length(angles)
	b = angles(i);
	v =  [-sin(phi)  cos(phi) 1;
				   -sin(phi) -cos(phi) 1;
	                sin(phi) -cos(phi) 1;
	                sin(phi)  cos(phi) 1] * [cos(b);sin(b);0];
	                
	em(i) = sum(abs(v));
end

out = em;