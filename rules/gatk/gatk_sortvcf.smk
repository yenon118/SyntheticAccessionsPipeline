rule gatk_sortvcf:
    input:
        in_file = os.path.join(os.path.abspath(output_folder),'generate_synthetic_accession','{sample}.vcf')
    output:
        out_file = os.path.join(os.path.abspath(output_folder),'gatk_sortvcf','{sample}.vcf'),
        out_tmp_dir = temp(directory(os.path.join(os.path.abspath(output_folder),'gatk_sortvcf','tmp','{sample}')))
    log:
        os.path.join(os.path.abspath(output_folder),'gatk_sortvcf_log','{sample}.log')
    resources:
        memory = memory
    conda:
         "./../../envs/gatk.yaml"
    shell:
         """
         mkdir -p {output.out_tmp_dir};
         gatk --java-options "-Xmx{resources.memory}g" SortVcf --TMP_DIR {output.out_tmp_dir} -I {input.in_file} -O {output.out_file} 2> {log}
         """
