import json
from find import find_in_json, find_all_in_json
import sys
from datetime import datetime

# read the json file
path = f'./synthetic_data2/gr2_{sys.argv[1]}.json'
with open(path) as f:
    data = json.load(f)

def get_patient_info():
    # find the patient information key by key in the json file
    patient_info = {}
    patient_info['Patient ID'] = find_in_json(data, 'Caseno') or "N/A"
    patient_info['Patient Name'] = find_in_json(data, 'Name')
    dob = find_in_json(data, 'DOB')
    patient_info['Date of Birth'] = dob
    # caluclate the age based on the date of birth and the current date
    today = datetime.today()
    age = today.year - int(dob[0:4]) - ((today.month, today.day) < (int(dob[5:7]), int(dob[8:])))
    patient_info['Age'] = age
    patient_info['Gender'] = find_in_json(data, 'Sex')
    patient_info['Contact Information'] = find_in_json(data, 'ContactInformation') or "N/A"
    patient_info['Address'] = find_in_json(data, 'Address') or "N/A"
    
    return patient_info

def get_diagnosis_info():
    # find the diagnosis information key by key in the json file
    diagnosis_info = {}
    diagnosis_info['Diagnosis Center'] = find_in_json(data, 'TreatingInstitution') or "N/A"
    diagnosis_info['Doctor Name'] = find_in_json(data, 'Physician')
    diagnosis_info['Accession Number'] = find_in_json(data, 'ReportId') or "N/A"
    diagnosis_info['Date of Diagnosis'] = find_in_json(data, 'Date') or "N/A"
    diagnosis_info['Date of Report Issuance'] = find_in_json(data, 'ReportDate') or "N/A"
    diagnosis_info['CLIA Number'] = find_in_json(data, 'MedicalHistory') or "N/A"
    diagnosis_info['Laboratory Medical Director '] = find_in_json(data, 'Supervisor') or "N/A"
    diagnosis_info['Method of Analysis'] = list(find_all_in_json(data, 'Method')) or "N/A"
    diagnosis_info['Pipeline Version (Report Version)'] = find_in_json(data, 'PipelineVersion') or "N/A"
    
    return diagnosis_info

def get_cancer_info():
    # find the cancer information key by key in the json file
    cancer_info = {}
    cancer_info['Cancer Type'] = find_in_json(data, 'Diagnosis')
    cancer_info['Cancer Stage'] = find_in_json(data, 'CancerStage') or "Not explicitly stated"
    cancer_info['Cancer Grade'] = find_in_json(data, 'CancerGrade') or "Not explicitly stated"
    cancer_info['Cancer Location in the Body'] = find_in_json(data, 'primary_tumor_site') or "Not explicitly stated"
    # tumor = find_in_json(data, 'Tumor specimen')
    # normal = find_in_json(data, 'Normal specimen')
    cancer_info['Tumor Specimen Source'] = find_in_json(data, 'specimen_site') or "N/A"
    cancer_info['Tumor Percentage in Sample'] = find_in_json(data, 'TumorPercentage') or "N/A"
    cancer_info['Normal Specimen Source'] = find_in_json(data, 'normal_specimen_site') or "N/A"
    cancer_info['Date of Tumor Sample Collection'] = find_in_json(data, 'CollectedDate')
    cancer_info['Date Tumor Sample Received'] = find_in_json(data, 'ReceivedDate')
    cancer_info['Date of Normal Sample Collection'] = "N/A"
    cancer_info['Date Normal Sample Received'] = "N/A"
    
    return cancer_info

