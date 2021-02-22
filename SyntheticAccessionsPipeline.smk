import sys
import os
import re

project_name = config['project_name']
workflow_path = config['workflow_path']
input_files = config['input_files']
output_folder = config['output_folder']
memory = config['memory']
threads = config['threads']

samples = []
input_folder = ''
input_extension = ''

for i in range(len(input_files)):
    if os.path.dirname(input_files[i]) != input_folder:
        input_folder = os.path.dirname(input_files[i])
    possible_sample = re.sub('(\\.vcf.*)', '', str(os.path.basename(input_files[i])))
    if not possible_sample in samples:
        samples.append(possible_sample)
    possible_extension = re.sub(possible_sample,'',str(os.path.basename(input_files[i])))
    if possible_extension != input_extension:
        input_extension = possible_extension


rule all:
    input:
        expand(os.path.join(os.path.abspath(output_folder),'generate_synthetic_accession_summary','{sample}.txt'), sample=samples),
        expand(os.path.join(os.path.abspath(output_folder),'generate_synthetic_accession','{sample}.vcf'), sample=samples),
        expand(os.path.join(os.path.abspath(output_folder),'gatk_sortvcf','{sample}.vcf'), sample=samples),
        os.path.join(os.path.abspath(output_folder),'gatk_gathervcfs','{project_name}.vcf'.format(project_name=project_name))


include: './rules/python/generate_synthetic_accession.smk'

include: './rules/gatk/gatk_sortvcf.smk'
include: './rules/gatk/gatk_gathervcfs.smk'
