# Supplementary Method S3. Extraction Prompts for ROTD Data Extraction

# -------------------------------------------------------------------------
# Stage 1: Patient Identification & Demographics
# -------------------------------------------------------------------------
DEMOGRAPHIC_PROMPT_TEMPLATE = """
# Task: Identify all distinct patients from the medical literature and extract their demographic information.

# Critical Rules (MUST OBEY):
1. **No fictional patients**: Each patient MUST be explicitly described in the article. If no patients are mentioned (no age/gender/clinical details), output empty list.
2. **Avoid duplicates**: Do not extract the same patient multiple times (e.g., "Case 1" and "the patient" = same patient).
3. **No guesses**: All data from original text; uniform English; no unmentioned info.
4. **No omissions**: Capture all explicit patient data.

### Field Definitions
- pmid: PDF filename (remove ".pdf"; e.g., "33471036" for "33471036.pdf")
- pat_id: "pat_pmid_XX" (XX=01/02...; e.g., "pat_33471036_01")
- age_y: Age in years (add notes if estimated), "N/A" or integer
- age_m: "N/A" or integer (only if article specifies months/days)
- age_d: "N/A" or integer (only if article specifies months/days)
- gender: "M"/"F"/"N/A"
- ethnicity: Patient's ethnic group (e.g., "Caucasian") or "N/A"
- country: Patient's country (e.g., "United Kingdom") or "N/A"
- past_med_hist: Include: 
  ① Past diseases (e.g., "Hypertension; Diabetes"); 
  ② Surgeries (e.g., "Cataract surgery 3 years ago"); 
  ③ Medications (e.g., "Takes metformin"); 
  ④ Family history (e.g., "Family history of breast cancer"); 
  ⑤ Misdiagnoses (e.g., "Initially misdiagnosed as pterygium"); 
  ⑥ If none: "No past medical history (diseases/surgeries/medications/family history) mentioned"


# Example Output (CORRECT Format)
[
{{
      "pmid": "32306619",
      "pat_id": "pat_32306619_01",
      "age_y": "78",
      "age_m": "N/A",
      "age_d": "N/A",
      "gender": "M",
      "ethnicity": "African American",
      "country": "United States",
      "past_med_hist": "Suspected juxtapapillary posterior scleritis OS in 2011; Treated with steroids for anterior and intermediate uveitis; No other past diseases/surgeries/medications/family history mentioned"
}}
]

# Real Data
PMID: {pmid}
Article content: {article_text} 
"""

# -------------------------------------------------------------------------
# Stage 2.1: Clinical Presentation (Phenotypes & Reports)
# -------------------------------------------------------------------------
CLINICAL_PRESENTATION_PROMPT_TEMPLATE = """
# Task: Extract clinical presentation information for a specific patient.

# Provided Patient Information:
{patient_demographics}

# Critical Rules (MUST OBEY):
1. **No guesses**: All data from original text; uniform English; no unmentioned info.
2. **No omissions**: Capture all explicit clinical presentation data for this patient only.
3. Do not include data from other patients.

### Field Definitions
- phenotype_names: English phenotypic manifestations (semicolon-separated; e.g., "Visual loss; Ocular pain; Abnormal fundus morphology; Metamorphopsia; Mydriasis; Vitreous hemorrhage"); Standardized terms should be used as much as possible, such as human phenotypic ontology terms;
- reports: Inspection results (imaging/pathology/laboratory/objective signs; e.g., "OCT: Subretinal fluid; Biopsy: Squamous dysplasia") or "N/A"


# Example Output (CORRECT Format)
{{
      "phenotype_names": "Vision loss; Neovascular glaucoma; Ocular pain; Elevated large cilio-choroidal mass", 
      "reports": "Fundus: Multiple patches; Fluorescein angiography: Multifocal hyperfluorescence; OCT: Increased choroidal thickening; Ultrasound: Thickened ocular posterior wall; CT: 22-mm nodule in left upper lobe of lung, enlarged contralateral mediastinal lymph nodes; Biopsy (lung): Adenocarcinoma, non-small cell lung cancer; Biopsy (buccal mucosa): Hyperpigmentation of basal layer and melanophages in submucosa"
}}

# Real Data
PMID: {pmid}
Patient Demographics: {patient_demographics}
Article content: {article_text} 
"""

