# Disease Gene Identification - Single File Script
# Fetches nucleotide sequences for selected genes from NCBI and computes
# sequence length and GC content, then saves a CSV and two plots.

from Bio import Entrez, SeqIO
import pandas as pd
import matplotlib.pyplot as plt
import time  # for delays between NCBI requests

# --------- SETTINGS ----------
Entrez.email = "your_email@example.com"   # required by NCBI: use your own email
genes = ["BRCA1", "TP53", "EGFR"]          # example disease-related genes
organism = "Homo sapiens"


# --------- FUNCTIONS ----------
def fetch_gene_sequence(gene_name):
    handle = Entrez.esearch(
        db="nucleotide",
        term=f"{gene_name}[Gene] AND {organism}[Organism]",
        retmax=1,
    )
    record = Entrez.read(handle)
    handle.close()
    time.sleep(0.5)  # small delay after esearch

    if not record["IdList"]:
        return None

    seq_id = record["IdList"][0]
    handle = Entrez.efetch(
        db="nucleotide",
        id=seq_id,
        rettype="fasta",
        retmode="text",
    )
    seq_record = SeqIO.read(handle, "fasta")
    handle.close()
    time.sleep(0.5)  # small delay after efetch

    return str(seq_record.seq)


def gc_content(sequence):
    g = sequence.count("G")
    c = sequence.count("C")
    return (g + c) / len(sequence) * 100


# --------- MAIN ANALYSIS ----------
data = []

for gene in genes:
    seq = fetch_gene_sequence(gene)
    if seq:
        length = len(seq)
        gc = gc_content(seq)
        data.append([gene, length, gc])

df = pd.DataFrame(data, columns=["Gene", "Length", "GC_Content"])

# Save results
df.to_csv("disease_genes_analysis.csv", index=False)

# --------- PLOTS ----------
plt.figure()
plt.bar(df["Gene"], df["Length"])
plt.xlabel("Gene")
plt.ylabel("Sequence Length")
plt.title("Gene Length Analysis")
plt.savefig("gene_length_plot.png")
plt.show()

plt.figure()
plt.bar(df["Gene"], df["GC_Content"])
plt.xlabel("Gene")
plt.ylabel("GC Content (%)")
plt.title("GC Content Analysis")
plt.savefig("gc_content_plot.png")
plt.show()

print("Analysis complete. Files saved successfully.")
