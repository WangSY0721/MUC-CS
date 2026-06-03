function main()
    G=[0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0;
       0 1 1 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0;
       0 1 1 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0;
       0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0;
       0 0 0 0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0;
       0 1 1 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0;
       0 1 1 1 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0;
       0 1 1 1 0 0 1 1 1 0 1 1 1 1 0 0 0 0 0 0;
       0 1 1 1 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0;
       0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0 0 0 0 0;
       0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0;
       0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0;
       0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 1 0;
       0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 1 0;
       1 1 1 1 0 0 0 0 0 0 0 1 1 1 0 1 1 1 1 0;
       1 1 1 1 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0;
       0 0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 1 1 0;
       0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 1 1 0;
       0 0 0 0 0 0 0 0 0 0 1 1 0 0 1 0 0 0 0 0;
       0 0 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0];
    MM=size(G, 1);                                             % G  地形图为 01 矩阵，如果为 1 表示障碍物
    Tau=ones(MM*MM,MM*MM); Tau=8.*Tau;	% Tau  初始信息素矩阵
    K=100;	%迭代次数（指蚂蚁出动多少波）
    M=50;	%蚂蚁个数
    S= 1 ;	%最短路径的起始点
    E=MM*MM;	%最短路径的目的点
    Alpha=1;	% Alpha  表征信息素重要程度的参数
    Beta=7;	% Beta  表征启发式因子重要程度的参数
    Rho=0.3 ;	% Rho  信息素蒸发系数
    Q=1;	% Q  信息素增加强度系数
    minkl=inf;	%minkl 表示当前最短路径长度
    mink=0;	%当前完成最短路径为第几次迭代
    minl=0;	%当前完成最短路径为第只蚂蚁
    D=G2D(G);	%每个栅格至各自邻域无障碍栅格的代价值
    N=size(D, 1);	%N 表示问题的规模（象素个数）
    a=1;	%小方格象素的边长
    Ex=a*(mod(E,MM)-0.5);	%目的点横坐标
    if Ex==-0.5	
        Ex=MM-0.5;	
    end	
    Ey=a*(MM+0.5-ceil(E/MM)); %目的点纵坐标
    Eta=zeros(N);                          %启发式信息矩阵，记录启发式信息
    %以下开始建立启发式信息矩阵
    for i= 1:N                                    %每个栅格的索引号，一共 N 个栅格
        ix=a*(mod(i,MM)-0.5);              %矩阵中各点的横坐标
        if ix==-0.5
            ix=MM-0.5; 
        end
        iy=a*(MM+0.5-ceil(i/MM));        %矩阵中各点的纵坐标
        if i~=E
            Eta(i)=1/((ix-Ex)^2+(iy-Ey)^2)^0.5; %启发信息取为至目标点的直线距离的倒数
        else
            Eta(i)=100; 
        end
    end

    ROUTES=cell(K,M);          %用细胞结构存储第 K 次迭代中的第 M 只蚂蚁的爬行路线 
    PL=zeros(K,M);                  %用矩阵存储第 K 次迭代中的第 M 只蚂蚁爬行路线的长度 %开始 K 次迭代，每轮派出 M 只蚂蚁，开始寻找路径
    tic;
    for k= 1:K                               %第 K 次迭代
        for m= 1:M                               %第 M 只蚂蚁
            %状态初始化
            W=S;                                    %将当前节点初始化为起始点
            Path=S;                                %爬行路线初始化
            PLkm=0;                              %爬行路线长度初始化
            TABUkm=ones(N);              %禁忌表初始化为 1，禁忌表记录走过的位置，将走过的位置由 1变 0
            TABUkm(S)=0;                    %将禁忌表起点位置置为 0
            DD=D;                                  %邻栅格点初始化 
            %下一步可以前往的栅格点
            DW=DD(W,:);    %取 G2D 矩阵中以当前点为局部起始点的一行
            DW1=find(DW); %DW1 矩阵存储该行中所有无障碍相邻栅格点（元素不为 0）的索引位置 
            for j=1:length(DW1)
                if TABUkm(DW1(j))==0 %判断 TABUkm 禁忌表中，该位置是否为之前走过的点 
                    DW(DW1(j))=0;    %删除 DW 中所有之前已经走过的相邻栅格点
                end
            end 
            %现在 DW 中为当前栅格点可以选择的所有相邻栅格点了
            %  计算各可选择邻节点的选择概率
            LJD=find(DW); %LJD 记录未走过的点的索引号，即下一步可选的点 
            Len_LJD=length(LJD);%可选点的个数
            %蚂蚁未遇到食物或者陷入死胡同或者觅食停止
            while W~=E&&Len_LJD>= 1 %起始点不等于终止点，且可选节点个数大于等于 1 
                %转轮赌法选择下一步怎么走
                PP=zeros(Len_LJD); 
                for i= 1:Len_LJD
                    PP(i)=(Tau(W,LJD(i))^Alpha)*((Eta(LJD(i)))^Beta); 
                end
                sumpp=sum(PP);
                PP=PP/sumpp;%蚂蚁从当前栅格点转移到各相邻栅格点的概率 
                Pcum(1)=PP(1);
                %轮盘赌选择下一栅格点
                for i=2:Len_LJD
                    Pcum(i)=Pcum(i-1)+PP(i);
                end
                Select=find(Pcum>=rand);
                %选择积累概率比随机数大的第一个可选择点作为行走的下一步，并取该点的索引号 
                to_visit=LJD(Select(1));
                %状态更新和记录
                Path=[Path,to_visit];         %路径增加
                PLkm=PLkm+DD(W,to_visit);     %路径长度增加
                W=to_visit;                   %蚂蚁移到下一个点
                %对应禁忌表更新 D 中可选择的相邻栅格点 
                for kk= 1:N
                    if TABUkm(kk)==0 
                        DD(W,kk)=0;
                        DD(kk,W)=0; 
                    end
                end
                TABUkm(W)=0;            
                %更新禁忌表
                DW=DD(W,:);
                DW1=find(DW);
                for j=1:length(DW1)
                    if TABUkm(DW1(j))==0 
                        DW(j)=0;
                    end
                end
                LJD=find(DW);
                Len_LJD=length(LJD);%可选节点的个数 
            end 
            %本次迭代的当前蚂蚁寻路完毕
            %记下每一代每一只蚂蚁的觅食路线和路线长度
            ROUTES{k,m}=Path; %记录本次迭代中的当前蚂蚁的行走路线
            if Path(end)==E %判断本只蚂蚁寻找路径的最后一个节点是否为终点
                PL(k,m)=PLkm; %若该蚂蚁到达终点，将本次路线长度放到 PL 的第 k 行 m 列 
                if PLkm<minkl %若本次路径长度< 当前已知的最短路径长度
                    mink=k; %记录完成本次最短路径的迭代次数 
                    minl=m; %记录完成本次最短路程的哪只蚂蚁
                    minkl=PLkm; %记录本次最短路线的长度
                end
            else
                PL(k,m)=0; %若该蚂蚁没有到达终点长，则本次路径长度为 0 
            end
        end 
        %返回进行下一只蚂蚁的寻路 
        %更新信息素
        Delta_Tau=zeros(N,N);%初始化信息素增量
        for m= 1:M    
            if PL(k,m)
                ROUT=ROUTES{k,m}; %ROUT 取本次迭代的所有蚂蚁的行走路线 
                TS=length(ROUT)-1;
                PL_km=PL(k,m); %PL_km 取本次迭代当前蚂蚁的路径长度
                for s=1:TS
                    x=ROUT(s);     
                    y=ROUT(s+1);
                    Delta_Tau(x,y)=Delta_Tau(x,y)+Q/PL_km;
                    Delta_Tau(y,x)=Delta_Tau(y,x)+Q/PL_km;
                end
            end
        end
        Tau=(1-Rho).*Tau+Delta_Tau;%信息素挥发一部分，新增加一部分 
    end
    %绘图
    plotif= 1;%是否绘图的控制参数
    if plotif==1 
        %绘收敛曲线 
        minPL=zeros(K);
        for i= 1:K %选出每次迭代的最短路径
            PLK=PL(i,:); %取第 i 次迭代的所有路径长度
            Nonzero=find(PLK); %提取本次迭代路径长度不为 0 的索引号存储至 Nonzero PLK
            PLK=PLK(Nonzero);
            minPL(i)=min(PLK); %选出本次迭代最短路径存储至 minPL 的相应迭代位置 
        end
        %绘制“收敛曲线变化趋势”图，将每次迭代的最短路径放在图中表示
        figure(1)
        plot(minPL); 
        hold on
        grid on
        title('收敛曲线变化趋势'); 
        xlabel('迭代次数');
        ylabel('最小路径长度');
        %绘爬行图 
        figure(2)
        axis([0,MM,0,MM]) %设置图的横纵坐标，MM 为地图矩阵的行数或列数
        for i= 1:MM 
            for j=1:MM
                if G(i,j)==1 %1 是黑色代表障碍，0 为白色无障碍 
                    x1=j-1;y1=MM-i;
                    x2=j;y2=MM-i;
                    x3=j;y3=MM-i+1;    
                    x4=j-1;y4=MM-i+1;
                    fill([x1,x2,x3,x4],[y1,y2,y3,y4],[0.2,0.2,0.2]); %将 1234 点所围成的图形进行黑色填充 
                    hold on
                else
                    x1=j-1;y1=MM-i;
                    x2=j;y2=MM-i;
                    x3=j;y3=MM-i+1;    
                    x4=j-1;y4=MM-i+1;
                    fill([x1,x2,x3,x4],[y1,y2,y3,y4],[1, 1, 1]); %将 1234 点所围成的图形进行白色填充 
                    hold on
                    set(gca,'YTickLabel',[20 18 16 14 12 10 8 6 4 2 0]); %使得地图矩阵的行列与正常坐标轴的行列一致 
                end
            end
        end
        hold on
        title('机器人运动轨迹'); 
        xlabel('坐标 x');
        ylabel('坐标 y');
        ROUT=ROUTES{mink,minl};
        %ROUT 取最短行走路线，mink 为该路线的迭代号,minl 为该路线的蚂蚁号 
        LENROUT=length(ROUT);
        %Rx 与 Ry 中分别存储具体的该路线
        Rx=ROUT; 
        Ry=ROUT;
        %将该路线的栅格索引号转换为横纵坐标 
        for ii= 1:LENROUT
            Rx(ii)=a*(mod(ROUT(ii),MM)-0.5); 
            if Rx(ii)==-0.5
                Rx(ii)=MM-0.5; 
            end
            Ry(ii)=a*(MM+0.5-ceil(ROUT(ii)/MM)); 
        end
        plot(Rx,Ry) %绘各代蚂蚁爬行图 
    end
end

function D=G2D(G)      %相邻栅格点初始化 
    l=size(G, 1);          %l=G 矩阵的行数
    %D 是所有点到所有点的矩阵。纵向将所有点作为起点，横向将所有点作为邻域局部到达点 
    D=zeros(l*l,l*l);
    for i= 1:l
        for j=1:l
            if G(i,j)==0 %判断局部起始栅格是否有障碍
                for m= 1:l
                    for n=1:l
                        if G(m,n)==0 %判断局部终点栅格，即相邻栅格是否有障碍 
                            im=abs(i-m);
                            jn=abs(j-n);
                            if im+jn==1||(im==1&&jn==1) %判断该栅格是否为当前栅格的邻域栅格
                                D((i-1)*l+j,(m-1)*l+n)=(im+jn)^0.5; %将所有点到所有邻域点的代价值填入 D 中
                                %D((i-1)*l+j,(m-1)*l+n)在矩阵中定位邻域矩阵的具体位置
                                %(im+jn)^0.5 在具体位置中填入具体代价 值
                            end
                        end
                    end
                end
            end
        end
    end
end
