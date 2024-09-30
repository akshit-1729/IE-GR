from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from find import find_in_json
import json, sys

file_name = f'./synthetic_data2/doc2_{sys.argv[2]}.pdf'
# open the json file
print(sys.argv[1])
filename = './synthetic_data2/'+sys.argv[1]
with open(filename, 'r') as json_file:
    data = json.load(json_file)

# Function to create the PDF with the desired layout
c = canvas.Canvas(file_name, pagesize=letter)
width, height = letter  # Letter size

def header(c):
    # Header Section
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.steelblue)
    c.drawString(400, height - 50, "Final Report")
    c.setStrokeColor(colors.steelblue)
    c.line(500, height - 25, 500, height - 75)
    # c.drawImage("caris-logo.png", 505, height - 75,65, 55 ,preserveAspectRatio=True, mask='auto')
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.4)
    c.line(35, height - 100, width - 35, height - 100)
    
def footer(c, width):
    # Footer Section
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.lightsteelblue)
    c.rect(35, 35, 540, 20, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.drawString(40, 40, "PATIENT: "+find_in_json(data, 'Name'))
    c.drawString(225, 40, "CASE NUMBER: "+find_in_json(data, 'Caseno'))
    c.drawString(425, 40, "PHYSICIAN: "+find_in_json(data, 'Physician'))
    
       
header(c)

# Patient Section
b_height = height - 120
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(35, b_height, "Patient")
c.setFont("Helvetica", 9)
c.setFillColor(colors.black)
c.drawString(35, height - 140, "Name: "+find_in_json(data, 'Name'))
c.drawString(35, height - 155, "Date of Birth: "+find_in_json(data, 'DOB'))
c.drawString(35, height - 170, "Sex: "+find_in_json(data, 'Sex'))
c.drawString(35, height - 185, "Case Number: "+find_in_json(data, 'Caseno'))
c.drawString(35, height - 200, "Diagnosis: "+find_in_json(data, 'Diagnosis'))

# Specimen Information
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(235, b_height, "Specimen Information")
c.setFont("Helvetica", 9)
c.setFillColor(colors.black)
c.drawString(235, height - 140, "Primary Tumor Site: "+find_in_json(data, 'primary_tumor_site'))
c.drawString(235, height - 155, "Specimen Site: "+ find_in_json(data, 'specimen_site'))
c.drawString(235, height - 170, "Specimen ID: "+find_in_json(data, 'specimen_ID'))
c.drawString(235, height - 185, "Specimen Collected: "+find_in_json(data, 'CollectedDate'))
c.drawString(235, height - 200, "Test Initiated: "+find_in_json(data, 'ReceivedDate'))

# Ordered By Section
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(435, b_height, "Ordered By")

c.setStrokeColor(colors.black)
c.line(35, height - 215, width - 35, height - 215)


## RESULTS WITH THERAPY ASSOCIATION
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(35, b_height - 120, "Results with therapy association")
c.setFont("Helvetica", 9)

# get table data from json file
therapy_association = find_in_json(data, 'Results with Therapy association')
therapy_association_data = []
l = []
inner_style_b = TableStyle([
    ('BACKGROUND', (0,0), (0,-1), colors.green),
    ('TEXTCOLOR', (0,0), (0,-1), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('BACKGROUND', (1,1), (-1,-1), colors.white),
    ('FONTSIZE', (0,0), (-1,-1), 8)
])
inner_style_lb = TableStyle([
    ('BACKGROUND', (0,0), (0,-1), colors.red),
    ('TEXTCOLOR', (0,0), (0,-1), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('BACKGROUND', (1,1), (-1,-1), colors.white),
    ('FONTSIZE', (0,0), (-1,-1), 8)
])
for key, value in therapy_association[0].items():
    l.append(key)
therapy_association_data.append(l)
for item in therapy_association:
    inner_data = []
    l = []
    l1 = []
    for key, value in item.items():
        if key == "Therapy association":
            styles = getSampleStyleSheet()
            style = styles['Normal']
            style.fontSize = 8
            paragraph = Paragraph(value[0], style)
            l1.append(paragraph)
            text = ", ".join(value[1:])
            paragraph = Paragraph(text, style)
            l1.append(paragraph)
            inner_data.append(l1)
            inner_table = Table(inner_data, colWidths=[2 * cm, 5 * cm], rowHeights=[2 * cm])
            if value[0] == "BENEFIT":
                inner_table.setStyle(inner_style_b)
            else:
                inner_table.setStyle(inner_style_lb)
            l.append(inner_table)
        else:    
            l.append(value)
    therapy_association_data.append(l)    

# Create a Table object
table = Table(therapy_association_data, colWidths=[2 * cm, 2 * cm, 2 * cm, 3 * cm, 7 * cm, 3 * cm])
# Define the Table Style
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.steelblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightsteelblue),
    ('GRID', (0, 0), (-1, -1), 1, colors.white),
    # ('SPAN', (0, -1), (-2, -1)), # Span across all but the last column
    ('FONTSIZE', (0, 0), (-1, -1), 8),
])


