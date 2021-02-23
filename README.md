# SyntheticAccessionsPipeline

<!-- badges: start -->
<!-- badges: end -->

The SyntheticAccessionsPipeline is a pipeline built for generating synthetic accessions into next-generation sequencing (NGS) whole-genome sequencing datasets.

## Requirements

In order to run the SyntheticAccessionsPipeline, users need to install software, programming languages, and packages in their computing systems.
The software, programming languages, and packages include: 

```
GATK>=4.1.7.0
Python3>=3.7.0
Snakemake>=5.31.0
Pandas>=1.1.3
``` 

## Installation

You can install the SyntheticAccessionsPipeline from [Github](https://github.com/yenon118/SyntheticAccessionsPipeline.git) with:

```
git clone https://github.com/yenon118/SyntheticAccessionsPipeline.git
```

## Usage

#### Write a configuration file in json format

Please save the file with .json extension.

```
{
  "project_name": "Soy775",
  "workflow_path": "/scratch/yenc/projects/SyntheticAccessionsPipeline",
  "input_files": [
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr01.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr02.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr03.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr04.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr05.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr06.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr07.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr08.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr09.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr10.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr11.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr12.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr13.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr14.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr15.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr16.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr17.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr18.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr19.vcf",
    "/scratch/yenc/projects/SyntheticAccessionsPipeline/data/Soy775/Soy775_Chr20.vcf"
  ],
  "output_folder": "/scratch/yenc/projects/SyntheticAccessionsPipeline/output/",
  "memory": 100,
  "threads": 10
}
```

#### Run workflow with the Snakemake workflow management system

```
snakemake -pj NUMBER_OF_JOBS --configfile CONFIGURATION_FILE --snakefile SNAKEMAKE_FILE

Mandatory Positional Argumants:
    NUMBER_OF_JOBS                          - the number of jobs
    CONFIGURATION_FILE                      - a configuration file
    SNAKEMAKE_FILE                          - the snakyVC.smk file that sit inside this repository 
```

## Examples

These are a few basic examples which show you how to use the SyntheticAccessionsPipeline:

```
cd /path/to/SyntheticAccessionsPipeline

snakemake -pj 10 --configfile Soy775_inputs.json --snakefile SyntheticAccessionsPipeline.smk
```

```
cd /path/to/SyntheticAccessionsPipeline

snakemake -pj 10 --configfile Nebraska_inputs.json --snakefile SyntheticAccessionsPipeline.smk
```
