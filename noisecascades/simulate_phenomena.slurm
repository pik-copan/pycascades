#!/bin/bash

# HERE Slurm jobscript that starts an array with jobs
# Each job gets one config_id / alpha / sigma combination
# Each job runs over GMT / strength / 500 seeds using 16 cpus...
# Each job saves only the FPT and Oktant to one big zarr array.
# Need to figure out where i can save this data.




# Example of running a job array to run Julia hello world

#SBATCH --array=0-27              # there is a max array size - 512 tasks
#SBATCH --job-name noisecascades
#SBATCH -p standard
##SBATCH -q priority
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
##SBATCH -t 1:00:00
##SBATCH -o noisestrength-%A-%a.out

# Load software
source ~/.bashrc

conda activate pycascades

cd $HOME/code/pycascades/noisecascades
# Run Julia with a command line arg being an index from 1 to 10
python simulate_phenomena.py $SLURM_ARRAY_TASK_ID
 #srun