% call graphics_toolkit("fltk")

clear all;

graphics_toolkit("fltk");

a = 0:.05:2*pi;

em30 = motors(30,a);
em45 = motors(45,a);
em60 = motors(60,a);

figure(1);
polar(a,em30,'r-');
hold on;
polar(a,em45,'g-');
polar(a,em60,'b-');
hold off;
grid on;
title('Number of Equivelent Motors');
legend('30','45','60');
print(1,'equiv_motors.png');