# Apply the Table Style
table.setStyle(style)
table_width, table_height = table.wrap(200, 500)

table.drawOn(c, 35, height - 250 - table_height)

footer(c, width)

### PAGE 2
c.showPage()
header(c)
b_height = height - 120

## RELEVANT BIOMARKERS
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(35, b_height, "Cancer-Type Relevant Biomarkers")

# get table data from json file
relevant_biomarkers = find_in_json(data, 'Relevant Biomarkers')
relevant_biomarkers_data = []
relevant_biomarkers_data_2 = []
l = []
for key, value in relevant_biomarkers[0].items():
    l.append(key)
relevant_biomarkers_data.append(l)
if len(relevant_biomarkers) > 5:
    relevant_biomarkers_data_2.append(l)
i = 0
for item in relevant_biomarkers:
    l = []
    for key, value in item.items():
        l.append(value)
    if i < 5:
        relevant_biomarkers_data.append(l)
    else:
        relevant_biomarkers_data_2.append(l)
    i = i + 1
    
# Create a Table object
table = Table(relevant_biomarkers_data)
table.setStyle(style)
table_width, table_height = table.wrap(30, 50)

table.drawOn(c, 35, b_height - 15 - table_height)

if len(relevant_biomarkers) > 5:
    table = Table(relevant_biomarkers_data_2)
    table.setStyle(style)
    table_width1, table_height1 = table.wrap(30, 50)
    table.drawOn(c, 35 + 300, b_height - 15 - table_height1)

## GENOMIC SIGNATURES
b_height = b_height - 40 - table_height
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(35, b_height, "Genomic Signatures")

# get table data from json file
genomic_signatures = find_in_json(data, 'Genomic Signatures')
genomic_signatures_data = []
l = []
for key, value in genomic_signatures[0].items():
    l.append(key)
genomic_signatures_data.append(l)
for item in genomic_signatures:
    l = []
    for key, value in item.items():
        l.append(value)
    genomic_signatures_data.append(l)

# Create a Table object
table = Table(genomic_signatures_data)
table.setStyle(style)
table_width, table_height = table.wrap(100, 50)

table.drawOn(c, 35, b_height - 15 - table_height)

### GENES
b_height = b_height - 40 - table_height
c.drawString(35, b_height, "Genes Tested with Pathogenic Alterations or likely Pathogenic Alterations")
c.setFont("Helvetica", 9)
c.setFillColor(colors.black)

# get table data from json file
genes_variants = find_in_json(data, 'Genes Tested with Pathogenic Alterations')
genes_variants_data = []
l = []
for key, value in genes_variants[0].items():
    l.append(key)
genes_variants_data.append(l)
for item in genes_variants:
    l = []
    for key, value in item.items():
        l.append(value)
    genes_variants_data.append(l)
    
# Create a Table object
table = Table(genes_variants_data)
table.setStyle(style)
table_width, table_height = table.wrap(200, 50)

table.drawOn(c, 35, b_height - 15 - table_height)

footer(c, width)

### PAGE 3
c.showPage()
header(c)
b_height = height - 120

## GENE VARIANTS OF UNKNOWN SIGNIFICANCE
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(35, b_height, "Gene Variants of Unknown Significance")

# get table data from json file
gene_variants_uk = find_in_json(data, 'Gene variants of unknown significance')
gene_variants_uk_data = []
l = []
for key, value in gene_variants_uk[0].items():
    l.append(key)
gene_variants_uk_data.append(l)
for item in gene_variants_uk:
    l = []
    for key, value in item.items():
        l.append(value)
    gene_variants_uk_data.append(l)
    
# Create a Table object
table = Table(gene_variants_uk_data)
table.setStyle(style)
table_width, table_height = table.wrap(200, 50)

table.drawOn(c, 35, b_height - 15 - table_height)

## IMMUNOCHEMISTRY
b_height = b_height - 40 - table_height
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(35, b_height, "Immunohistochemistry Results")

# get table data from json file
immunohistochemistry = find_in_json(data, 'Immunohistochemistry results')   
immunohistochemistry_data = []
immunohistochemistry_data_2 = []
l = []
for key, value in immunohistochemistry[0].items():
    l.append(key)
immunohistochemistry_data.append(l)
if len(immunohistochemistry) > 5:
    immunohistochemistry_data_2.append(l)
i = 0
for item in immunohistochemistry:
    l = []
    for key, value in item.items():
        l.append(value)
    if i < 5:
        immunohistochemistry_data.append(l)
    else:
        immunohistochemistry_data_2.append(l)
    i = i + 1
    
# Create a Table object
table = Table(immunohistochemistry_data)
table.setStyle(style)
table_width, table_height = table.wrap(200, 50)
table.drawOn(c, 35, b_height - 15 - table_height)

