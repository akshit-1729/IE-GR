from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import json
from find import find_in_json
from itertools import islice
import sys

# Define the PDF file name
file_name = f'./synthetic_data/doc_{sys.argv[2]}.pdf'
# open the json file
print(sys.argv[1])
filename = './synthetic_data/'+sys.argv[1]
with open(filename, 'r') as json_file:
    data = json.load(json_file)

# Create a canvas for the pdf
c = canvas.Canvas(file_name, pagesize=letter)
width, height = letter  # Size of letter page

# Define the positions for the text
first_quarter = width / 4

# function for common footer in every page
def footer(c, width, info):
    c.setStrokeColor(colors.grey)
    c.line(0, 50, width, 50)
    first_unit = width / 8
    c.setFont("Helvetica", 7)
    c.setFillColor(colors.grey)
    c.drawString(first_unit, 30, "Electronically signed by")
    c.setFillColor(colors.black)
    c.drawString(first_unit, 20, info["SignedBy"])
    c.setFillColor(colors.grey)
    c.drawString(2*first_unit + 10, 30, "CLIA number")
    c.setFillColor(colors.black)
    c.drawString(2*first_unit + 10, 20, "14D2114007")
    c.setFillColor(colors.grey)
    c.drawString(3*first_unit, 30, "Date Signed/Reported")
    c.setFillColor(colors.black)
    c.drawString(3*first_unit, 20, info["ReportDate"])
    c.setFillColor(colors.grey)
    c.drawString(4*first_unit + 10, 30, "Laboratory Medical Director")
    c.setFillColor(colors.black)
    c.drawString(4*first_unit + 10, 20, info["Supervisor"])
    c.setFillColor(colors.grey)
    c.drawString(5*first_unit + 40, 30, "ID #")
    c.setFillColor(colors.black)
    c.drawString(5*first_unit + 40, 20, info["ReportId"])
    c.setFillColor(colors.grey)
    c.drawString(6*first_unit + 20, 30, "Pipeline version")
    c.setFillColor(colors.black)
    c.drawString(6*first_unit + 20, 20, "3.2.0")


## HEADER

# Header styles
c.setFillColor(colors.whitesmoke)
# Draw black background
c.setFillColorRGB(0, 0, 0)  # Set the fill color to black
c.rect(0, height - 75, width, 100, fill=1)  # Draw the rectangle with fill
# Change fill color to white for the text
c.setFillColor(colors.whitesmoke)
# Draw the header texts
c.setFont("Helvetica", 16)
c.drawCentredString(first_quarter / 2, height - 45, find_in_json(data, "BodyPart") + " Sample")
c.drawCentredString(first_quarter / 2, height - 60, find_in_json(data, "Name"))
c.setFont("Helvetica", 10)
c.drawString(first_quarter + (first_quarter / 2.5), height - 40, "Diagnosis")
c.setFont("Helvetica-Bold", 10)
c.drawString(first_quarter + (first_quarter / 2.5), height - 55, find_in_json(data, "Diagnosis"))
c.setFont("Helvetica", 10)
c.drawString((first_quarter*2) + (first_quarter / 2), height - 40, "Accession No.")
c.setFont("Helvetica-Bold", 10)
c.drawString((first_quarter*2) + (first_quarter / 2), height - 55, find_in_json(data, "ReportId"))
c.setFont("Helvetica", 12)
c.drawCentredString((first_quarter*3) + (first_quarter / 1.5), height - 45, "xT")

### BODY
# new height for the body
b_height = height - 100

## left side of the body
c.setFillColor(colors.black)
c.setFont("Helvetica", 9)
c.drawString(30, b_height - 10, "Date of Birth")
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height - 22, find_in_json(data, "DateOfBirth"))
c.setFont("Helvetica", 9)
c.drawString(30, b_height - 44, "Sex")
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height - 56, find_in_json(data, "Sex"))
c.setFont("Helvetica", 9)
c.drawString(30, b_height - 78, "Physician")
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height - 90, find_in_json(data, "Physician"))
c.setFont("Helvetica", 9)
c.drawString(30, b_height - 112, "Institution")
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height - 124, find_in_json(data, "TreatingInstitution"))

