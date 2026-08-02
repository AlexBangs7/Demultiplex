#!/bin/bash
#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 # optional: number of cpus, default is 1
#SBATCH --mem=16GB                        # optional: amount of memory, default is 4GB per cpu
#SBATCH --job-name=qscore-R1             # optional: job name


/usr/bin/time -v pixi run ./Assignment-the-first/Part1.py \
    --read R1