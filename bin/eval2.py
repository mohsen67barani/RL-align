#! /usr/bin/python3

import sys
import os
import re

ALL_X3=0
FIT_X3=1
ALL_M3=2
FIT_M3=3
ALL_M0=4
FIT_M0=5

prefix=[0,0,0,0,0,0]
prefix[ALL_X3]="gAllX3"
prefix[FIT_X3]="gFitX3"
prefix[ALL_M3]="gAllM3"
prefix[FIT_M3]="gFitM3"
prefix[ALL_M0]="gAllM0"
prefix[FIT_M0]="gFitM0"

# -------------------------------
# print stats

def stats(name,where,Tok,Ttot,Etot,EokLM,EokL,Epred,Eexp,Icost,SGcost,SRcost,SGfit,SRfit,TimeTot) :
   print (name)
   ALL=where
   FITTING=where+1
   print ("With reference solution")
   F = 100.0*Ttot[FITTING]/Ttot[ALL] if Ttot[ALL]>0 else 0
   print ("   Fitting: {:.2f}% ({}/{})".format(F,Ttot[FITTING],Ttot[ALL]))   
   for k in [FITTING,ALL] :
      if Ttot[k]==0 : continue
      N = prefix[k]
      A = 100.0*(EokLM[k]+EokL[k])/Etot[k]
      print ("   {}_Acc: {:.2f}% (({}+{})/{})".format(N,A,EokLM[k],EokL[k],Etot[k]))
      P = 100.0*EokLM[k]/Epred[k]
      print ("   {}_P: {:.2f}% ({}/{})".format(N,P,EokLM[k],Epred[k]))
      R = 100.0*EokLM[k]/Eexp[k]
      print ("   {}_R: {:.2f}% ({}/{})".format(N,R,EokLM[k],Eexp[k]))
      print ("   {}_F1: {:.2f}%".format(N,2*P*R/(P+R) if P+R>0 else 0))
      W = 100.0*Tok[k]/Ttot[k]
      print ("   {}_Identical: {:.2f}% ({}/{})".format(N,W,Tok[k],Ttot[k]))
      C = 100.0*Icost[k]/Ttot[k]
      print ("   {}_SameCost: {:.2f}% ({}/{})".format(N,C,Icost[k],Ttot[k]))
      DR = 1.0*SRcost[k]/Ttot[k]
      print ("   {}_AvgCostSol: {:.2f} ({}/{})".format(N,DR,SRcost[k],Ttot[k]))
      DG = 1.0*SGcost[k]/Ttot[k]
      print ("   {}_AvgCostRef: {:.2f} ({}/{})".format(N,DG,SGcost[k],Ttot[k]))
      DF = 1.0*(SRcost[k]-SGcost[k])/Ttot[k]
      print ("   {}_AvgCostDiff: {:.2f} ({}/{})".format(N,DF,SRcost[k]-SGcost[k],Ttot[k]))
      FR = 1.0*SRfit[k]/Ttot[k]
      print ("   {}_AvgFitSol: {:.2f} ({:.2f}/{})".format(N,FR,SRfit[k],Ttot[k]))
      FG = 1.0*SGfit[k]/Ttot[k]
      print ("   {}_AvgFitRef: {:.2f} ({:.2f}/{})".format(N,FG,SGfit[k],Ttot[k]))
      FF = 1.0*(SRfit[k]-SGfit[k])/Ttot[k]
      print ("   {}_AvgFitDiff: {:.2f} ({:.2f}/{})".format(N,FF,SRfit[k]-SGfit[k],Ttot[k]))
      TT = 1.0*TimeTot[k]/Ttot[k]
      print ("   {}_AvgTraceTime: {:.6} ({:.1f}/{})".format(N,TT,1.0*TimeTot[k],Ttot[k]))
      print ("   {}_TotalTime: {:.1f} ({} traces)".format(N,1.0*TimeTot[k],Ttot[k]))


# -------------------------------

def separate(s) :
   x = s.rfind("]")
   m = s[0:x+1]  # event mark (L,L/M) in output 
   t = s[x+1:] # task name in output
   return m,t


def fitness(alig) :
   nsync = alig.count("[L/M]")
   nlog =  alig.count("[L]")
   nmod =  alig.count("[M-REAL]")
   return 1.0*nsync/(nsync+nlog+nmod)

def cost(alig) :
   nlog =  alig.count("[L]")
   nmod =  alig.count("[M-REAL]")
   return nlog+nmod


