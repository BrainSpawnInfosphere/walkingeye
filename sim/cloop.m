function [sys2,f]=cloop(sys,poles)

f=place(sys,poles);
sys2 = ss(sys.a-sys.b*f,sys.b);