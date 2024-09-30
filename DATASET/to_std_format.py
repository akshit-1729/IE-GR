import json
from find import find_in_json
import sys
from datetime import datetime

# read the json file
path = f'./synthetic_data/gr_{sys.argv[1]}.json'
with open(path) as f:
    data = json.load(f)

def get_patient_info():
    # find the patient information key by key in the json file
    patient_info = {}
    patient_info['Patient ID'] = find_in_json(data, 'Patient ID') or "N/A"
    patient_info['Patient Name'] = find_in_json(data, 'Name')
    dob = find_in_json(data, 'DateOfBirth')
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
    diagnosis_info['Diagnosis Center'] = find_in_json(data, 'TreatingInstitution')
    diagnosis_info['Doctor Name'] = find_in_json(data, 'Physician')
    diagnosis_info['Accession Number'] = find_in_json(data, 'ReportId')
    diagnosis_info['Date of Diagnosis'] = find_in_json(data, 'Date')
    diagnosis_info['Date of Report Issuance'] = find_in_json(data, 'ReportDate')
    diagnosis_info['CLIA Number'] = find_in_json(data, 'MedicalHistory') or "14D2114007"
    diagnosis_info['Laboratory Medical Director '] = find_in_json(data, 'Supervisor')
    diagnosis_info['Method of Analysis'] = find_in_json(data, 'Method') or "Not explicitly stated, assumed NGS"
    diagnosis_info['Pipeline Version (Report Version)'] = find_in_json(data, 'PipelineVersion') or "3.2.0"
    
    return diagnosis_info

def get_cancer_info():
    # find the cancer information key by key in the json file
    cancer_info = {}
    cancer_info['Cancer Type'] = find_in_json(data, 'Diagnosis')
    cancer_info['Cancer Stage'] = find_in_json(data, 'CancerStage') or "Not explicitly stated"
    cancer_info['Cancer Grade'] = find_in_json(data, 'CancerGrade') or "Not explicitly stated"
    cancer_info['Cancer Location in the Body'] = find_in_json(data, 'BodyPart') or "Not explicitly stated"
    tumor = find_in_json(data, 'Tumor specimen')
    normal = find_in_json(data, 'Normal specimen')
    cancer_info['Tumor Specimen Source'] = tumor['source']
    cancer_info['Tumor Percentage in Sample'] = tumor['TumorPercentage']
    cancer_info['Normal Specimen Source'] = normal['source']
    cancer_info['Date of Tumor Sample Collection'] = tumor['CollectedDate']
    cancer_info['Date Tumor Sample Received'] = tumor['ReceivedDate']
    cancer_info['Date of Normal Sample Collection'] = normal['CollectedDate']
    cancer_info['Date Normal Sample Received'] = normal['ReceivedDate']
    
    return cancer_info

