import random
import json
from faker import Faker
from faker.providers import BaseProvider
from datetime import timedelta
import csv
import sys
import copy
fake = Faker()

class MedicalProvider(BaseProvider):
    """
    A custom provider for generating medical terms.
    """
    def gene(self):
        """
        Generate a gene name
        """
        genes = ['FGFR3', 'PDGFRB', 'CHEK2', 
                'SF3B1', 'DDR2', 'HSP90B1',
                'CDKN2A', 'EGFR', 'PHF6', 'KLF1',
                'HBB', 'AKT1', 'IDH1', 'ALDH2', 'FOXL2', 
                'FBXW7', 'BLM', 'MSH2', 'NOTCH1', 'MTOR',
                'DNMT3A', 'SDHD', 'IDH2', 'H3.3', 'XPC', 'MYCN',
                'PTEN', 'ERBB2', 'NF1', 'STAG2', 'KRAS', 'NT5C2',
                'MUTYH', 'PKLR', 'MYOD1', 'ALK', 'SDHB', 'FGFR1', 'MYD88',
                'JAK2', 'NTRK1', 'U2AF1', 'CSF1R', 'PAX5', 'FGFR4', 'B2M', 'TP53',
                'IKZF1', 'SIX1', 'PRKCA', 'SRSF2', 'MAPK1', 'CD74', 'EZH2', 'DICER1',
                'ARHGAP45', 'CDC73', 'CHD6', 'SDHA', 'TOP2A', 'FGFR2', 'FLT3', 'RB1',
                'RNF43', 'CCND3', 'CTNNB1', 'HRAS', 'TEK', 'BTK', 'KLF4', 
                'HDAC1', 'HBA2','MYO1G', 'MAP2K2', 'APC', 'KIT', 'BRAF', 'CSF3R', 'GNAS',
                'JAK3', 'ABL1', 'CALR', 'HSD3B1', 'ARID2', 'BRCA1', 'PDGFRA', 'BRCA2', 
                'SMO', 'ZEB2', 'MET', 'HDAC2', 'PIK3CA', 'STAT5B', 'PTCH1', 'NRAS',
                'TLR8', 'MPL', 'ERCC2', 'NCSTN', 'PTPN11', 'DPYD', 'ARID2']
        return self.random_element(genes)
    
    def mutation(self):
        """
        Generate a mutation name
        """
        mutations = ["Missensevariant(exon2)-GOF",
                        "Stopgain-LOF",
                        "Frameshift-LOF",
                        "Frameshift-GOF",
                        "Spliceregionvariant-LOF",
                        "Spliceregionvariant-GOF",
                        "Nonsense-LOF",
                        "Nonsense-GOF"]
        
        return self.random_element(mutations)
    
    
# Create a Faker instance
fake = Faker()

# Add the MedicalProvider to the Faker instance
fake.add_provider(MedicalProvider)
# gene = fake.gene()

descriptions = {'KRAS':"KRAS is a GDP/GTP binding protein that acts as an intracellular signal transducer. KRAS is involved in several pathways involved in cellular proliferation and survival, including the PI3K-AKT-mTOR pathway and the Ras-Raf-MEK-ERK pathway. Activating mutations, copy number gains, and overexpression of KRAS are associated with cancer progression.",
                'ARID2':"ARID2 encodes a protein that is a subunit of the SWI/SNF chromatin remodeling complex SWI/SNF-B or PBAF. This complex functions in ligand-dependent transcriptional activation. Loss of function mutations and copy number loss of ARID2 are associated with cancer progression.",
                'RBM10':"RBM10 encodes a protein that contains a RNA-binding motif and interacts with RNA homopolymers, and is thought to function in regulating alternative splicing. Loss of function mutations and copy number loss of RBM10 are associated with cancer progression.",
                'STK11': "STK11 (LKB1) encodes an enzyme in the serine/threonine kinase family that is responsible for maintaining energy metabolism and cellular polarization through the activation of AMP-activated protein kinase and other members of the AMPK family. The enzyme also acts as a tumor suppressor by regulating cell growth. Loss of function mutations, copy number loss, epigenetic variation, and underexpression of STK11 are associated with cancer progression.",
                'TP53':"TP53 encodes a protein that is a transcription factor that regulates the expression of genes involved in cell cycle arrest, apoptosis, and DNA repair. TP53 is a tumor suppressor gene that is mutated in many cancers. Mutations in TP53 are associated with cancer progression.",
                'NFEL2L2': "NFE2L2 acts as a transcription factor for proteins that contain an antioxidant response element (ARE) within their promoter sequence. Genes that contain ARE are involved in injury and inflammation response. Activating mutations and overexpression of NFE2L2 are associated with cancer progression.",
                'FAT1': "FAT1 encodes a transmembrane protein involved in tumor suppressor signaling. FAT1 protein can regulate transcriptional activity by sequestering beta-catenin, thereby preventing it from entering the nucleus. Loss of function mutations and copy number loss of FAT1 are associated with cancer progression.",
                'BCL11B': "BCL11B encodes a C2H2-type zinc finger protein that functions as a transcriptional repressor and plays a role in T-cell development and survival. Loss of function mutations, copy number loss, and fusions resulting in the underexpression of BCL11B are associated with cancer progression.",
                'PTEN': "PTEN encodes a phosphatase that acts as a tumor suppressor by negatively regulating the PI3K-AKT-mTOR pathway. Loss of function mutations, copy number loss, and underexpression of PTEN are associated with cancer progression.",
                }

