%ÊÊÓ¦¶Èº¯Êý
function ITAE= PID_FUN( kp,ki,kd )
ts=0.01;
sys=tf(462,[0.78,27.2124,22.3608]);
dsys=c2d(sys,ts,'z');
[num,den]=tfdata(dsys,'v');
u_1=0.0;u_2=0.0;
y_1=0.0;y_2=0.0;
x=[0,0,0]';
error_1=0;
ITAE=0.0;
err=0.0;
SteadyState=0;
SteadyStateTime=0;
MaxITAE=350;
for k=1:1:1000
if ITAE>MaxITAE
break;
end
time(k)=k*ts;
rin(k)=1;
u(k)=kp*x(1)+kd*x(2)+ki*x(3);
yout(k)=-den(2)*y_1-den(3)*y_2+num(2)*u_1+num(3)*u_2;
error(k)=rin(k)-yout(k);
if error(k)<0
err=abs(error(k))*30;
else err=error(k);
end
if SteadyState==0
if yout(k)>0.95*rin(k)&&yout(k)<1.05*rin(k)
SteadyStateTime=k*ts;
SteadyState=1;
end
end
ITAE=ITAE+err*ts*k*0.1;
u_2=u_1;u_1=u(k);
y_2=y_1;y_1=yout(k);
x(1)=error(k);
x(2)=(error(k)-error_1)/ts;
x(3)=x(3)+error(k)*ts;
error_1=error(k);
end
if SteadyStateTime==0
ITAE=MaxITAE;
else
ITAE=ITAE+0.5*SteadyStateTime;
end
end