def get_biomarkers():
    # find the biomarkers information key by key in the json file
    General_Biomarkers = {}
    immunotherapy_markers = find_in_json(data, 'immunotherapy markers')[0]
    General_Biomarkers['Microsatellite Instability (MSI)'] = immunotherapy_markers['statusvalue']
    General_Biomarkers['Tumor Mutational Burden (TMB)'] = immunotherapy_markers['TmbValue']
    General_Biomarkers['Tumor Mutational Burden Percentile'] = immunotherapy_markers.get('Tmbpercentile', "N/A")
    General_Biomarkers['Loss of Heterozygosity (LOH)'] = find_in_json(data, 'LOH') or "N/A"
    General_Biomarkers['Mismatch Repair (MMR) Status'] = find_in_json(data, 'MMR') or "N/A"
    General_Biomarkers['PDL1 Expression'] = find_in_json(data, 'PDL1') or "N/A"
    General_Biomarkers['EBV (Epstein-Barr Virus) Status'] = find_in_json(data, 'EBV') or "N/A"
    General_Biomarkers['Other Immunotherapy Markers'] = find_in_json(data, 'OtherImmunotherapyMarkers') or "N/A"
    General_Biomarkers['Low-Coverage Regions'] = find_in_json(data, 'low coverage regions') or []
    
    # Extract gene mutations
    Gene_Mutations = []

    # Get "Somatic - Potentially Actionable" mutations
    potentially_actionable = find_in_json(data, 'genomic variants')['Somatic - Potentially Actionable']
    for variant in potentially_actionable:
        Gene_Mutation = variant['GeneMutation'].split(' ')
        mutation = {
            'Gene Name': variant['Gene'],
            'DNA Mutation Description': variant['DNA Alteration'],
            'Protein Variant': Gene_Mutation[0],
            'Mutation Type': Gene_Mutation[1][0:-4],
            'Functional Impact': Gene_Mutation[1][-3:],
            'Exon Number': variant.get('ExonNumber', "N/A"),
            'Variant Allele Fraction': variant['VariantAlleleFraction'],
            'Transcript ID': variant.get('TranscriptID', "N/A"),
            'Somatic or Germline': 'Somatic',
            'Potentially Actionable or Biologically Relevant': 'Potentially Actionable',
            'Analyte': variant.get('Analyte', "DNA"),
            'Method of Detection ': variant.get('Method', "N/A"),
            'Pathogenicity': variant.get('Pathogenicity', "N/A"),
            'Pertinent Negative Results': variant.get('Pertinent Negatives', "N/A")
        }
        Gene_Mutations.append(mutation)
    
    # Get "Somatic - Biologically Relevant" mutations
    biologically_relevant = find_in_json(data, 'genomic variants')['Somatic - Biologically Relevant']
    for variant in biologically_relevant:
        Gene_Mutation = variant['GeneMutation'].split(' ')
        mutation = {
            'Gene Name': variant['Gene'],
            'DNA Mutation Description': variant['DNA Alteration'],
            'Protein Variant': Gene_Mutation[0],
            'Mutation Type': Gene_Mutation[1][0:-4],
            'Functional Impact': Gene_Mutation[1][-3:],
            'Exon Number': variant.get('ExonNumber', "N/A"),
            'Variant Allele Fraction': variant['VariantAlleleFraction'],
            'Transcript ID': variant.get('TranscriptID', "N/A"),
            'Somatic or Germline': 'Somatic',
            'Potentially Actionable or Biologically Relevant': 'Biologically Relevant',
            'Analyte': variant.get('Analyte', "DNA"),
            'Method of Detection ': variant.get('Method', "N/A"),
            'Pathogenicity': variant.get('Pathogenicity', "N/A"),
            'Pertinent Negative Results': variant.get('Pertinent Negatives', "N/A")
        }
        Gene_Mutations.append(mutation)
        
    pert_neg = find_in_json(data, 'genomic variants')['Pertinent Negatives']
    for gene in pert_neg:
        mutation = {
            'Gene Name': gene,
            'DNA Mutation Description': "N/A",
            'Protein Variant': "N/A",
            'Mutation Type': "N/A",
            'Functional Impact': "N/A",
            'Exon Number': "N/A",
            'Variant Allele Fraction': "N/A",
            'Transcript ID': "N/A",
            'Somatic or Germline': 'N/A',
            'Potentially Actionable or Biologically Relevant': 'N/A',
            'Analyte': "DNA",
            'Method of Detection ': "N/A",
            'Pathogenicity': "N/A",
            'Pertinent Negative Results': 'Pertinent Negatives'
        }
        Gene_Mutations.append(mutation)
    
    immunochemistry_markers = []
    
    return {
        'General Biomarkers': General_Biomarkers,
        'Gene Mutations': Gene_Mutations,
        'Immunochemistry Biomarkers': immunochemistry_markers
    }