c.setFont("Helvetica", 9)
b_height_left = b_height - 200
for key1, value1 in find_in_json(data, "specimen").items():
    c.drawString(30, b_height_left, key1+":")
    i = 10
    for key2, value2 in value1.items():
        c.drawString(30, b_height_left - i, key2+" "+value2)
        i = i + 12
    b_height_left = b_height_left - i - 20

## right side of the body
b_height_right = b_height 
c.setFont("Helvetica-Bold", 9)
c.setStrokeColor(colors.black)
c.drawString(first_quarter + (first_quarter / 2.5), b_height_right - 10, "GENOMIC VARIANTS", charSpace=0.5)
c.line(first_quarter + (first_quarter / 2.5), b_height_right - 15, first_quarter + (first_quarter / 2.5) + 375, b_height - 15)

c.drawString(first_quarter + (first_quarter / 2.5) + 270, b_height_right - 30, "variant allele fraction")

b_height_right = b_height - 30
styles = getSampleStyleSheet()
style = styles['Normal']
style.fontSize = 9
# add data of genomic variants
genomic_variants = find_in_json(data,"genomic variants") 
for key, value in islice(genomic_variants.items(), 2):
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(first_quarter + (first_quarter / 2.5), b_height_right, key)
    i = 0
    i_text = 0
    for item in value:
        i = i + 25.5
        c.setFillColor(colors.black)
        if key == "Somatic - Potentially Actionable":
            c.roundRect(first_quarter + (first_quarter / 2.5), b_height_right - i, 50, 
                        14, 7, fill=1, stroke=1)
            c.setFillColor(colors.whitesmoke)
        else:
            c.roundRect(first_quarter + (first_quarter / 2.5), b_height_right - i, 50, 14, 7)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(first_quarter + (first_quarter / 2.5) + 12, b_height_right - i+3,
                     item["Gene"])
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        # c.drawString(first_quarter + (first_quarter / 2.5) + 60, b_height_right - i+3,
        #              item["DNA Alteration"] + '  ' +item["GeneMutation"])
        text = item["DNA Alteration"] + '  ' +item["GeneMutation"]
        style.fontSize = 9
        paragraph = Paragraph(text, style)
        w, h = paragraph.wrap(210, 15)
        paragraph.drawOn(c, first_quarter + (first_quarter / 2.5) + 60, b_height_right - i - h/2 + 6)
        c.drawString(first_quarter + (first_quarter / 2.5) + 270, b_height_right - i+3,
                     item["VariantAlleleFraction"])
        c.setFillColor(colors.black)
        x = float(item["VariantAlleleFraction"][0:-1])/100
        c.rect(first_quarter + (first_quarter / 2.5) + 310,  b_height_right - i+3,
               50 * x , 2, fill=1, stroke=0)
        c.setFillColor(colors.lightgrey)
        c.rect(first_quarter + (first_quarter / 2.5) + 310 + 50 * x, b_height_right - i+3, 
               50 * (1-x), 2, fill=1, stroke=0)    
    b_height_right = b_height_right - i - 20
 