doctor = fake.name()
with open('./Dictionaries/cancer_diagnoses.csv', 'r') as file:
    reader = csv.DictReader(file)
    
    # Convert the CSV data to a list of dictionaries
    data_list = list(reader)
    
    # Pick a random cancer type
    random_cancer_entry = random.choice(data_list)
    
    # Get the cancer type and a random diagnosis associated with it
    cancer_type = random_cancer_entry['Cancer']
    diagnoses = random_cancer_entry['Diagnosis'].split(', ')
    random_diagnosis = random.choice(diagnoses)
def generate_patient_details():
    name = fake.name()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=90)
    sex = random.choice(['Male', 'Female'])
    
    diagnosis = random_diagnosis
    bodypart = cancer_type.split()[0]
    physician = " ".join(["Dr.", doctor])
    treating_institution = fake.company()

    patient_details = {
        'Name': name,
        'DateOfBirth': str(date_of_birth),
        'Sex': sex,
        'Diagnosis': diagnosis,
        'BodyPart': bodypart,
        'Physician': physician,
        'TreatingInstitution': treating_institution
    }
    return patient_details

cdate1 = fake.date_between(start_date='-1y', end_date='today')
def generate_specimen_details():
    cdate2 = cdate1 + timedelta(days=random.randint(1, 7))
    specimen_details = {
        'Tumor specimen':{
            'source': cancer_type.split()[0],
            'CollectedDate': str(cdate1),
            'ReceivedDate': str(fake.date_between(start_date=cdate1, end_date=cdate1+fake.time_delta(timedelta(days=10)))),
            'TumorPercentage': f'{random.randint(1, 100)}%'
        },
        'Normal specimen':{
            'source': "Blood",
            'CollectedDate': str(cdate2),
            'ReceivedDate': str(fake.date_between(start_date=cdate2, end_date=cdate2+fake.time_delta(timedelta(days=10))))
        }
    }
    return specimen_details

spa = []
sbr = []
def generate_genomic_variants():
    
    spa_count = random.randint(1, 4)
    if spa_count <= 2:
        sbr_count = random.randint(1, 6)
    else:
        sbr_count = random.randint(1, 3)
    i = 40.0
    for _ in range(spa_count):
        variants = []
        gene = fake.gene()
        with open('./Dictionaries/ncit-protein-variants.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Gene'] == gene:
                    variant = row['Protein Variant']
                    variants.append(variant)

        random_variant = random.choice(variants)
        variant = {
            'Gene': gene ,
            'GeneMutation': random_variant + ' ' + fake.mutation(),
            'VariantAlleleFraction': f'{round(random.uniform(1.0, i), 2)}%'
        }
        spa.append(variant)
        i -= 5.0
    for _ in range(sbr_count):
        gene = fake.gene()
        with open('./Dictionaries/ncit-protein-variants.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Gene'] == gene:
                    variant = row['Protein Variant']
                    variants.append(variant)

        random_variant = random.choice(variants)
        variant = {
            'Gene': gene,
            'GeneMutation': random_variant + ' ' + fake.mutation(),
            'VariantAlleleFraction': f'{round(random.uniform(1.0, i), 2)}%'
        }
        sbr.append(variant)
        i -= 5.0
    genomic_variants = {
        "Somatic - Potentially Actionable": spa,
        "Somatic - Biologically Relevant": sbr,
        "Germline - Pathogenic": [],
        "Pertinent Negatives": [fake.gene() for _ in range(random.randint(0, 5))]
    }
    return genomic_variants


def generate_variants_of_unknown_significance():
    
    somatic_count = random.randint(6, 12)
    if somatic_count <= 8:
        germline_count = random.randint(1, 2)
    else:
        germline_count = 0
    i = 25.0
    svariants_uks = []
    gvariants_uks = []
    for _ in range(somatic_count):
        variants = []
        gene = fake.gene()
        with open('./Dictionaries/ncit-protein-variants.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Gene'] == gene:
                    variant = row['Protein Variant']
                    variants.append(variant)

        random_variant = random.choice(variants)
        variant = {
            'Gene': gene,
            'GeneMutation': random_variant + ' ' + fake.mutation(),
            'VariantAlleleFraction': f'{round(random.uniform(1.0, i), 2)}%'
        }
        svariants_uks.append(variant)
        if i <= 10.0:
            i = 10.0
        else:
            i -= 5.0
    for _ in range(germline_count):
        variants = []
        gene = fake.gene()
        with open('./Dictionaries/ncit-protein-variants.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Gene'] == gene:
                    variant = row['Protein Variant']
                    variants.append(variant)

        random_variant = random.choice(variants)
        variant = {
            'Gene': gene,
            'GeneMutation': random_variant + ' ' + fake.mutation(),
            'Condition': fake.word()
        }
        gvariants_uks.append(variant)
        if i <= 10.0:
            i = 10.0
        else:
            i -= 5.0
    return { "Somatic": svariants_uks,
            "Germline": gvariants_uks}

