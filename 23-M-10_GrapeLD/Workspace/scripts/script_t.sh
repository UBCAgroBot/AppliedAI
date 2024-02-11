#!/bin/bash

#SBATCH --account=st-sielmann-1-gpu
#SBATCH --cpus-per-task=HOW_MANY_CPUS
#SBATCH --gpus-per-node=HOW_MANY_GPUS
#SBATCH --job-name=JOB_NAME
#SBATCH --mail-type=ALL
#SBATCH --mail-user=YOUR_EMAIL
#SBATCH --mem=MEMORY
#SBATCH --nodes=NODES
#SBATCH --ntasks=NTASKS
#SBATCH --output=output.txt
#SBATCH --error=error.txt
#SBATCH --time=TIME

module load gcc python miniconda3 cuda cudnn

source ~/.bashrc
conda activate CONDA_ENV_NAME

cd $SLURM_SUBMIT_DIR

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

PATH_TO_YOUR_PYTHON_EXEC PATH_TO_YOUR_SCRIPT

conda deactivate
 