def update_1(mout,mgold,where) :
   global Etotf, EokLMf, EokLf, Epredf, Eexpf
   Etotf[where] += 1
   if mout=="[L/M]" and mgold=="[L/M]" : EokLMf[where] += 1
   if mout=="[L]" and mgold=="[L]" : EokLf[where] += 1
   if mout=="[L/M]" : Epredf[where] += 1
   if mgold=="[L/M]" : Eexpf[where] += 1
   

def update_counts_1(where, mout, mgold, fitting) :
   if where == ALL_X3 or where == ALL_M3:
      update_1(mout,mgold,ALL_X3)
      if fitting : update_1(mout,mgold,FIT_X3)
      if where == ALL_M3 :  
         update_1(mout,mgold,ALL_M3)
         if fitting : update_1(mout,mgold,FIT_M3)

   elif where == ALL_M0 :
      update_1(mout,mgold,ALL_M0)
      if fitting : update_1(mout,mgold,FIT_M0)


def update_2(aligout,aliggold,costout,costgold,fitout,fitgold,time,where) :
   global Ttotf, Tokf, Icostf, SRcostf, SGcostf, SRfitf, SGfitf,TimeTotf
   
   Ttotf[where] += 1
   if aligout==aliggold : Tokf[where] += 1
   if costout==costgold : Icostf[where] += 1
   SRcostf[where] += costout
   SGcostf[where] += costgold
   SRfitf[where] += fitout
   SGfitf[where] += fitgold
   TimeTotf[where] += time

def update_counts_2(where,aligout,aliggold,costout,costgold,fitout,fitgold,time,fitting) :

   if where == ALL_X3 or where == ALL_M3:
      update_2(aligout,aliggold,costout,costgold,fitout,fitgold,time,ALL_X3)
      if fitting : update_2(aligout,aliggold,costout,costgold,fitout,fitgold,time,FIT_X3)
      if where == ALL_M3 :  
         update_2(aligout,aliggold,costout,costgold,fitout,fitgold,time,ALL_M3)
         if fitting : update_2(aligout,aliggold,costout,costgold,fitout,fitgold,time,FIT_M3)

   elif where == ALL_M0 :
      update_2(aligout,aliggold,costout,costgold,fitout,fitgold,time,ALL_M0)
      if fitting : update_2(aligout,aliggold,costout,costgold,fitout,fitgold,time,FIT_M0)

      

# -------------------------------
# MAIN program

if len(sys.argv)<3 :
   print('Usage: ',sys.argv[0],"golddir outdir")
   exit()
   
golddir = sys.argv[1]
outdir = sys.argv[2]

Tok = [0,0,0,0,0,0]  # Traces ok (as a whole) in total, and only fitting
Ttot = [0,0,0,0,0,0] # Traces in total, and only fitting
Etot = [0,0,0,0,0,0] # Events in total, and only fitting
EokLM = [0,0,0,0,0,0] # Events ok (LM in output and gold) in total, and only fitting
EokL = [0,0,0,0,0,0] # Events ok (L in output and gold) in total, and only fitting
Epred = [0,0,0,0,0,0] # events predicted (LM or L in output) in total, and only fitting
Eexp = [0,0,0,0,0,0] # events expected (LM in gold) in total, and only fitting
Icost = [0,0,0,0,0,0] # traces with identical cost in total, and only fitting
SGcost = [0,0,0,0,0,0] # sum of costs for gold 
SRcost = [0,0,0,0,0,0] # sum of costs for result
SGfit = [0,0,0,0,0,0] # sum of fitness for result
SRfit = [0,0,0,0,0,0] # sum of fitness for result
TimeTot = [0,0,0,0,0,0] # time used in total

