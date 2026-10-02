#!/bin/bash
#SBATCH --job-name=course-hold
#SBATCH --partition=cpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --exclusive
#SBATCH --time=00:02:00
#SBATCH --output=course-hold-%j.out
set -euo pipefail
test "$(scontrol show config | awk '$1 == "ClusterName" {print $3}')" = rack-course
srun sleep 90
