import random
import json
from faker import Faker
from faker.providers import BaseProvider
from datetime import timedelta
import csv
import sys
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
    """
    Generate patient details
    """
    patient_details = {
        'Name': fake.name(),
        "DOB": str(fake.date_of_birth(minimum_age=18, maximum_age=100)),
        "Sex": random.choice(['Male', 'Female']),
        "Caseno": str(fake.random_int(min=1000, max=9999)),
        "Diagnosis": random_diagnosis,
        "Physician": " ".join(["Dr.", doctor])
    }
    return patient_details


cdate1 = fake.date_between(start_date='-1y', end_date='today')
def generate_specimen_details():
    specimens = []
    with open('./Dictionaries/cancer-specimensite.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['cancer'] == cancer_type:
                specimen = row['specimen site']
                specimens.append(specimen)
                
    random_specimen = random.choice(specimens)
    specimen_details = {
        "primary_tumor_site": cancer_type.split()[0],
        "specimen_site": random_specimen,
        "specimen_ID": str(fake.random_int(min=1000, max=9999)),
        "CollectedDate": str(cdate1),
        "ReceivedDate":  str(fake.date_between(start_date=cdate1, end_date=cdate1+fake.time_delta(timedelta(days=10)))),
        "Pathological Diagnosis": "Left breast, central, 12:00, suspicious mass, 12-gauge core needle biopsy: Infiltrating moderately-differentiated mammary carcinoma, grade 2, Nottingham score 6 (architectural grade 3, nuclear grade 2, mitotic figures 1).",
        "Dissection Information": "Molecular testing of this specimen was performed after harvesting of targeted tissues with an approved manual microdissection technique. Candidate slides were examined under a microscope and areas containing tumor cells (and separately normal cells, when necessary for testing) were circled. A laboratory technician harvested targeted tissues for extraction from the marked areas using a dissection microscope."
    }
    return specimen_details

def generate_gene_details():
    count = random.randint(3, 6)
    i = 40
    gene_detail_list = []
    for _ in range(count):
        gene = fake.gene()
        variants = []
        with open('./Dictionaries/ncit-protein-variants.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Gene'] == gene:
                    variant = row['Protein Variant']
                    variants.append(variant)

        random_variant = random.choice(variants)
        
        alt_variants = []
        with open('./Dictionaries/ncit-gene-mutations.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Gene'] == gene:
                    alt_variant = row['DNA Alteration']
                    alt_variants.append(alt_variant)
            if alt_variants == []:
                alt_variants = row['DNA Alteration']
        random_alt_variant = random.choice(alt_variants)
        gene_detail = {
            "Gene": fake.gene(),
            "Method": "Seq",
            "Analyte": "DNA tumor",
            "Variant Interpretation": random.choice(["Pathogenic", "Likely Pathogenic", "Benign", "Likely Benign"]),
            "Protien Alteration": random_variant,
            "Exon": random.randint(2, 20),
            "DNA Alteration": random_alt_variant,
            "Allele Frequency %": f'{round(random.uniform(1.0, i), 2)}'
        }
        i = i - 5
        gene_detail_list.append(gene_detail)
    return gene_detail_list

def generate_gene_uk_details():
    count = random.randint(3, 6)
    i = 30
    gene_detail_list = []
    for _ in range(count):
        gene = fake.gene()
        variants = []
        with open('./Dictionaries/ncit-protein-variants.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Gene'] == gene:
                    variant = row['Protein Variant']
                    variants.append(variant)
            
        random_variant = random.choice(variants)
        
        alt_variants = []
        with open('./Dictionaries/ncit-gene-mutations.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Gene'] == gene:
                    alt_variant = row['DNA Alteration']
                    alt_variants.append(alt_variant)
            if alt_variants == []:
                alt_variants = row['DNA Alteration']
        random_alt_variant = random.choice(alt_variants)
        gene_detail = {
            "Gene": fake.gene(),
            "Method": "Seq",
            "Analyte": "DNA tumor",
            "Variant Interpretation": "Variant of uncertain significance",
            "Protien Alteration": random_variant,
            "Exon": random.randint(2, 20),
            "DNA Alteration": random_alt_variant,
            "Allele Frequency %": f'{round(random.uniform(1.0, i), 2)}'
        }
        i = i - 5
        gene_detail_list.append(gene_detail)
    return gene_detail_list
    
def generate_gene_indeterminate_list():
    count = random.randint(3, 6)
    l = []
    for _ in range(count):
        l.append(fake.gene())

    return l

def generate_relevant_biomarkers():
    analytes = ['Protien', 'DNA-Tumor', 'RNA-Tumor']
    p_biomarkers = ['Mismatch repair status', 'ER', 'AR', 'PR', 'PD-L1(SP142)']
    status = ['Positive', 'Negative']
    count = random.randint(3,10)
    relevant_biomarker_list = []
    for _ in range(count):
        analyte = random.choice(analytes)
        if analyte == 'Protien':
            method = "IHC"
            biomarker = random.choice(p_biomarkers)
            result = random.choice(status) + "| "+str(random.randint(1,3))+"+, "+str(random.randint(1,100))+"%" 
        else:
            method = "Seq"
            biomarker = fake.gene()
            result = random.choice(['Mutation not detected', 'Fusion not detected', 'Stable'])
        relevant_biomarker = {
            "BioMarker": biomarker,
            "Method": method,
            "Analyte": analyte,
            "Result": result
        }
        relevant_biomarker_list.append(relevant_biomarker)
    return relevant_biomarker_list
    
tmb_val = random.randint(5, 20)
if tmb_val < 13:
    tmb_status = 'Low'
else:
    tmb_status = 'High'        
def generate_gene_sig_details():
    # Microsatellite instability
    gene_sig_list = []
    msi = {
        "BioMarker": "Microsatellite instability",
        "Method": "Seq",
        "Analyte": "DNA tumor",
        "Result": random.choice(['High', 'Low', 'Equivocal'])
    }      
    gene_sig_list.append(msi)
    
    # Tumor mutational burden
    
    tmb = {
        "BioMarker": "Tumor mutational burden",
        "Method": "Seq",
        "Analyte": "DNA tumor",
        "Result": str(tmb_val) + " mutations/Mb " + tmb_status
    }
    gene_sig_list.append(tmb)
    
    # genomic loss of heterozygosity
    glh_val = random.randint(1, 40)
    if glh_val < 16:
        status = 'Low'
    else:
        status = 'High'
    glh = {
        "BioMarker": "Genomic loss of heterozygosity (LOH)",
        "Method": "Seq",
        "Analyte": "DNA tumor",
        "Result": status + " - " + str(glh_val) + "% of tested genomic segments exhibit LOH"
    }
    gene_sig_list.append(glh)
    
    return gene_sig_list
  
def generate_immunohistochemistry_results():
    biomarker_list = ['AR', 'ER', 'ERBB2', 'PR', 'PD-L1(SP142)', 'PMS2', 'MLH1', 'MSH2', 'MSH6', 'PTEN']
    n = random.randint(3, 10)
    random_biomarkers = random.sample(biomarker_list, n)
    res = []
    for i in range(n):
        ele = {
            "Biomarker": random_biomarkers[i],
            "Result": random.choice(['Positive', 'Negative']) + "| "+str(random.randint(1,3))+"+, "+str(random.randint(1,100))+"%"
        }
        res.append(ele)
    return res
    
json_file=f'gr_{sys.argv[1]}.json'
path = './synthetic_data2/'+json_file
gr = {}

gr['Patient'] = generate_patient_details()
gr['specimen information'] = generate_specimen_details()
gr['Results with Therapy association'] = [
        {
            "Biomarker": "ER",
            "Method": "IHC",
            "Analyte": "protein",
            "Result": "Positive | 3+, 100%",
            "Therapy association": ["BENEFIT", "abemaciclib", "palbociclib", "ribociclib", "endocrine", "therapy", "everolimus"],
            "Biomarker level": "level 2"
        },
        {
            "Biomarker": "PR",
            "Method": "IHC",
            "Analyte": "protein",
            "Result": "Positive | 2+, 95%",
            "Therapy association": [
                "BENEFIT",
                "abemaciclib",
                "palbociclib",
                "ribociclib",
                "endocrine therapy"
            ],
            "Biomarker_level": "level 2"
        },
        {
            "Biomarker": "TMB",
            "Method": "seq",
            "Analyte": "DNA tumor",
            "Result": str(tmb_val) + " m/Mb " + tmb_status,
            "Therapy association": [
                "BENEFIT",
                "pembrolizumab"
            ],
            "Biomarker_level": "level 2"
        },
        {
            "Biomarker": "ERBB2",
            "Method": "IHC",
            "Analyte": "Protien",
            "Result": "Negative | 0",
            "Therapy association": [
                "LACK OF BENEFT",
                "trastuzumab",
                "ado-trastuzumab emtansine",
                "pertuzumab",
                "fam-trastuzumab deruxtecan-nxki",
                "lapatinib",
                "neratinib",
                "tucatinib"
            ],
            "Biomarker_level": "level 1"
        }
    ]
gr['Relevant Biomarkers'] = generate_relevant_biomarkers()
gr['Genomic Signatures'] = generate_gene_sig_details()
gr['Genes Tested with Pathogenic Alterations'] = generate_gene_details()
gr['Gene variants of unknown significance'] = generate_gene_uk_details()
gr['Immunohistochemistry results'] = generate_immunohistochemistry_results()
gr['Genes Tested with indeterminate results'] = generate_gene_indeterminate_list()
gr['Chemotherapy clinical trials'] = [
        {
            "Drug class": "Anti hormonal therapy",
            "Biomarker": "ER",
            "Method": "IHC",
            "Analyte": "protein",
            "Investigational agents": ["anastrazole", "letrozole", "exemestane", "fulvestrant", "tamoxifen", "goserelin", "leuprolide"]
        },
        {
            "Drug class": "Anti hormonal therapy",
            "Biomarker": "PR",
            "Method": "IHC",
            "Analyte": "protein",
            "Investigational agents": [
                "anastrazole",
                "letrozole",
                "exemestane",
                "fulvestrant",
                "tamoxifen",
                "goserelin",
                "leuprolide"
            ]
        },
        {
            "Drug class": "Anti inflammatory agents",
            "Biomarker": "PIK3CA",
            "Method": "NGS",
            "Analyte": "DNA tumor",
            "Investigational agents": ["aspirin"]
        }
    ]
gr['Targeted therapy clinical trials'] = [
        {
            "Drug class": "Akt inhibitors",
            "Biomarker": "ARID1A",
            "Method": "NGS",
            "Analyte": "DNA tumor",
            "Investigational agents": ["AZD5363", "MK-2206", "ipataserib"]
        },
        {
            "Drug class": "immunomodulatory agents",
            "Biomarker": "TMB",
            "Method": "NGS",
            "Analyte": "DNA tumor",
            "Investigational agents": [
                "avelumab",
                "atezolizumab",
                "durvalumab",
                "ipilimumab",
                "nivolumab",
                "pembrolizumab"
            ]
        },
        {
            "Drug class": "PARP inhibitors",
            "Biomarker": "NBN",
            "Method": "NGS",
            "Analyte": "DNA tumor",
            "Investigational agents": ["BGB-290", "BMN-673", "olaparib", "rucaparib", "talazoparib"]
        },
        {
            "Drug class": "Akt/mTor inhibitors",
            "Biomarker": "PIK3CA",
            "Method": "NGS",
            "Analyte": "DNA tumor",
            "Investigational agents": [
                "AZD5363",
                "BYL719",
                "MK-2206",
                "ipataserib",
                "everolimus",
                "temsirolimus"
            ]
        }
    ]
with open(path, 'w') as f:
    json.dump(gr, f, indent=4)
    
print(json_file)