def get_biomarkers():
    # find the biomarkers information key by key in the json file
    General_Biomarkers = {}
    gb = find_in_json(data, 'Genomic Signatures')
    General_Biomarkers['Microsatellite Instability (MSI)'] = gb[0]['Result']
    General_Biomarkers['Tumor Mutational Burden (TMB)'] = gb[1]['Result']
    General_Biomarkers['Tumor Mutational Burden Percentile'] = "N/A"
    General_Biomarkers['Loss of Heterozygosity (LOH)'] = gb[2]['Result']
    MMR = []
    PDL1 = []
    # Check in "Relevant Biomarkers"
    if "Relevant Biomarkers" in data:
        for biomarker in data["Relevant Biomarkers"]:
            if biomarker.get("BioMarker") == "Mismatch repair status":
                MMR.append(biomarker.get("Result"))
            elif  biomarker.get("BioMarker") == "PD-L1(SP142)":
                PDL1.append(biomarker.get("Result"))
    General_Biomarkers['Mismatch Repair (MMR) Status'] = MMR if MMR else "N/A"
    General_Biomarkers['PDL1 Expression'] = PDL1 if PDL1 else "N/A"
    General_Biomarkers['EBV (Epstein-Barr Virus) Status'] = find_in_json(data, 'EBV') or "N/A"
    General_Biomarkers['Other Immunotherapy Markers'] = find_in_json(data, 'OtherImmunotherapyMarkers') or "N/A"
    General_Biomarkers['Low-Coverage Regions (Indeterminate Genes)'] = find_in_json(data, 'Genes Tested with indeterminate results') or []
    
    # Extract gene mutations
    Gene_Mutations = []

    # Get "pathogenic" mutations
    pathogenic = find_in_json(data, 'Genes Tested with Pathogenic Alterations')
    for variant in pathogenic:
        mutation = {
            'Gene Name': variant['Gene'],
            'DNA Mutation Description': variant['DNA Alteration'],
            'Protein Variant': variant['Protien Alteration'],
            'Mutation Effect': "N/A",
            'Functional Impact': "N/A",
            'Exon Number': variant.get('Exon', "N/A"),
            'Variant Allele Fraction': variant['Allele Frequency %'],
            'Transcript ID': variant.get('TranscriptID', "N/A"),
            'Somatic or Germline': "N/A",
            'Potentially Actionable or Biologically Relevant': "N/A",
            'Analyte': variant.get('Analyte', "DNA"),
            'Method of Detection ': variant.get('Method', "N/A"),
            'Pathogenicity': variant.get('Variant Interpretation', "N/A"),
            'Pertinent Negative Results': variant.get('Pertinent Negatives', "N/A")
        }
        Gene_Mutations.append(mutation)
    
    relevant_biomarkers = find_in_json(data, 'Relevant Biomarkers')
    # Filter the biomarkers whose analyte is not 'Protien'
    filtered_biomarkers = [biomarker for biomarker in relevant_biomarkers if biomarker['Analyte'] != 'Protien']
    
    for item in filtered_biomarkers:
        mutation = {
            'Gene Name': item['BioMarker'],
            'DNA Mutation Description': item.get('DNA Alteration', "N/A"),
            'Protein Variant': item.get('Protien Alteration', "N/A"),
            'Mutation Effect': item['Result'],
            'Functional Impact': "N/A",
            'Exon Number': item.get('Exon', "N/A"),
            'Variant Allele Fraction': item.get('Allele Frequency %', "N/A"),
            'Transcript ID': item.get('TranscriptID', "N/A"),
            'Somatic or Germline': "N/A",
            'Potentially Actionable or Biologically Relevant': "N/A",
            'Analyte': item.get('Analyte', "DNA"),
            'Method of Detection ': item.get('Method', "N/A"),
            'Pathogenicity': item.get('Variant Interpretation', "N/A"),
            'Pertinent Negative Results': item.get('Pertinent Negatives', "N/A")
        }
        Gene_Mutations.append(mutation)

    # # Get "Somatic - Biologically Relevant" mutations
    # biologically_relevant = find_in_json(data, 'genomic variants')['Somatic - Biologically Relevant']
    # for variant in biologically_relevant:
    #     Gene_Mutation = variant['GeneMutation'].split(' ')
    #     mutation = {
    #         'Gene Name': variant['Gene'],
    #         'DNA Mutation Description': variant['DNA Alteration'],
    #         'Protein Variant': Gene_Mutation[0],
    #         'Mutation Effect': Gene_Mutation[1][0:-4],
    #         'Functional Impact': Gene_Mutation[1][-3:],
    #         'Exon Number': variant.get('ExonNumber', "N/A"),
    #         'Variant Allele Fraction': variant['VariantAlleleFraction'],
    #         'Transcript ID': variant.get('TranscriptID', "NM_001011645"),
    #         'Somatic or Germline': 'Somatic',
    #         'Potentially Actionable or Biologically Relevant': 'Biologically Relevant',
    #         'Analyte': variant.get('Analyte', "DNA"),
    #         'Method of Detection ': variant.get('Method', "N/A"),
    #         'Pathogenicity': variant.get('Pathogenicity', "N/A"),
    #         'Pertinent Negative Results': variant.get('Pertinent Negatives', "N/A")
        # }
        # Gene_Mutations.append(mutation)
    
    immunochemistry_markers = find_in_json(data, 'Immunohistochemistry results')
    imo = []
    for item in immunochemistry_markers:
        imo.append(
            {
                'Biomarker Name': item['Biomarker'],
                'Number of Stained Cells': "N/A",
                'Percentage of Expression': ' '.join(item['Result'].split(' ')[1:]),
                'Interpretation': item['Result'].split(' ')[0][:-1]
            }
        )
    
    
    return {
        'General Biomarkers': General_Biomarkers,
        'Gene Mutations': Gene_Mutations,
        'Immunochemistry Biomarkers': imo
    }

