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

-------------------------------------------------------

### [08-01-2026]

- Examine files
    - R1 = Read1 (102 bases)
    - R2 = Index1 (8 bases)
    - R3 = Index2 (Rev-Comp)
    - R4 = Read2
    - Phred +33 encoding

**Scripts run:**

```x```

**Commands run:**

` less /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R1_001.fastq.gz `
` less /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R2_001.fastq.gz `
` less /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R3_001.fastq.gz `
` less /projects/bgmp/shared/2017_sequencing/1294_S1_L008_R4_001.fastq.gz `

**Job resource usage (`/usr/bin/time -v` summary from Talapas):**

N/A

---