# -------------------------------------------------------------------------
# Stage 2.2: Diagnosis
# -------------------------------------------------------------------------
DIAGNOSIS_PROMPT_TEMPLATE = """
# Task: Extract diagnostic information for a specific patient.

# Provided Patient Information:
{patient_demographics}

# Critical Rules (MUST OBEY):
1. **No guesses**: All data from original text; uniform English; no unmentioned info.
2. **No omissions**: Capture all explicit diagnostic data for this patient only.
3. Do not include data from other patients.

### Field Definitions
- laterality: Lesion side ("R"/"L"/"B"/"N/A") (NO "bilateral"/"left eye").
- disease: Full diagnosis (as in article; e.g., "Ocular surface squamous neoplasia")
- location: Lesion location (e.g., "Nasal conjunctiva; Cornea") or "N/A"
- tumor_size: Tumor size (e.g., "1.0×0.5×0.4 cm") or "N/A"
- stage: Staging (e.g., "pT3") or "N/A"
- pathology: Pathological subtype (e.g., "spindle cell type") or "N/A"


# Example Output (CORRECT Format)
{{
      "laterality": "L",
      "disease": "Vasoproliferative tumor of the retina",
      "location": "Choroid (macular/juxtapapillary region, left eye)",
      "tumor_size": "9.0×9.0×4.0 mm",
      "stage": "Medium/2 (COMS/AJCC)",
      "pathology": "Mixed cell type; Heavy pigmentation; Necrosis; Limited extra-scleral extension"
}}

# Real Data
PMID: {pmid}
Patient Demographics: {patient_demographics}
Article content: {article_text} 
"""

# -------------------------------------------------------------------------
# Stage 2.3: Treatment
# -------------------------------------------------------------------------
TREATMENT_PROMPT_TEMPLATE = """
# Task: Extract treatment information for a specific patient.

# Provided Patient Information:
{patient_demographics}

# Critical Rules (MUST OBEY):
1. **No guesses**: All data from original text; uniform English; no unmentioned info.
2. **No omissions**: Capture all explicit treatment data for this patient only.
3. Do not include data from other patients.

### Field Definitions
- treatment: Treatment methods (e.g., "Topical mitomycin C; Surgical excision") or "N/A"


# Example Output (CORRECT Format)
{{
      "treatment": "Fine needle aspiration biopsy; Enucleation"
}}

# Real Data
PMID: {pmid}
Patient Demographics: {patient_demographics}
Article content: {article_text} 
"""

# -------------------------------------------------------------------------
# Stage 2.4: Outcomes
# -------------------------------------------------------------------------
OUTCOME_PROMPT_TEMPLATE = """
# Task: Extract outcome information for a specific patient.

# Provided Patient Information:
{patient_demographics}

# Critical Rules (MUST OBEY):
1. **No guesses**: All data from original text; uniform English; no unmentioned info.
2. **No omissions**: Capture all explicit outcome data for this patient only.
3. Do not include data from other patients.

### Field Definitions
- outcome: Treatment outcome (e.g., "Tumor spontaneous regression; Vision improved") or "N/A"
- va_pre: Vision before treatment (Snellen/LogMAR; e.g., "20/400 (R)") or "N/A"
- va_post: Vision after treatment (Snellen/LogMAR; e.g., "20/50 (R)") or "N/A"


# Example Output (CORRECT Format)
{{
      "outcome": "Alive at 132 months follow-up",
      "va_pre": "20/20 (L)",
      "va_post": "N/A"
}}

# Real Data
PMID: {pmid}
Patient Demographics: {patient_demographics}
Article content: {article_text} 
"""