def get_fda_therapies():
    # get the FDA-approved therapies information
    fda_therapies_curr_diag = []
    
    current_diagnosis = find_in_json(data, 'Results with Therapy association')
    for item in current_diagnosis:
        therapy_type = "immunotherapy" if item['Biomarker'] == "TMB" else "targeted therapy"
        x = {'Therapy Name' : ', '.join(item['Therapy association'][1:]),
        'Therapy Type' : item.get('Therapy Type', therapy_type),
        'Evidence Source' :"N/A",
        'Associated Biomarker' : {
            "Biomarker Name": item['Biomarker'],
            "Biomarker level": item['Biomarker_level'],
            "Positively/Negatively Associated": item['Therapy association'][0]
        }
        }
        fda_therapies_curr_diag.append(x)
    
    return {
        'FDA-Approved Therapies for Current Diagnosis': fda_therapies_curr_diag,
        'FDA-Approved Therapies for Other Indications': []
    }

def get_clinical_trials():
    # find the clinical trial information
    clinical_trials = []
    
    trials = find_in_json(data, 'Chemotherapy clinical trials')
    for trial in trials:
        trial_info = {
            'Trial Title': trial['Drug class'],
            'Clinical Trial ID': trial.get('trial_id', "N/A"),
            'Phase of Trial': "N/A",
            'Trial Location': "N/A",
            'Therapy Type': "Chemotherapy",
            'Medication': ', '.join(trial['Investigational agents']),
            'Associated Mutations': [trial['Biomarker']]
            # 'Associated Mutations': [x + ' mutation' for x in trial['mutations']]
            
        }
        clinical_trials.append(trial_info)
        
    trials = find_in_json(data, 'Targeted therapy clinical trials')
    for trial in trials:
        trial_info = {
            'Trial Title': trial['Drug class'],
            'Clinical Trial ID': trial.get('trial_id', "N/A"),
            'Phase of Trial': "N/A",
            'Trial Location': "N/A",
            'Therapy Type': "Targeted therapy",
            'Medication': ', '.join(trial['Investigational agents']),
            'Associated Mutations': [trial['Biomarker']]
            # 'Associated Mutations': [x + ' mutation' for x in trial['mutations']]
            
        }
        clinical_trials.append(trial_info)
        
    return clinical_trials

def get_variants_of_unknown_significance():
    # find variants of unknown significance (VUS)
    vus = []
    
    somatic_variants = find_in_json(data, 'Gene variants of unknown significance')
    for variant in somatic_variants:
        vus_info = {
            'Gene Name': variant['Gene'],
            'DNA Alteration': variant['DNA Alteration'],
            'Protein Variant': variant['Protien Alteration'],
            'Mutation Effect': "N/A",
            'Variant Allele Fraction': variant['Allele Frequency %'],
            'Exon Number': variant.get('Exon', "N/A"),
            'Transcript ID': variant.get('TranscriptID', "N/A"),
            'Functional Impact': variant.get('GeneMutation', "N/A"),
            'Somatic or Germline': "N/A"
        }
        vus.append(vus_info)
    
    return vus

def get_additional_info():
    # find additional information
    additional_info = {}
    add = find_in_json(data, 'Additional Indicators')[0]
    additional_info['Prognostic Markers'] = {
        'description': add['description'],
        'recommendation': add['therapy'],
        'biomarker': add['mutation']
    }
    
    return additional_info

json_file=f'fgr2_{sys.argv[1]}.json'
path = './formatted ground truth 2/'+json_file
gr = {}

gr['Patient Information'] = get_patient_info()
gr['Diagnosis Information'] = get_diagnosis_info()
gr['Cancer Information'] = get_cancer_info()
gr['Biomarkers'] = get_biomarkers()
gr['Therapeutic Information'] = get_fda_therapies()
gr['Clinical Trials'] = get_clinical_trials()
gr['Variants of Unknown Significance (VUS)'] = get_variants_of_unknown_significance()
gr['Additional Indicators'] = []


# write the formatted ground truth to a json file
with open(path, 'w') as f:
    json.dump(gr, f, indent=4)