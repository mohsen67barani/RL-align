#! /bin/bash -l

# els tres primers bucles estan paralelitzats al qsub (veure submit.sh)
DATE=$1
dummy=$2
excl=$3
cross=$4
order=$5
paral=$6
ordert=$7
paralt=$8
orderparal=$9


cd /home/mohsen/RL-align


for cross in -50; do
   for excl in -20 ; do
      for dummy in -20 ; do
	for order in 5 ; do
            for paral in 5 ; do
		for ordert in 10; do
		   for paralt in 10; do 
			for orderparal in 10; do 
                 cat config/config-base \
                        | sed 's/DummyCompatibility -150/DummyCompatibility '$dummy'/' \
                        | sed 's/ExclusiveCompatibility -300/ExclusiveCompatibility '$excl'/' \
                        | sed 's/CrossCompatibility -100/CrossCompatibility '$cross'/' \
                        | sed 's/OrderCompatibility 50/OrderCompatibility '$order'/' \
                        | sed 's/ParallelCompatibility 10/ParallelCompatibility '$paral'/' \
			| sed 's/TorderCompatibility 100/ParallelCompatibility '$ordert'/' \
			| sed 's/TparallelCompatibility 30/ParallelCompatibility '$paralt'/' \
			| sed 's/OrderParallelCompatibility 50/ParallelCompatibility '$orderparal'/' \
                        > config/config.$dummy.$excl.$cross.$order.$paral.$ordert.$paralt.$orderparal.cfg
		for model in M1 M3 M5 M7 M9 ML1 ML3 ML5 prAm6 prCm6 prEm6 prGm6 M2 M4 M6 M8 M10 ML2 prBm6 prDm6 prFm6; do
		if [[ ! -d ''data/$model'' ]]; then 
		mkdir data/$model; 
		fi;

	 bin/align data/unfoldings/$model data/logs/$model.xes config/config.$dummy.$excl.$cross.$order.$paral.$ordert.$paralt.$orderparal.cfg >> ./data/$model/$model.$dummy.$excl.$cross.$order.$paral.$ordert.$paralt.$orderparal 
	
		
		done

	rm -rf config/config.$dummy.$excl.$cross.$order.$paral.$ordert.$paralt.$orderparal.cfg
  done
         done
		done 
			done 
				done 
					done 
						done 
							done 