b_height_right = b_height_right + 5    
c.setStrokeColor(colors.grey)
c.line(first_quarter + (first_quarter / 2.5), b_height_right, first_quarter + (first_quarter / 2.5) + 375, b_height_right)
b_height_right = b_height_right - 20    
for key, value in islice(genomic_variants.items(), 2, None):
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(first_quarter + (first_quarter / 2.5), b_height_right, key)
    c.setFont("Helvetica", 9)
    if value == []:
        c.drawString(first_quarter + (first_quarter / 2.5), b_height_right - 20,
                     "No " + key + " variants were found in the limited set of genes on which we report.")
        b_height_right = b_height_right - 20
    else:
        i = 0
        for item in value:
            c.setFillColor(colors.grey)
            c.setFont("Helvetica-Bold", 8)
            if len(item) <= 4:
                c.roundRect(first_quarter + (first_quarter / 2.5) + i, b_height_right - 25, 35, 
                        14, 7)
                c.drawCentredString(first_quarter + (first_quarter / 2.5) + i+17, b_height_right - 25 + 3,
                     item)
            if len(item) > 4 and len(item) < 8:
                c.roundRect(first_quarter + (first_quarter / 2.5) + i, b_height_right - 25, 45, 
                        14, 7)
                c.drawCentredString(first_quarter + (first_quarter / 2.5) + i+22, b_height_right - 25 + 3,
                     item)
            elif len(item) > 8:
                c.roundRect(first_quarter + (first_quarter / 2.5) + i, b_height_right - 25, 60, 
                        14, 7)
                c.drawCentredString(first_quarter + (first_quarter / 2.5) + i+30, b_height_right - 25 + 3,
                     item)
            i = i+45
        b_height_right = b_height_right - 20
    b_height_right = b_height_right - 15
    c.line(first_quarter + (first_quarter / 2.5), b_height_right, first_quarter + (first_quarter / 2.5) + 375, b_height_right)
    b_height_right = b_height_right - 20
    

# Add data of Immunotherapy markers
c.setFont("Helvetica-Bold", 9)
c.setFillColor(colors.black)
c.setStrokeColor(colors.black)
b_height_right = b_height_right - 20
c.drawString(first_quarter + (first_quarter / 2.5), b_height_right, "IMMUNOTHERAPY MARKERS", charSpace=0.5)
c.line(first_quarter + (first_quarter / 2.5), b_height_right - 5, first_quarter + (first_quarter / 2.5) + 375, b_height_right - 5)
b_height_right = b_height_right - 5
immunotherapy_markers = find_in_json(data, "immunotherapy markers")
for item in immunotherapy_markers:
    c.drawString(first_quarter + (first_quarter / 2.5), b_height_right - 20, item['marker_name'])
    c.drawString(first_quarter + (first_quarter / 2.5) + 150, b_height_right - 20, item["Status type"])
    c.setFont("Helvetica-Bold", 9)
    c.setFillColorRGB(0, 153/255.0, 204/255.0) 
    c.roundRect(first_quarter + (first_quarter / 2.5), b_height_right - 45, 50, 16, 8, fill=1, stroke=1)
    c.setFillColor(colors.whitesmoke)
    c.drawString(first_quarter + (first_quarter / 2.5)+6, b_height_right - 41, item["TmbValue"])
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(first_quarter + (first_quarter / 2.5)+60, b_height_right - 41, item["Tmbpercentile"])
    c.roundRect(first_quarter + (first_quarter / 2.5)+150, b_height_right - 45, 210, 16, 8)
    c.drawString(first_quarter + (first_quarter / 2.5)+170, b_height_right - 41, "Stable")
    c.drawString(first_quarter + (first_quarter / 2.5)+170+(70*1), b_height_right - 41, "Equivocal")
    c.drawString(first_quarter + (first_quarter / 2.5)+170+(70*2), b_height_right - 41, "High")
    d = {"Stable": 0, "Equivocal": 1, "High": 2}
    c.setFillColorRGB(0, 153/255.0, 204/255.0) 
    c.roundRect(first_quarter + (first_quarter / 2.5)+150+70*d[item["statusvalue"]], b_height_right - 45, 70, 16, 8, fill=1, stroke=1)
    c.setFillColor(colors.whitesmoke)
    c.drawString(first_quarter + (first_quarter / 2.5)+170+70*d[item["statusvalue"]], b_height_right - 41, item["statusvalue"])
    c.setFillColor(colors.black)
    b_height_right = b_height_right - 45