for f in sorted(os.listdir(outdir)) :

   if re.search("M.*\.[0-2]",f) :
      where = ALL_M0
   elif re.search("M.*\.3",f) and not re.search("ML5\.3",f) :
      where = ALL_M3 # (and X3 also)
   else :   
      where = ALL_X3

   error = False

   Tokf = [0,0,0,0,0,0] # Traces ok (as a whole) in current file: all / only fitting
   Ttotf = [0,0,0,0,0,0] # Traces in total in current file: all / only fitting
   Etotf = [0,0,0,0,0,0] # Events in total in current file: all / only fitting
   EokLMf = [0,0,0,0,0,0] # Events ok (LM in output and gold) in current file: all / only fitting
   EokLf = [0,0,0,0,0,0] # Events ok (L in output and gold) in current file: all / only fitting
   Epredf = [0,0,0,0,0,0] # events predicted (LM or L in output) in current file: all / only fitting
   Eexpf = [0,0,0,0,0,0] # events expected (LM in gold) in current file: all / only fitting
   Icostf = [0,0,0,0,0,0] # traces with identical cost in current file: all / only fitting
   SGcostf = [0,0,0,0,0,0] # sum of cost for gold in current file: all / only fitting
   SRcostf = [0,0,0,0,0,0] # sum of cost for result in current file: all / only fitting
   SGfitf = [0,0,0,0,0,0] # sum of fitness for result in current file
   SRfitf = [0,0,0,0,0,0] # sum of fitness for result in current file
   TimeTotf = [0,0,0,0,0,0] # time used in this file
    
   fname = re.sub("\.[0-3]\.out",".gold",f)
   print ("------------------------------------------")

   try :
      fout = open(outdir+"/"+f)
      fgold = open(golddir+"/"+fname)
   except:
      continue

   lout = fout.readline()
   lgold = fgold.readline()   
   while lout!='' and lgold!='' :
      (idout,aligout,fitout,time) = lout.split()
      time = float(time)
      fitting = (fitout=="FITTING")
      (idgold,aliggold) = lgold.split()

      if idgold < idout :
         # unsolved case, skip gold. (Should not happen, since we always produce an output)
         print(f,"- UNSOLVED instance", idgold)
         # next
         lgold = fgold.readline()
         
      elif idout < idgold :
         # no gold solution for this trace. Just ignore it.
         lout = fout.readline()
         
      else :
         # IDs match, compare traces
         
         evout = aligout.split("|")   # events in output
         evgold = aliggold.split("|") # events in gold
         acevout = len(evout) - aligout.count("[M-REAL]"); # actual events (i.e. not inserted) in output
         acevgold = len(evgold) - aliggold.count("[M-REAL]"); # actual events (i.e. not inserted) in gold
         if acevout!=acevgold :
            print(f,"- Length mismatch",idout,idgold,"\n", aligout,"\n", aliggold)
            error = True
            break

         iout = 0
         igold = 0
         while iout<len(evout) and igold<len(evgold) :
            ## advance iout skipping insertions
            while iout<len(evout) and evout[iout].count("[M-REAL]")>0 : iout += 1
            if iout==len(evout) : (mout,tout)==("EOT","EOT")
            else : (mout,tout) = separate(evout[iout])

            ## advance igold skipping insertions
            while igold<len(evgold) and evgold[igold].count("[M-REAL]")>0 : igold += 1
            if igold==len(evgold) : (mgold,tgold)==("EOT","EOT")
            else : (mgold,tgold) = separate(evgold[igold])

            if tout!=tgold :
               print(f,"- Task mismatch",idout,idgold,"\n", tout,"\n", tgold)
               error = True
               break
            
            update_counts_1(where, mout, mgold, fitting)

            iout += 1
            igold += 1
         # end while on events
         
         if not error :
            costout = cost(aligout)
            costgold = cost(aliggold)
            fitout = fitness(aligout)
            fitgold = fitness(aliggold)
            
            update_counts_2(where, aligout, aliggold, costout, costgold, fitout, fitgold, time, fitting)

         lout = fout.readline()
         lgold = fgold.readline()   

      # end case ids match

   #end for each trace
         
   if not error :
      stats (f,where,Tokf,Ttotf,Etotf,EokLMf,EokLf,Epredf,Eexpf,Icostf,SGcostf,SRcostf,SGfitf,SRfitf,TimeTotf)      

      for k in [ALL_X3,FIT_X3,ALL_M3,FIT_M3,ALL_M0,FIT_M0] :
         Tok[k] += Tokf[k]
         Ttot[k] += Ttotf[k]
         EokLM[k] += EokLMf[k]
         EokL[k] += EokLf[k]
         Epred[k] += Epredf[k]
         Eexp[k] += Eexpf[k]
         Etot[k] += Etotf[k]
         Icost[k] += Icostf[k]
         SRcost[k] += SRcostf[k]
         SGcost[k] += SGcostf[k]
         SRfit[k] += SRfitf[k]
         SGfit[k] += SGfitf[k]
         TimeTot[k] += TimeTotf[k]


# end for each file
    
print ("...........................................")
stats ("TOTAL-X3",ALL_X3,Tok,Ttot,Etot,EokLM,EokL,Epred,Eexp,Icost,SGcost,SRcost,SGfit,SRfit,TimeTot)
print ("...........................................")
stats ("TOTAL-M3",ALL_M3,Tok,Ttot,Etot,EokLM,EokL,Epred,Eexp,Icost,SGcost,SRcost,SGfit,SRfit,TimeTot)
print ("...........................................")
stats ("TOTAL-M0",ALL_M0,Tok,Ttot,Etot,EokLM,EokL,Epred,Eexp,Icost,SGcost,SRcost,SGfit,SRfit,TimeTot)

