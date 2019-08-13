import io
import os
import sys
import traceback
import datetime
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def retrieve_project_parameters():
    
    parameters = sys.argv

    parameters_number = parameters.index("-traces") if "-traces" in parameters else None
    if parameters_number is not None:
        parameters_number = parameters_number + 1
        traces = parameters[parameters_number]
    else:
        traces = ""

    parameters_number = parameters.index("-file") if "-file" in parameters else None
    if parameters_number is not None:
        parameters_number = parameters_number + 1
        file = parameters[parameters_number]
    else:
        file = ""

    parameters_number = parameters.index("-saveas") if "-saveas" in parameters else None
    if parameters_number is not None:
        parameters_number = parameters_number + 1
        saveas = parameters[parameters_number]
    else:
        saveas = file.lower().replace(".pdf", "_new.pdf")

    parameters_number = parameters.index("-text") if "-text" in parameters else None
    if parameters_number is not None:
        parameters_number = parameters_number + 1
        text = parameters[parameters_number]
    else:
        text = ""

    parameters_number = parameters.index("-size") if "-size" in parameters else None
    if parameters_number is not None:
        parameters_number = parameters_number + 1
        size = parameters[parameters_number]
    else:
        size = ""

    parameters_number = parameters.index("-position") if "-position" in parameters else None
    if parameters_number is not None:
        parameters_number = parameters_number + 1
        position = str(parameters[parameters_number]).split(",")
    else:
        position = str(",").split(",")
        
    return {
        "traces": traces,
        "file": file,
        "saveas": saveas,
        "text": text,
        "size": size,
        "position": position,
    }


def validate_project_parameters(parameters):
    
    traces = parameters["traces"]
    file = parameters["file"]
    saveas = parameters["saveas"]
    text = parameters["text"]
    size = parameters["size"]
    position = parameters["position"]
    
    if traces == "" or traces.upper() == "FALSE":
        traces = False
    elif traces.upper() == "TRUE":
        traces = True
    else:
        return "ERROR: Invalid traces parameter! Parameter = " + str(traces)

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "=== * Parameters retrieved start * ===")
        
    if os.path.isfile(file):
        if not file.upper().endswith(".PDF"):
            return "ERROR: The save as file is not PDF!"
    else:
        return "ERROR: The file was not found!"

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tFile = " + str(file))

    saveas_exists = os.path.isdir(os.path.dirname(os.path.abspath(saveas)))
    if saveas_exists:
        if not saveas.upper().endswith(".PDF"):
            return "ERROR: The save as file is not PDF!"
    else:
        return "ERROR: The save as folder directory was not found!"

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tSave as = " + str(saveas))

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tText = " + str(text))

    if size != "":
        if not size.isnumeric():
            return "ERROR: The specified size is not numeric!"
            
    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tSize = " + str(size))
        
    if isinstance(position, list):
        position = [i.strip() for i in position]
        
        for i in position:
            if not i.isnumeric():
                return "ERROR: The specified position is invalid!"
            
        position = {"x": position[0], "y": position[1]}
        
    else:
        return "ERROR: The specified position is invalid!"
            
    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tPosition = " + str(position))
               

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "=== * Parameters retrieved end * ===")
        
    return {
        "traces": traces,
        "file": file,
        "saveas": saveas,
        "text": text,
        "size": size,
        "position": position,
    }


def create_template(traces, pdf_packet, size, position, text):

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "=== * Create template start * ===")
    
    can = canvas.Canvas(pdf_packet, pagesize=letter)

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tCanvas generated...")

    if size is not "" and size.isnumeric():
        size = int(size)
        can.setFont('Courier', size=size)
    
        if traces is True:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tText size changed...")

    width, height = letter
    x, y = int(position["x"]), int(position["y"])
    can.drawString(width - x, height - y, text)

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tText drawn...")
        
    can.showPage()
    can.save()

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tTemplate saved...")

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "=== * Create template end * ===")
        
    can = None
    return pdf_packet


def generate_pdf(traces, pdf_packet, file, saveas):

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "=== * Generate PDF start * ===")
    
    pdf_packet.seek(0)
    pdf_reader = PdfFileReader(pdf_packet, strict=False)
    pdf_writer = PdfFileWriter()

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tPDF objects declared...")

    pdf_existing = PdfFileReader(open(file, "rb"), strict=False)
    pdf_existing_pages = pdf_existing.numPages
    
    for i in range(pdf_existing_pages):
        page = pdf_existing.getPage(i)
        page.mergePage(pdf_reader.getPage(0))
        pdf_writer.addPage(page)

        if traces is True:
            print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + f"\tPage {str(i+1)} of {str(pdf_existing_pages)} handled...")

    with open(saveas, "wb") as pdf_new:
        pdf_writer.write(pdf_new)

    if traces is True:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "\tOutput PDF generated...")
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ": " + "=== * Generate PDF end * ===")
        
    pdf_packet, pdf_reader, pdf_writer = None, None, None
    return pdf_packet
        

def execute_command(parameters):
    
    traces = parameters["traces"]
    file = parameters["file"]
    saveas = parameters["saveas"]
    text = parameters["text"]
    size = parameters["size"]
    position = parameters["position"]
    
    try:
        pdf_packet = io.BytesIO()
        pdf_packet = create_template(traces, pdf_packet, size, position, text)
        pdf_packet = generate_pdf(traces, pdf_packet, file, saveas)
    
    except:
        print(traceback.format_exc())
        return "ERROR: Unexpected issue!"
    
    return True
    
    
def main():

    parameters = retrieve_project_parameters()
    
    parameters = validate_project_parameters(parameters)
    if not isinstance(parameters, dict):
        print(str(parameters))
        return
    
    valid = execute_command(parameters)
    if not valid is True:
        print(str(valid))
        return
    
    print("SUCCESS")
    
    
if __name__ == "__main__":
    main()
