#!/bin/bash
#SBATCH --job-name=course-checkpoint
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=128M
#SBATCH --time=00:03:00
#SBATCH --requeue
#SBATCH --open-mode=append
#SBATCH --output=course-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
test "$(scontrol show config | awk '$1 == "ClusterName" {print $3}')" = rack-course
echo "job=$SLURM_JOB_ID attempt=${SLURM_RESTART_COUNT:-0} node=$SLURMD_NODENAME"
exec srun python3 ../workload.py --directory "evidence/job-$SLURM_JOB_ID" --steps 100 --delay 0.5
