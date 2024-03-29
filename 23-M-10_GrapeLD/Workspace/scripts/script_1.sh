#!/bin/bash

#SBATCH --account=st-sielmann-1-gpu
#SBATCH --cpus-per-task=12
#SBATCH --gpus-per-node=4
#SBATCH --job-name=grape-ld
#SBATCH --mail-type=ALL
#SBATCH --mail-user=astrollin.neil@gmail.com
#SBATCH --mem=16G
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --output=output.txt
#SBATCH --error=error.txt
#SBATCH --time=8:00:00

module load gcc python miniconda3 cuda cudnn

source ~/.bashrc
conda activate grape-ld

cd $SLURM_SUBMIT_DIR

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

/home/nlin06/miniconda3/envs/grape-ld/bin/python /scratch/st-sielmann-1/agrobot/grape-ld/__main__.py

conda deactivate
 
