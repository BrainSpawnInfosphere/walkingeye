function plotstep(sys)
% step() plots out per input each input, this combines (sum)
% the outputs into the 3 states.
%
[y,t] = step(sys);
for i=1:length(y)
    for j=1:3
        yy(i,j) = sum(y(i,j,:)); 
    endfor 
endfor

figure(1);
for i=1:3
    subplot(3,1,i);plot(t,yy(:,i)); grid on;
    if(i==1) ylabel('\dot x'); endif;
    if(i==2) ylabel('\dot y'); endif;
    if(i==3) ylabel('\psi'); xlabel('time (sec)');endif;
endfor