# Lab Notebook — Demultiplexing Assignment 1

**Base Directory**
- `/projects/bgmp/abangs/bioinfo/Bi622/Demultiplex`

**Environment / Versions:**
- Compute environment:
    - talapas login node
    - bgmp compute node

- Software/package versions:
    - 

**Data Source:**

File from talapas
```
/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz # Biological reads
/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz # Index reads
/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz # Index reads
/projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz # Biological reads
```

-------------------------------------------------------

### [07-21-2026]

-Write psuedocode for part 2

**Scripts run:**

N/A

**Commands run:**

N/A

**Job resource usage (`/usr/bin/time -v` summary from Talapas):**

N/A

----------------------------------------------------

### [08-02-2026]

- Resolve bugs in Part1.py
- Add script to write distribution to tsv
- Add script to create distribution figure 
- Run on test files
- Run on sequencing files

**Scripts run:**

```
qscore-R1.sh
qscore-R2.sh
qscore-R3.sh
qscore-R4.sh
```

**Commands run:**

```
pixi shell 
./Assignment-the-first.Part1.py -t True R1 
./Assignment-the-first.Part1.py -t True R2 
./Assignment-the-first.Part1.py -t True R3 
./Assignment-the-first.Part1.py -t True R4 
```
```
sbatch Assignment-the-first/qscore-R1.sh
sbatch Assignment-the-first/qscore-R2.sh
sbatch Assignment-the-first/qscore-R3.sh
sbatch Assignment-the-first/qscore-R4.sh
```
```
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R
2_001.fastq.gz | grep -A 1 "^@" | grep -v "^@" | grep N | wc -l
zcat /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R
3_001.fastq.gz | grep -A 1 "^@" | grep -v "^@" | grep N | wc -l
```

**Job resource usage (`/usr/bin/time -v` summary from Talapas):**

```
Command being timed: "pixi run ./Assignment-the-first/Part1.py --read R1"
Percent of CPU this job got: 99%
Elapsed (wall clock) time (h:mm:ss or m:ss): 37:43.23
Maximum resident set size (kbytes): 72900
```
```
Command being timed: "pixi run ./Assignment-the-first/Part1.py --read R2"
Percent of CPU this job got: 99%
Elapsed (wall clock) time (h:mm:ss or m:ss): 6:32.35
Maximum resident set size (kbytes): 70772
```
```
Command being timed: "pixi run ./Assignment-the-first/Part1.py --read R3"
Percent of CPU this job got: 99%
Elapsed (wall clock) time (h:mm:ss or m:ss): 6:16.47
Maximum resident set size (kbytes): 73040
```
```
Command being timed: "pixi run ./Assignment-the-first/Part1.py --read R4"
Percent of CPU this job got: 99%
Elapsed (wall clock) time (h:mm:ss or m:ss): 37:07.10
Maximum resident set size (kbytes): 70400
Exit status: 0
```

----------------------------------------------------------