#! /bin/bash

DATE=`date +%Y-%m-%d`
#DATE=$1

for cross in -50 -100 -150 -200 -300 -400 -500; do
   for excl in -20 -40 ; do
      for dummy in -20 -40; do
		for order in 5 15 15 25 40 50 60 ; do
            		for paral in 5 15 25 15 25 40 50 60 ; do
                 cat config/config-base \
                        | sed 's/DummyCompatibility/DummyCompatibility '$dummy'/' \
                        | sed 's/ExclusiveCompatibility/ExclusiveCompatibility '$excl'/' \
                        | sed 's/CrossCompatibility/CrossCompatibility '$cross'/' \
                        | sed 's/OrderCompatibility/OrderCompatibility '$order'/' \
                        | sed 's/ParallelCompatibility/ParallelCompatibility '$paral'/' \
                        > config/config.$order.$paral.$cross.$dummy.$excl.cfg
                    
			./bin/align ./data/unfoldings/prCm6 ./data/logs/prCm6.xes ./config/config.$order.$paral.$cross.$dummy.$excl.cfg > $order.$paral.$cross.$dummy.$excl
                 #bin/eval2.py data/alignments data/results/output-train.$order.$paral.$cross.$dummy.$excl >> data/results/train/stats.$DATE.$cross.$dummy.$excl
                 rm -rf data/results/output-train.$order.$paral.$cross.$dummy.$excl
                 rm -rf config/config.$order.$paral.$cross.$dummy.$excl.cfg
            done
         done
	  
	  
	  #sbatch -p medium --mem=8G -o /home/usuaris/padro/BPM/std/out.$DATE.$dummy.$excl.$cross -e /home/usuaris/padro/BPM/std/err.$DATE.$dummy.$excl.$cross /home/usuaris/padro/BPM/experiments-BPIC.sh $DATE $dummy $excl $cross
      done
   done
done


#/home/usuaris/bmohsen/ /home/usuaris/bmohsen/algorithm/RL-align 

#/home/mohsen/testcode/RL-align

#-100 -150 -200 -300 -400 -500
#-40 -60 -100 -150 -200 -300 -400
#-40 -60 -100 -150 -200 -300 -400
#echo "sbatch -p medium --mem=8G -c 4 -o /home/usuaris/bmohsen/algorithm/RL-align/std/out.$DATE.$dummy.$excl.$cross -e /home/usuaris/bmohsen/algorithm/RL-align/std/err.$DATE.$dummy.$excl.$cross /home/usuaris/bmohsen/algorithm/RL-align/experiments.sh $DATE $dummy $excl $cross"
	      