# -------------------------------------------------------------------------
# Stage 2.5: Genomics
# -------------------------------------------------------------------------
GENOMICS_PROMPT_TEMPLATE = """
You are a medical data extraction assistant. Given the text from a case report and the demographic information of a specific patient, extract only the genetic information corresponding to this patient from the case report.

# Critical Rules (MUST OBEY):
1. No fictional data: Only extract genetic information explicitly described in the article for this patient.
2. No omissions: Extract all explicit genetic information for this patient.
3. Output a JSON array.  Each JSON object represents a mutation/variant for this patient, with all the above fields as key-value pairs.
4. If the patient has multiple mutations/variants, list each as a separate object in the array.
5. For missing fields, use empty string "". 
6. Even if there is no genetic information, still output one JSON object, all fields as "" (empty string).
7. The HGVS nomenclature must be strictly adhered to.
8. It is prohibited to add any information that is not explicitly mentioned in the original text, such as the default chromosome location of genes, the default mutation type, the default reference sequence, etc.

# Fields to Extract:
• Genetic_test_method: The genetic testing method(s) used for the patient.
• zygosity: zygosity information of the subject (e.g., heterozygous, homozygous, compound heterozygous).
• Mutation_type: Type of mutation (e.g., missense, nonsense, frameshift, splice site, deletion, duplication).
• Mutation_gene_name: Name of the mutated gene.
• Mutation_hgvs: HGVS nomenclature of the mutation, Strictly abide by the HGVS naming rule: 
• Chromosome: Chromosome explicitly reported for the mutation/gene (e.g., "Chromosome 17", "17q12").

[HGVS nomenclature#
Changes in DNA, RNA, and protein sequences, also called variants (and sometimes mutations or polymorphisms), are described using a specific language. To prevent confusion regarding its meaning, a standard has been developed for this language: the HGVS nomenclature. This standard is used world-wide, especially in human health and clinical diagnostics. This page will try to explain the standard, briefly and in simple terms. After reading, you should be able to understand the basics of the HGVS nomenclature and be able to use the internet to find more information about specific variants. In addition, while searching, you should be able to prevent making mistakes leading to misinterpretation of the variant and its possible consequences. More details, on all subjects, are available elsewhere on the HGVS nomenclature pages.

The format#
The format of a complete variant description is "reference : description" (spaces added for clarity only), e.g.;
NM_004006.2:c.4375C>T
NC_000023.11:g.32389644G>A

All variants are described in relation to a reference, the reference sequence; in the examples above, NM_004006.3 (from the GenBank database) and NC_000023.11 (from the GenBank database). After the reference, a description of the variant is given; in the examples above, c.4375C>T and g.32389644G>A.

A description without a reference sequence is near useless. Additional information will then be required to guess what reference sequence may have been used. When the guess you made is wrong, you of course end up with a variant description which is wrong, and the information you retrieved is also not correct. So be very careful when you make a guess; it is better to check the source of the original description and ask for the reference sequence that was used. Additional information to make a guess may come from the name of the gene containing the variant, the associated phenotype studied (disease), the chromosome number and from possibly predicted consequences of the variant on the RNA and/or protein level. Since reference sequences usually change over time, the date of the report describing the variant can give useful information as well.

DNA > RNA > protein#
In nature, the DNA code is first transcribed into an RNA molecule (see Wikipedia). Next, there are two options:
- the RNA molecule is translated into a protein and the protein is the final product of a gene. Proteins perform a vast array of functions, including catalysing metabolic reactions, DNA replication, responding to stimuli, providing structure to cells and organisms, transporting molecules from one location to another, etc. (see Wikipedia).
- the RNA molecule is the final product of the gene (so the RNA is not translated into a protein). RNA molecules perform a vast array of functions, including, e.g., rRNAs (ribosomal RNA) and tRNAs (transfer RNAs), both active in protein translation.
Variants are usually detected by reading the DNA code, a method called DNA sequencing. A proper report always contains the variant described on the DNA level. In addition, a report usually contains a description of the predicted consequence of the variant on the protein; rarely, the consequence on RNA is mentioned. In rare cases, not following current standards, only the predicted consequences on the protein level are reported.

Some variants have an effect on how the transcript (RNA) is generated, and consequently, on its translation into protein. When only DNA has been analysed, the consequences of the variant on the RNA and the protein level can only be predicted. The HGVS nomenclature demands predicted consequences have to be reported in parentheses. The predicted consequence of the variant NM_004006.2:c.4375C>T on the protein level is described as p.(Arg1459Ter). The "()" warn the variant described is a predicted consequence only.

Reference sequences#
Variants described on the DNA level are mostly reported in relation to a specific gene based on a so-called "coding DNA reference sequence". When a coding DNA reference sequence is used, the description of the variant starts with "c." (like in the example c.4375C>T). Since we nowadays have a reliable reference sequence of the complete human genome, it becomes more common to (also) give the description based on a "genomic reference sequence", starting with "g." (g.32407761G>A). In addition, the (predicted) consequences on the RNA level (starting with "r.") and/or the protein level (starting with "p.") may be given.
NOTE: the "p." addition is sometimes incorrectly left out when the predicted protein consequences are reported.

Reference sequences have a format like NC_000023.10, where NC_000023 is the accession number of the reference sequence and ".10" its version number. Version numbers are required since we started to use reference sequences, at a time our knowledge of the human genome was far from complete. The version number directly follows the accession number and increases over time.
For details, see "Reference Sequences".

Example descriptions#
- genomic (nucleotide)
    NC_: a genomic reference sequence based on a chromosome
        NC_000023.9:g.32317682G>A (Mar.2006: hg18, NCBI36)
        NC_000023.10:g.32407761G>A (Feb.2009: h19, GRCh37)
        NC_000023.11:g.32389644G>A (Dec.2013: hg38, GRCh38)
    NG_: a genomic reference sequence based on a Gene or Genomic region
        NG_012232.1:g.954966C>T
    LRG_: a genomic reference sequence, used in a diagnostic setting, based on a Gene or Genomic region
        LRG_199:g.954966C>T
- transcript (RNA, nucleotide)
    NM_: a reference sequence based on a protein coding RNA (mRNA)
        NM_004006.2:c.4375C>T
    NR_: a reference sequence based on a non-protein coding RNA
        NR_002196.1:n.601G>T
- protein (amino acid)
    NP_: a reference sequence based on a protein (amino acid) sequence
        NP_003997.1:p.Arg1459Ter (p.Arg1459*)
    
Genomic reference sequences#
For human, the reference sequence accession number directly in front of the version number gives the number of the chromosome: 1-22, 23 for the X-chromosome, and 24 for the Y-chromosome. In NC_000023.10 this number is "23", so a reference sequence of human chromosome X.

In many cases, the reference sequence is not given, but a genome build is mentioned. The genome build has two formats, either "hg" and a number (hg18, hg19, hg38), or "GRCh/NCBI" and a number (NCBI35, NCBI36, GRCh37, GRCh38). A genome build is an attempt to reconstruct the full human genome sequence based on all data available at the time of building the reference sequence. The most frequently used genome builds are hg18 / NCBI36 (from March 2006), hg19 / GRCh37 (from February 2009), and hg38 / GRCh38 (from December 2013). Having the genomic reference sequence (like NC_000023.10) is most precise. When the reference sequence is missing, you need to know the genome build used. In addition, when using a website or database to find more information on the variant, make sure you know the genome build (reference sequence) used by the database.
NOTE: genome builds are versioned as well, using "patches" (e.g., p1), in which errors are corrected.

Genomic reference sequences can also be based on smaller sequences not covering an entire chromosome. They usually cover only a specific gene or specific genomic segment. The most frequently used are NGs (RefSeq Gene reference sequences, format NG_012232.1) or LRGs (Locus Genomic Reference sequences, format LRG_199).

Coding DNA reference sequences#
In a human diagnostic setting, the most frequently used reference is a "coding DNA reference sequence" (description starting with "c.", e.g., NM_004006.3:c.4375C>T). Variant descriptions based on this format are very popular because they directly link to the encoded protein. In protein coding DNA reference sequences, numbering starts with 1 at the first position of the protein coding region; the A of the translation initiating ATG triplet. Numbering ends at the last position of the ending triplet; the last position of the translation stop codon (TAA, TAG, or TGA). When you divide the position number from a "c." description by three, you get the affected amino acid residue from the protein sequence (description starting with "p."); for NM_004006.3:c.4375C>T (with predicted consequence on protein level p.(Arg1459Ter)), i.e. 4375 divided by three gives amino acid 1459.
NOTE: positions before the protein coding region get a hyphen-minus sign (e.g., "c.-26"), those after the translation stop an asterisk (e.g., c.*85). Numbering in intronic sequences has a format like c.530+6 or c.531-23. For details, see "Reference Sequences". The most frequently used coding DNA reference sequences are the NMs (RefSeq gene transcript sequences, e.g., NM_004006.2) and LRGs (Locus Genomic Reference sequences, e.g., LRG_199t1).

Variants#
Depending on the change found, the description of the variant can have many different formats. For a detailed overview, please see the specific pages on this website. Here, we will list and briefly explain the major variant types.

A standard variant description has the format "prefix . position(s) change" (spaces added for clarity only). In the variant description c.4375C>T, the prefix "c." indicates the type of reference sequence used ("c." indicating a coding DNA reference sequence), "4375" is the position of the nucleotide affected, and "C>T" the change (a C changed to a T).

Types of variants#
All variants given are in the DMD gene and reported in relation to coding DNA reference sequence NM_004006.3 (LRG_199t1).

- substitution
one letter (nucleotide) of the DNA code is replaced (substituted) by one other letter. On DNA and RNA level, a substitution is indicated using ">".
    c.4375C>T
    the C nucleotide at position c.4375 changed to a T.
- deletion
one or more letters of the DNA code are missing (deleted). A deletion is indicated using "del".
    c.4375_4379del
    the nucleotides from position c.4375 to c.4379 (CGATT) are missing (deleted). Sometimes misreported as c.4375_4379delCGATT.
- duplication
one or more letters of the DNA code are present twice (doubled, duplicated). A duplication is indicated using "dup".
    c.4375_4385dup
    the nucleotides from position c.4375 to c.4385 (CGATTATTCCA) are present twice (duplicated). Sometimes misreported as c.4375_4385dupCGATTATTCCA or c.4385_4386insCGATTATTCCA.
- insertion
one or more letters in the DNA code are new (inserted). An insertion is indicated using "ins".
    c.4375_4376insACCT
    the new sequence ACCT was found inserted between positions c.4375 and c.4376.
- deletion/insertion (delins)
one or more letters in the DNA code are missing and replaced by several new letters. A deletion/insertion is indicated using "delins".
    c.4375_4376delinsAGTT
    the nucleotides from position c.4375 to c.4376 (CG) are missing (deleted) and replaced by the new sequence, AGTT. Sometimes misreported as c.4375_4376delCGinsAGTT.
There are more variant types, yet these occur less frequently.

Aliases#
It should be noted that one variant, based on different reference sequences used, can be described in many different ways. Variant c.5234G>A in the DMD gene can be described based on different genomic reference sequences (e.g., NC_000023.9:g.32290917C>T, NC_000023.10:g.32380996C>T, NC_000023.11:g.32362879C>T, NG_012232.1:g.981731G>A, and LRG_199:g.981731G>A) as well as different coding DNA reference sequences (e.g., LRG_199t1:c.5234G>A, NM_004006.3:c.5234G>A, NM_004009.3:c.5222G>A, NM_000109.3:c.5210G>A, NM_004007.2:c.4865G>A, NM_004010.3:c.4865G>A, NM_004011.3:c.1211G>A, NM_004012.3:c.1202G>A, etc.). These alternative descriptions are rather confusing, especially when reference sequences are not properly listed. Consequently, when databases or the internet are queried for information regarding the potential consequences of specific variants, errors are easily made.

Other descriptions#
Sometimes, variants are not described using the format reference:description (NM_004006.3:c.4375C>T) explained above, but using an identifier (ID) in another database. Common formats include a rs ID (from dbSNP, rs128627255), OMIM ID (from OMIM, OMIM300377:0073), LOVD ID (from LOVD, DMD_000073), RCV ID (from ClinVar, RCV000012030), etc. In most cases, using these IDs, the database can be used to find the full description of the variant using the approved HGVS format reference:description.

Missing information#
When a reference sequence is not known, the best way forward is to try and get the name of the gene that is affected by the variant. All genes have an official abbreviation: the gene symbol. For the Duchenne muscular dystrophy gene, the gene symbol is "DMD". The HGNC (HUGO Gene Nomenclature Committee) keeps a catalog of all approved gene symbols and their aliases/synonyms. The HGNC site can be used to find the gene symbol and check whether the name/symbol you have is the officially approved one. Using "dystrophin", the name of a protein, you will see this is an alias for the Duchenne muscular dystrophy gene, official gene symbol "DMD". HGNC, and many other sources, can also tell you on which human chromosome a gene is, so to which chromosome the variant description you have may relate.
]


# Example Output 1:
[
    {{
    "Genetic_test_method": "whole exome sequencing",
    "zygosity": "compound heterozygous",
    "Mutation_type": "missense",
    "Mutation_gene_name": "GAA",
    "Mutation_hgvs": "NM_000152.5:c.2238G>C",
    "Chromosome": "17q25.3"
    }},
    {{
    "Genetic_test_method": "whole exome sequencing",
    "zygosity": "compound heterozygous",
    "Mutation_type": "frameshift",
    "Mutation_gene_name": "BRCA1",
    "Mutation_hgvs": "NM_007294.4:c.68_69del",
    "Chromosome": "17q21.31"
    }}
]

# Example Output 2: 
[
    {{
    "Genetic_test_method": "",
    "zygosity": "",
    "Mutation_type": "",
    "Mutation_gene_name": "ABCA12",
    "Mutation_hgvs": "",
    "Chromosome": ""
    }}
]

# Real Data
PMID: {pmid}
Provided demographic information: {patient_demographics}
Case report: {article_text} 
"""