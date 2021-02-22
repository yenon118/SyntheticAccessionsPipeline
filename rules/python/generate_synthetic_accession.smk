rule generate_synthetic_accession:
    input:
        in_file = os.path.join(os.path.abspath(input_folder),'{sample}'+input_extension)
    output:
        summary_file = os.path.join(os.path.abspath(output_folder),'generate_synthetic_accession_summary','{sample}.txt'),
        out_file = os.path.join(os.path.abspath(output_folder),'generate_synthetic_accession','{sample}.vcf')
    log:
        os.path.join(os.path.abspath(output_folder),'generate_synthetic_accession_log','{sample}.log')
    resources:
        memory = memory
    threads: threads
    shell:
        """
        python3 {workflow_path}/scripts/python/generate_synthetic_accession.py -i {input.in_file} -o {output.out_file} -t {threads} -s {output.summary_file}
        """
