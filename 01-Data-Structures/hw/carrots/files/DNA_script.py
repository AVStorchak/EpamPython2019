def translate_from_dna_to_rna(dna):
    rna = dna.replace('T', 'U')

    return rna


def count_nucleotides(dna):
    nucleotide_set = sorted(set(dna))
    num_of_nucleotides = {}
    for nucleotide in nucleotide_set:
        num_of_nucleotides[nucleotide] = dna.count(nucleotide)

    return num_of_nucleotides


def translate_rna_to_protein(dna):
    with open('rna_codon_table.txt') as f:
        raw = f.read()

    codon_dict = {}
    codon_string = " ".join(raw.split())
    for i in codon_string.split():
        if len(i) == 3:
            codon_dict[i] = ''
            current_key = i
        elif i == "Stop":
            codon_dict[current_key] = '-'
        else:
            codon_dict[current_key] = i

    n = 3
    rna = translate_from_dna_to_rna(dna)
    original_string = [rna[i:i+n] for i in range(0, (len(rna)//3)*3, n)]
    converted_string = []

    for i in original_string:
        converted_string.append(codon_dict[i])
    protein = ''.join(i for i in converted_string)

    return protein


with open('dna.fasta') as f:
    raw_input = f.readlines()
    genes = {}

for line in raw_input:
    if 'gene' in line:
        gene_name = line.strip('\n')
        genes[gene_name] = ''
    else:
        genes[gene_name] = ''.join([genes[gene_name], line.strip('\n')])

with open('dna_statistics.txt', 'w') as f:
    for name, sequence in genes.items():
        print(f'{name} contains: {count_nucleotides(sequence)}', file = f)

with open('rna_list.fasta', 'w') as f:
    for name, sequence in genes.items():
        f.write(f'{name} corresponds to the following RNA:\n')
        f.write(f'{translate_from_dna_to_rna(sequence)}\n')

with open('codon_sequence.fasta', 'w') as f:
    for name, sequence in genes.items():
        f.write(f'{name} corresponds to the following protein:\n')
        f.write(f'{translate_rna_to_protein(sequence)}\n')