def get_fda_therapies():
    # get the FDA-approved therapies information
    l1 = []
    l2 = []
    fda_therapies_curr_diag = {}
    fda_therapies_oth_diag = {}
    
    current_diagnoses = find_in_json(data, 'FDA-Approved Therapies')['Current Diagnosis']
    for current_diagnosis in current_diagnoses:
        fda_therapies_curr_diag['Therapy Name'] = current_diagnosis['Mechanism']
        fda_therapies_curr_diag['Therapy Type'] = current_diagnosis.get('Therapy Type', "targeted therapy")
        fda_therapies_curr_diag['Medication'] = current_diagnosis['Medication']
        fda_therapies_curr_diag['Evidence Source'] = ', '.join(current_diagnosis['Recommendations'])
        fda_therapies_curr_diag['Associated Biomarker'] = {
            "Biomarker Name": current_diagnosis['Relevant Mutation'],
            "Positively/Negatively Associated": current_diagnosis.get('Association', "N/A")
        }
        l1.append(fda_therapies_curr_diag)
    
    other_diagnoses = find_in_json(data, 'FDA-Approved Therapies')['Other Indications']
    for other_diagnosis in other_diagnoses:
        fda_therapies_oth_diag['Therapy Name'] = other_diagnosis['Mechanism']
        fda_therapies_oth_diag['Therapy Type'] = current_diagnosis.get('Therapy Type', "targeted therapy")
        fda_therapies_oth_diag['Medication'] = other_diagnosis['Medication']
        fda_therapies_oth_diag['Evidence Source'] = ', '.join(current_diagnosis['Recommendations'])
        fda_therapies_oth_diag['Associated Biomarker'] = {
            "Biomarker Name": other_diagnosis['Relevant Mutation'],
            "Positively/Negatively Associated": other_diagnosis.get('Association', "N/A")
        }
        l2.append(fda_therapies_oth_diag)
    
    return {
        'FDA-Approved Therapies for Current Diagnosis': l1,
        'FDA-Approved Therapies for Other Indications': l2
    }

def get_clinical_trials():
    # find the clinical trial information
    clinical_trials = []
    
    trials = find_in_json(data, 'Clinical trials')
    for trial in trials:
        trial_info = {
            'Trial Title': trial['description'],
            'Clinical Trial ID': trial.get('trial_id', "N/A"),
            'Phase of Trial': trial['phase'],
            'Trial Location': trial.get('location', "City, state - x mi"),
            'Therapy Type': "N/A",
            'Medication' : "N/A",
            'Associated Mutations': trial['mutations']
            # 'Associated Mutations': [x + ' mutation' for x in trial['mutations']]
        }
        clinical_trials.append(trial_info)
    
    return clinical_trials

def get_variants_of_unknown_significance():
    # find variants of unknown significance (VUS)
    vus = []
    
    somatic_variants = find_in_json(data, 'variants of unknown significance')['Somatic']
    for variant in somatic_variants:
        Gene_Mutation = variant['GeneMutation'].split(' ')
        vus_info = {
            'Gene Name': variant['Gene'],
            'DNA Alteration': variant['DNA Alteration'],
            'Protein Variant': Gene_Mutation[0],
            'Mutation Type': Gene_Mutation[1][0:-4],
            'Functional Impact': Gene_Mutation[1][-3:],
            'Variant Allele Fraction': variant['VariantAlleleFraction'],
            'Exon Number': variant.get('ExonNumber', "N/A"),
            'Transcript ID': variant.get('TranscriptID', "NM_001011645"),
            'Somatic or Germline': 'Somatic'
        }
        vus.append(vus_info)
        
    germline_variants = find_in_json(data, 'variants of unknown significance')['Germline']
    for variant in germline_variants:
        Gene_Mutation = variant['GeneMutation'].split(' ')
        vus_info = {
            'Gene Name': variant['Gene'],
            'DNA Alteration': variant['DNA Alteration'],
            'Protein Variant': Gene_Mutation[0],
            'Mutation Type': Gene_Mutation[1][0:-4],
            'Functional Impact': Gene_Mutation[1][-3:],
            'Condition': variant['Condition'],
            'Exon Number': variant.get('ExonNumber', "N/A"),
            'Transcript ID': variant.get('TranscriptID', "NM_001011645"),
            'Somatic or Germline': 'Germline'
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

json_file=f'fgr_{sys.argv[1]}.json'
path = './formatted ground truth/'+json_file
gr = {}

gr['Patient Information'] = get_patient_info()
gr['Diagnosis Information'] = get_diagnosis_info()
gr['Cancer Information'] = get_cancer_info()
gr['Biomarkers'] = get_biomarkers()
gr['Therapeutic Information'] = get_fda_therapies()
gr['Clinical Trials'] = get_clinical_trials()
gr['Variants of Unknown Significance (VUS)'] = get_variants_of_unknown_significance()
gr['Additional Indicators'] = get_additional_info()


# write the formatted ground truth to a json file
with open(path, 'w') as f:
    json.dump(gr, f, indent=4)