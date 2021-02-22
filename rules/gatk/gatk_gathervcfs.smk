rule gatk_gathervcfs:
    input:
        in_file = expand(os.path.join(os.path.abspath(output_folder),'gatk_sortvcf','{sample}.vcf'), sample=samples)
    params:
          ' '.join(['-I '+os.path.join(os.path.abspath(output_folder),'gatk_sortvcf','{sample}.vcf'.format(sample=sample)) for sample in samples])
    output:
        out_file = os.path.join(os.path.abspath(output_folder),'gatk_gathervcfs','{project_name}.vcf'.format(project_name=project_name)),
        out_tmp_dir = temp(directory(os.path.join(os.path.abspath(output_folder),'gatk_gathervcfs','tmp',project_name)))
    log:
        os.path.join(os.path.abspath(output_folder),'gatk_gathervcfs_log','{project_name}.log'.format(project_name=project_name))
    resources:
        memory = memory
    conda:
         "./../../envs/gatk.yaml"
    shell:
         """
         mkdir -p {output.out_tmp_dir};
         gatk --java-options "-Xmx{resources.memory}g" GatherVcfs --TMP_DIR {output.out_tmp_dir} {params} -O {output.out_file} 2> {log}
         """
