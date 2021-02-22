import sys
import os
import re
import gzip
import pathlib
import argparse

from joblib import Parallel, delayed


def generate_reference_line_and_synthetic_line(header, line, output_file_path, summary_file_path=None):
    line = str(line).strip()
    line_array = line.split("\t")

    line_array[2] = "."
    line_array[5] = "."
    line_array[6] = "PASS"
    line_array[7] = "."
    line_array[8] = "GT"

    reference_allele = line_array[3].strip()
    alternate_alleles = line_array[4].strip().split(',')

    genotypes = []

    # Replace genotype indexes with alleles
    for i in range(9, len(line_array)):
        line_array[i] = re.sub("(:.*)", "", line_array[i])
        genotype_indexes_array = line_array[i].split("/")
        genotype = ['.'] * len(genotype_indexes_array)
        for j in range(len(genotype_indexes_array)):
            if genotype_indexes_array[j] != '' and genotype_indexes_array[j] != '.':
                try:
                    genotype_indexes_array[j] = int(genotype_indexes_array[j])
                    if genotype_indexes_array[j] == 0:
                        genotype[j] = reference_allele
                    else:
                        genotype[j] = alternate_alleles[genotype_indexes_array[j] - 1]
                except ValueError as e:
                    genotype_indexes_array[j] = '.'
                    genotype[j] = '.'

        genotypes.append('/'.join(genotype))

    # Generate genotypes frequency dictionary
    genotypes_frequency_dict = {}
    for i in range(len(genotypes)):
        if genotypes[i] not in genotypes_frequency_dict.keys():
            genotypes_frequency_dict[genotypes[i]] = 1
        else:
            genotypes_frequency_dict[genotypes[i]] = genotypes_frequency_dict[genotypes[i]] + 1

    # Sort genotypes frequency dictionary
    sorted_genotypes_frequency_dict = {}
    for item in sorted(genotypes_frequency_dict.items(), key=lambda x: x[1], reverse=True):
        if item[0] not in sorted_genotypes_frequency_dict.keys():
            sorted_genotypes_frequency_dict[item[0]] = item[1]

    # Remove missing ./.
    sorted_genotypes_frequency_dict_without_missing = sorted_genotypes_frequency_dict.copy()
    if './.' in sorted_genotypes_frequency_dict_without_missing.keys():
        temp = sorted_genotypes_frequency_dict_without_missing.pop('./.')

    # Split into reference genotypes frequency and alternate genotypes frequency
    reference_genotypes_frequency_dict = {}
    alternate_genotypes_frequency_dict = sorted_genotypes_frequency_dict.copy()
    if str(reference_allele + '/' + reference_allele) in alternate_genotypes_frequency_dict.keys():
        reference_genotypes_frequency = alternate_genotypes_frequency_dict.pop(
            str(reference_allele + '/' + reference_allele))
        if str(reference_allele + '/' + reference_allele) not in reference_genotypes_frequency_dict.keys():
            reference_genotypes_frequency_dict[
                str(reference_allele + '/' + reference_allele)] = reference_genotypes_frequency

    # Determine reference synthetic line genotype
    line_array.append('0/0')

    # Determine alternate synthetic line genotype
    alternate_genotype_array = ['.']*2
    for key in alternate_genotypes_frequency_dict.keys():
        if key != './.':
            genotype_indexes_array = str(key).split("/")
            if len(genotype_indexes_array) == 2 and genotype_indexes_array[0] == genotype_indexes_array[1]:
                alternate_genotype_array[0] = alternate_alleles.index(genotype_indexes_array[0])+1
                alternate_genotype_array[1] = alternate_alleles.index(genotype_indexes_array[1])+1
                break
    line_array.append('/'.join([str(element) for element in alternate_genotype_array]))

    # Write to output VCF file
    with open(output_file_path, 'a') as writer:
        writer.write(str('\t'.join(line_array)) + '\n')

    # Write alleles and their frequency into summary file
    if summary_file_path is not None:
        frequency_str = str(line_array[0]) + "\t" + \
                        str(line_array[1]) + "\t" + \
                        str(''.join(list(reference_genotypes_frequency_dict.keys()))) + "\t" + \
                        str(''.join(
                            [str(element) for element in list(reference_genotypes_frequency_dict.values())])
                        ) + "\t" + \
                        str(', '.join(list(alternate_genotypes_frequency_dict.keys()))) + "\t" + \
                        str(', '.join(
                            [str(element) for element in list(alternate_genotypes_frequency_dict.values())])
                        ) + "\n"
        if summary_file_path.exists():
            with open(summary_file_path, 'a') as writer:
                writer.write(frequency_str)


def main(args):
    #######################################################################
    # Get arguments
    #######################################################################
    input_file_path = args.input_file
    output_file_path = args.output_file

    n_jobs = args.threads
    summary_file_path = args.summary_file

    #######################################################################
    # Check if output parent folder exists
    # If not, create the output parent folder
    #######################################################################
    if not output_file_path.parent.exists():
        try:
            output_file_path.parent.mkdir(parents=True)
        except FileNotFoundError as e:
            pass
        except FileExistsError as e:
            pass
        except Exception as e:
            pass
        if not output_file_path.parent.exists():
            sys.exit(1)

    #######################################################################
    # If summary file path is not none, check if summary parent folder exists
    # If not, create the output parent folder
    #######################################################################
    if summary_file_path is not None:
        if not summary_file_path.parent.exists():
            try:
                summary_file_path.parent.mkdir(parents=True)
            except FileNotFoundError as e:
                pass
            except FileExistsError as e:
                pass
            except Exception as e:
                pass
            if not summary_file_path.parent.exists():
                sys.exit(1)

    #######################################################################
    # Open input file
    #######################################################################
    if str(input_file_path).endswith("gz"):
        reader = gzip.open(input_file_path, 'rt')
    else:
        reader = open(input_file_path, 'r')

    #######################################################################
    # Process input file
    #######################################################################
    input_metadata_array = []
    header = ""
    while not header.strip().startswith("#CHROM"):
        header = reader.readline()
        if header.startswith("##"):
            if not header.startswith("##GATK"):
                input_metadata_array.append(str(header).strip())

    # Write metadata and header
    with open(output_file_path, 'w') as writer:
        writer.write(str('\n'.join(input_metadata_array))+'\n')
        writer.write(header.strip() + '\tRef_syn\tAlt_syn\n')

    if summary_file_path is not None:
        # Write summary file header
        with open(summary_file_path, 'w') as writer:
            writer.write('Chromosome\tPosition\tReference\tReference_count\tAlternate\tAlternate_count\n')

    Parallel(n_jobs=n_jobs)(
        delayed(generate_reference_line_and_synthetic_line)(header, line, output_file_path, summary_file_path)
        for line in reader
    )

    #######################################################################
    # Close input file
    #######################################################################
    reader.close()


if __name__ == "__main__":
    #######################################################################
    # Parse arguments
    #######################################################################
    parser = argparse.ArgumentParser(prog='generate_synthetic_line', description='generate synthetic line')

    parser.add_argument('-i', '--input_file', help='Input file', type=pathlib.Path, required=True)
    parser.add_argument('-o', '--output_file', help='Output file', type=pathlib.Path, required=True)

    parser.add_argument('-t', '--threads', help='Number of threads', type=int, default=10)
    parser.add_argument('-s', '--summary_file', help='Summary file', type=pathlib.Path, default=None)

    args = parser.parse_args()

    #######################################################################
    # Call main function
    #######################################################################
    main(args)
