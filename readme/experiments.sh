#! /bin/bash -l

# els tres primers bucles estan paralelitzats al qsub (veure submit.sh)
DATE=$1
dummy=$2
excl=$3
cross=$4

cd /home/mohsen/RL-align
rm -f data/results/train/stats.$DATE.$cross.$dummy.$excl

TRAIN="data/alignments/M*[13579].gold data/alignments/pr[ACEG]*.gold"
TEST="data/alignments/M*[02468].gold data/alignments/pr[BDF]*.gold"

#for cross in -50 -100 -150 -200 -300 -400 -500; do
#   for excl in -20 -40 -60 -80 -100 -120 -140 -160; do
#      for dummy in -20 -40 -60 -80 -100 -120 -140 -160; do
         for order in 5 15 15 25 40 50 60 ; do
            for paral in 5 15 25 15 25 40 50 60 ; do
                 cat config/config-base \
                        | sed 's/DummyCompatibility/DummyCompatibility '$dummy'/' \
                        | sed 's/ExclusiveCompatibility/ExclusiveCompatibility '$excl'/' \
                        | sed 's/CrossCompatibility/CrossCompatibility '$cross'/' \
                        | sed 's/OrderCompatibility/OrderCompatibility '$order'/' \
                        | sed 's/ParallelCompatibility/ParallelCompatibility '$paral'/' \
                        > config/config.$order.$paral.$cross.$dummy.$excl.cfg
                    
			./bin/align ./data/unfoldings/M8 ./data/logs/M8.xes ./config/config.$order.$paral.$cross.$dummy.$excl.cfg 
                 #bin/eval2.py data/alignments data/results/output-train.$order.$paral.$cross.$dummy.$excl >> data/results/train/stats.$DATE.$cross.$dummy.$excl
                 rm -rf data/results/output-train.$order.$paral.$cross.$dummy.$excl
                 rm -rf config/config.$order.$paral.$cross.$dummy.$excl.cfg
            done
         done
#      done
#   done
#done

#/home/usuaris/bmohsen/algorithm/RL-align
#15 25 40 50 60
#15 25 40 50 60
#bin/execute.sh config/config.$order.$paral.$cross.$dummy.$excl.cfg train "$TRAIN"
