function [tBSeuCallUI,rBSeuCallUI] = problem1_A1()

format long

% addpath(genpath('./')); %adds all the functions from subfolders to the path
% mfiles=getfilenames('./','BSeuCallU*.m')

warning off

Methods={'MC','MC-S','QMC-S','MLMC','MLMC-A',...
    'FFT','FGL','COS',...
    'FD','FD-NU','FD-AD',...
    'RBF','RBF-FD','RBF-PUM','RBF-LSML','RBF-AD','RBF-MLT'};

%% Problem 1 a) I

display('Problem 1 a) I');
rootpath=pwd;
S=[90,100,110]; K=100; T=1.0; r=0.03; sig=0.15;
U=[2.758443856146076 7.485087593912603 14.702019669720769];

filepathsBSeuCallUI=getfilenames('./','BSeuCallUI_*.m');
par={S,K,T,r,sig};
[timeBSeuCallUI,relerrBSeuCallUI] = executor(rootpath,filepathsBSeuCallUI,U,par)

tBSeuCallUI=NaN(numel(Methods),1); rBSeuCallUI=tBSeuCallUI;
for ii=1:numel(Methods)
    for jj=1:numel(filepathsBSeuCallUI)
        a=filepathsBSeuCallUI{jj}(3:3+numel(Methods{ii}));
        b=[Methods{ii},'/'];
        if strcmp(a,b)
            tBSeuCallUI(ii)=timeBSeuCallUI(jj);
            rBSeuCallUI(ii)=relerrBSeuCallUI(jj);
        end
    end
end

cd(rootpath);
