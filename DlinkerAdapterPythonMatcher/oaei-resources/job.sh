#!/bin/bash

#SBATCH --job-nam=Automatic-alignment

#SBATCH -p highmemdell

#SBATCH -c 25 

#SBATCH --mail-user=billhappi@gmail.com

#SBATCH --mail-type=ALL 

> ./logs/running.log
> ./outputs/logs/comparisons.txt
> ./outputs/logs/links.txt

i=1;
params=``
for param in "$@" 
do
    i=$((i + 1));
    params=`echo $params $param`
done

# echo "All params : ". $params

module load system/python/3.8.12
python3.8 ./main.py $params
python3.8 ./pythonMatcher.py $params

### sh ./job.sh --source ./inputs/spaten_hobbit/source.nt --target ./inputs/spaten_hobbit/target.nt --alpha_predicate 1 --alpha 0.3 --phi 1 --measure_level 0