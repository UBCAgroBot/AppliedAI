#!/bin/bash

#SBATCH --time=00:20:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --gpus-per-node=1
#SBATCH --mem=16GB
#SBATCH --job-name=aa_test
#SBATCH --account=st-sielmann-1-gpu
#SBATCH --mail-user=mali8@student.ubc.ca
#SBATCH --mail-type=ALL
#SBATCH --output=/scratch/st-sielmann-1/agrobot/auto-annotation-demo/out.txt
#SBATCH --error=/scratch/st-sielmann-1/agrobot/auto-annotation-demo/error.txt

############################################################################################################################

python autoannot.py data annotations true