def generate_genomic_details():
    genomic_details_spa = []
    spa1 = copy.deepcopy(spa)
    for i in range(len(spa1)):
        gene = spa1[i]['Gene']
        # find the description of the gene
        description = descriptions.get(gene, "No description available")
        if description == "No description available":
            description = random.choice(list(descriptions.values()))
        spa1[i]['description'] = description
        genomic_details_spa.append(spa1[i])
        
    genomic_details_sbr = []
    sbr1 = copy.deepcopy(sbr)    
    for i in range(len(sbr1)):
        gene = sbr1[i]['Gene']
        # find the description of the gene
        description = descriptions.get(gene, "No description available")
        if description == "No description available":
            description = random.choice(list(descriptions.values()))
        sbr1[i]['description'] = description
        genomic_details_sbr.append(sbr1[i])
    
    return {
        "Somatic Variant Details - Potentially Actionable": genomic_details_spa,
        "Somatic Variant Details - Biologically Relevant": genomic_details_sbr
    }

def generate_tmb():
    status_options = ['High', 'Stable', 'Equivocal']
    status = random.choice(status_options)
    tmb = {
        'marker_name': "Tumor Mutational Burden",
        'TmbValue': f'{random.randint(1, 50)} m/Mb',
        'Tmbpercentile': f'{random.randint(1, 100)}%',
        'Status type': "Microsatellite Instability Status",
        'statusvalue': status,
    }
    return tmb

def generate_other_details():
    return {
        "ReportId": str(fake.random_int(min=1000, max=9999)),
        "ReportDate": str(fake.date_between(start_date=cdate1, end_date=cdate1+(timedelta(days=10)))),
        "SignedBy": doctor,
        "Supervisor": " ".join(["Dr.", fake.name()])
    }

json_file=f'gr_{sys.argv[1]}.json'
path = './synthetic_data/'+json_file
gr = {}

gr['patient'] = generate_patient_details()
gr['specimen'] = generate_specimen_details()
gr['genomic variants'] = generate_genomic_variants()
gr['immunotherapy markers'] = [generate_tmb()]
# keeping therapies and clinical trials as static data for now
gr['FDA-Approved Therapies'] = {
        "Current Diagnosis": [
            {
                "Mechanism": "KRAS G12C Inhibitor",
                "Medication": "Sotorasib",
                "Recommendations": [
                    "NCCN, Consensus, Non-Small Cell Lung Cancer",
                    "MSK OncoKB, Level 1"
                ],
                "Relevant Mutation": "KRASp.G12C G12C-GOF"
            },
        ],
        "Other Indications": [
            {
                "Mechanism": "KRAS G12C Inhibitor",
                "Medication": "Sotorasib",
                "Recommendations": [
                    "NCCN, Consensus, Non-Small Cell Lung Cancer",
                    "MSK OncoKB, Level 1"
                ],
                "Relevant Mutation": "KRASp.G12C G12C-GOF"
            }
        ]
    }
gr['Additional Indicators'] = [
        {
            "description": "Unfavorable Prognosis",
            "therapy":"NCCN, Consensus, Non-Small Cell Lung Cancer",
            "mutation": "KRASp.G12C Gain-of-function"
        }
    ]
gr['Clinical trials'] = [
        {
            "description": "A Study of VS-6766 v. VS-6766 + Defactinib in Recurrent G12V, Other KRAS and BRAF Non- Small Cell Lung Cancer ",
            "phase": "Phase 2",
            "mutations": ["KRAS"]
        },
        {
            "description": "A Phase 1/2 Study of MRTX849 in Patients With Cancer Having a KRAS G12C Mutation KRYSTAL-1",
            "phase":"Phase 1/2",
            "mutations": ["KRAS", "STK11"]
        },
        {
            "description": "First-in-human Study of DRP-104 (Sirpiglenastat) as Single Agent and in Combination With Atezolizumab in Patients With Advanced Solid Tumors. (NCT04471415)",
            "phase":"Phase 1/2",
            "mutations": ["NFE2L2","STK11"]
        }
    ]
gr['variants of unknown significance'] = generate_variants_of_unknown_significance()
gr['low coverage regions'] = [fake.gene() for _ in range(random.randint(1, 3))]
gr['genomic variants details'] = generate_genomic_details()
gr['clinical history'] = {"Date": str(fake.date_between(start_date=cdate1-fake.time_delta(timedelta(days=10)), end_date=cdate1)),}
gr['other'] = generate_other_details()

with open(path, 'w') as f:
    json.dump(gr, f, indent=4)
    
print(json_file)