# Add data of Therapies
b_height_right = b_height_right - 30
therapies = find_in_json(data, "FDA-Approved Therapies")
j = 0
styles = getSampleStyleSheet()
style = styles['Normal']
style.fontSize = 9
for key, value in therapies.items():
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.black)
    c.drawString(first_quarter + (first_quarter / 2.5), b_height_right - j, "FDA-APPROVED THERAPIES, " + key, charSpace=0.5)
    c.line(first_quarter + (first_quarter / 2.5), b_height_right - j - 5, first_quarter + (first_quarter / 2.5) + 375, b_height_right - j - 5)
    i = j + 20
    for item in value:
        if item is {}:
            continue
        c.setFont("Helvetica", 9)
        text = item['Mechanism']
        paragraph = Paragraph(text, style)
        w, h = paragraph.wrap(75, 40)
        paragraph.drawOn(c, first_quarter + (first_quarter / 2.5), b_height_right - i - h/2 - 3)
        # c.drawString(first_quarter + (first_quarter / 2.5), b_height_right - i, item['val1'])
        # c.drawString(first_quarter + (first_quarter / 2.5), b_height_right - i - 15, item['val12'])
        c.setFont("Helvetica-Bold", 9)
        c.drawString(first_quarter + (first_quarter / 2.5)+100, b_height_right - i, item['Medication'])
        c.setFont("Helvetica", 9)
        for val in item['Recommendations']:
            c.drawString(first_quarter + (first_quarter / 2.5)+175, b_height_right - i, val)
            i = i + 15
        c.drawString(first_quarter + (first_quarter / 2.5)+175, b_height_right - i, item['Relevant Mutation'])
        # c.drawString(first_quarter + (first_quarter / 2.5)+175, b_height_right - i - 15, item['val32'])
        # c.drawString(first_quarter + (first_quarter / 2.5)+175, b_height_right - i - 30, item['val33'])
    i = i + 15
    b_height_right = b_height_right - i
    c.setStrokeColor(colors.grey)
    c.line(first_quarter + (first_quarter / 2.5), b_height_right, first_quarter + (first_quarter / 2.5) + 375, b_height_right)
    j = j + 20


#footer of the report
footer(c, width, find_in_json(data, "other"))

### PAGE 2
c.showPage()
footer(c, width, find_in_json(data, "other"))
b_height = height - 35
c.setStrokeColor(colors.black)
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height, "ADDITIONAL INDICATORS", charSpace=0.5)
c.line(30, b_height - 5, width - 30, b_height - 5)
add_indicators = find_in_json(data, "Additional Indicators")
i = 20
for item in add_indicators:
    c.setFont("Helvetica-Bold", 9)
    c.drawString(30, b_height - i, item["description"])
    c.setFont("Helvetica", 9)
    c.drawString(300, b_height - i, item["therapy"])
    c.drawString(300, b_height - i - 15, item["mutation"])
    c.setStrokeColor(colors.grey)
    c.line(30, b_height - i - 25, width - 30, b_height - i - 25)
    b_height = b_height - i - 25

# Add data for clinical trials 
b_height = b_height - 30
c.setStrokeColor(colors.black)
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height, "CLINICAL TRIALS", charSpace=0.5)
c.line(30, b_height - 5, width - 30, b_height - 5)
b_height = b_height - 5
styles = getSampleStyleSheet()
style = styles['Normal']
style.fontSize = 9
clinical_trials = find_in_json(data, "Clinical trials")
i = 15
for item in clinical_trials:
    text = item["description"]
    paragraph = Paragraph(text, style)
    w, h = paragraph.wrap(350, 30)
    paragraph.drawOn(c, 30, b_height - i - h)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(400, b_height - i , item["phase"])
    c.setFont("Helvetica", 9)
    c.drawString(400, b_height - i - 10, "City, state - x mi")
    j = 20
    for mut in item["mutations"]:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(400, b_height - i - j, mut + " mutation")
        j = j + 10
    c.setStrokeColor(colors.grey)
    c.line(30, b_height - i - j - 5, width - 30, b_height - i - j - 5)
    b_height = b_height - i - j - 10
    