if len(immunohistochemistry) > 5:
    table = Table(immunohistochemistry_data_2)
    table.setStyle(style)
    table_width1, table_height1 = table.wrap(200, 50)
    table.drawOn(c, 35 + 250, b_height - 15 - table_height1)


## GENE TESTED WITH INDETERMINATE RESULTS
b_height = b_height - 40 - table_height
c.setFont("Helvetica", 15)
c.setFillColor(colors.steelblue)
c.drawString(35, b_height - 10, "Genes Tested with Indeterminate Results by Tumor DNA Sequencing")

# get table data from json file
genes_indeterminate = find_in_json(data, 'Genes Tested with indeterminate results')
i = 0
c.setFont("Helvetica", 9)
c.setFillColor(colors.black)
for item in genes_indeterminate:
    c.drawString(40 + i, b_height - 30, item)
    i += 50
    
footer(c, width)

### PAGE 4
c.showPage()
header(c)
b_height = height - 120
c.drawString(35, b_height, "Specimen Information")
c.line(35, b_height - 15, width - 35, b_height - 15)
c.setFont("Helvetica", 9)
c.setFillColor(colors.black)
c.drawString(35, b_height - 30, "Specimen ID: "+find_in_json(data, 'specimen_ID'))
c.drawString(35, b_height - 45, "Specimen Recieved: "+find_in_json(data, 'ReceivedDate'))
c.drawString(235, b_height - 30, "Specimen Collected: "+find_in_json(data, 'CollectedDate'))
c.drawString(235, b_height - 45, "Testing Initiated: "+find_in_json(data, 'ReceivedDate'))
c.drawString(35, b_height - 60, "Gross Description: "+find_in_json(data, 'specimen_ID'))
c.setFont("Helvetica-Bold", 9)
c.drawString(35, b_height - 85, "Pathological Diagnosis: ")
styles = getSampleStyleSheet()
style = styles['Normal']
style.fontSize = 9
text = find_in_json(data, 'Pathological Diagnosis')
paragraph = Paragraph(text, style)
w, h = paragraph.wrap(500, 30)
paragraph.drawOn(c, 35, b_height - h - 90)
b_height = b_height - 110 - h
c.drawString(35, b_height, "Dissection Information: ")
text = find_in_json(data, 'Dissection Information')
paragraph = Paragraph(text, style)
w, h = paragraph.wrap(500, 30)
paragraph.drawOn(c, 35, b_height - h - 5)

footer(c, width)

### PAGE 5
c.showPage()
header(c)
b_height = height - 120
c.drawString(35, b_height, "Clinical Trials Connector")
c.setFont("Helvetica-Bold", 9)
c.setFillColor(colors.steelblue)
c.rect(35, b_height - 50, 540, 20, fill=1)
c.setFillColor(colors.whitesmoke)
c.drawString(35+200, b_height - 42.5, "CHEMOTHERAPY CLINICAL TRIALS")

# get table data from json file
ch_clinical_trials = find_in_json(data, 'Chemotherapy clinical trials')
ch_clinical_trials_data = []
l = []
for key, value in ch_clinical_trials[0].items():
    l.append(key)
ch_clinical_trials_data.append(l)
for item in ch_clinical_trials:
    l = []
    for key, value in item.items():
        if key == "Investigational agents":
            l.append(", ".join(value))   
        else:    
            l.append(value)
    ch_clinical_trials_data.append(l)
    
# Create a Table object
table = Table(ch_clinical_trials_data)
# Define the Table Style
style = TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.steelblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.lightsteelblue),
    ('GRID', (0, 0), (-1, -1), 1, colors.white),
    # ('SPAN', (0, -1), (-2, -1)), # Span across all but the last column
    ('FONTSIZE', (0, 0), (-1, -1), 8),
])
table.setStyle(style)
table_width, table_height = table.wrap(200, 50)
table.drawOn(c, 35, b_height - 50 - table_height)

b_height = b_height - 100 - table_height
c.setFont("Helvetica-Bold", 9)
c.setFillColor(colors.steelblue)
c.rect(35, b_height - 50, 540, 20, fill=1)
c.setFillColor(colors.whitesmoke)
c.drawString(35+200, b_height - 42.5, "TARGETED THERAPY CLINICAL TRIALS")

# get table data from json file
targeted_clinical_trials = find_in_json(data, 'Targeted therapy clinical trials')
targeted_clinical_trials_data = []
l = []
for key, value in targeted_clinical_trials[0].items():
    l.append(key)
targeted_clinical_trials_data.append(l)
for item in targeted_clinical_trials:
    l = []
    for key, value in item.items():
        if key == "Investigational agents":
            l.append(", ".join(value))   
        else:    
            l.append(value)
    targeted_clinical_trials_data.append(l)
    
# Create a Table object
table = Table(targeted_clinical_trials_data)
table.setStyle(style)
table_width, table_height = table.wrap(200, 50)
table.drawOn(c, 35, b_height - 50 - table_height)

footer(c, width)

# Save the PDF
c.save()

# Create the PDF


# Provide the path to the saved PDF
print(file_name)