# Add data for other gene variants
b_height = b_height - 30
c.setStrokeColor(colors.black)
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height, "VARIANTS OF UNKNOWN SIGNIFICANCE", charSpace=0.5)
c.line(30, b_height - 5, width - 30, b_height - 5)
b_height = b_height - 5
v_unknown_significance = find_in_json(data, "variants of unknown significance")
for key, value in v_unknown_significance.items():
    if value == []:
        continue
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.black)
    c.drawString(30, b_height - 20, key)
    c.drawString(120, b_height - 20, "Mutation effect")
    if key == "Somatic":
        c.drawString(375, b_height - 20, "Variant allele fraction")
    else:
        c.drawString(375, b_height - 20, "Condition")
    i = 15
    for item in value:
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.black)
        c.drawString(30, b_height - 20 - i, item["Gene"])
        c.drawString(120, b_height - 20 - i, item["DNA Alteration"] + '  ' + item["GeneMutation"])
        c.drawString(120, b_height - 20 - i - 10, "NM_001011645")
        if key == "Somatic":
            c.drawString(375, b_height - 20 - i, item["VariantAlleleFraction"])
            x = float(item["VariantAlleleFraction"][0:-1])/100
            c.rect(410,  b_height - 20 - i, 60 * x , 2,
                fill=1, stroke=0)
            c.setFillColor(colors.lightgrey)
            c.rect(410 + 60 * x, b_height - 20 - i, 60 * (1-x), 2,
                fill=1, stroke=0)
        else:
            c.drawString(375, b_height - 20 - i, item["Condition"])
        i = i + 30
    b_height = b_height - i

### PAGE 3
c.showPage()
footer(c, width, find_in_json(data, "other"))
b_height = height - 35
c.setStrokeColor(colors.black)
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height, "LOW COVERAGE REGIONS", charSpace=0.5)
c.line(30, b_height - 5, width - 30, b_height - 5)
b_height = b_height - 5
low_coverage_regions = find_in_json(data, "low coverage regions")
i = 0
for item in low_coverage_regions:
    c.setFont("Helvetica", 9)
    c.drawString(30 + i, b_height - 20, item)
    i = i + 100

# Add details of gene variants
b_height = b_height - 50
somatic_variants = find_in_json(data, "genomic variants details")
for key, value in somatic_variants.items():
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.black)
    c.drawString(30, b_height, key.upper(), charSpace=0.5)
    c.line(30, b_height - 5, width - 30, b_height - 5)
    i = 30
    for item in value:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(colors.black)
        if key == "Somatic Variant Details - Potentially Actionable":
            c.roundRect(30, b_height - i, 60, 
                        16, 8, fill=1, stroke=1)
            c.setFillColor(colors.whitesmoke)
        else:
            c.roundRect(30, b_height - i, 60, 16, 8)
        c.drawString(30 + 30 - len(item["Gene"])*3, b_height - i + 4, item["Gene"])
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 9)
        c.drawString(100, b_height - i + 4, item["DNA Alteration"] + '  ' + item["GeneMutation"])
        c.drawString(475, b_height - i + 4, "VAF: " + item["VariantAlleleFraction"])
        x = float(item["VariantAlleleFraction"][0:-1])/100
        c.rect(525,  b_height - i + 6, 50 * x , 2,
               fill=1, stroke=0)
        c.setFillColor(colors.lightgrey)
        c.rect(525 + 50 * x, b_height - i + 6, 50 * (1-x), 2,
               fill=1, stroke=0)
        text = item["description"]
        style.fontSize = 9
        paragraph = Paragraph(text, style)
        w, h = paragraph.wrap(width - 60, 50)
        paragraph.drawOn(c, 30, b_height - i - h - 5)
        b_height = b_height - i - h - 5
    b_height = b_height - 30
    
c.setFillColor(colors.black)
c.setFont("Helvetica-Bold", 9)
c.drawString(30, b_height, "CLINICAL HISTORY", charSpace=0.5)
c.line(30, b_height - 5, width - 30, b_height - 5)
b_height = b_height - 5
c.setFont("Helvetica", 9)
c.drawString(30, b_height - 20, "Diagnosed on")
c.drawString(30, b_height - 35, find_in_json(data, "clinical history")["Date"])

# Save the PDF
c.save()

# Return the path to the generated PDF header
print(file_name)
