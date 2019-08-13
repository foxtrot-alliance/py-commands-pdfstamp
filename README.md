# py-commands-pdfstamp

For support, please contact us: support@foxtrotalliance.com

This program allows you to stamp PDF files with a certain text like, for example, stamping a document number. You can run the program via the CMD or as part of an automation script in an RPA tool like Foxtrot. This solution is meant to supplement Foxtrots core functionality and enable you to add text on top of a text PDF document. The solution is written in Python using the modules "PyPDF2" and "reportlab". You can see the [full source code here](https://github.com/foxtrot-alliance/py-commands-pdfstamp/blob/master/py-commands-pdfstamp.py).

## Installation

1. Download the [latest version](https://github.com/foxtrot-alliance/py-commands-pdfstamp/releases/download/v0.0.1/py-commands-pdfstamp_v0.0.1.zip).
2. Unzip the folder somewhere appropriate, we suggest directly on the C: drive for easier access. So, your path would be similar to "C:\py-commands-pdfstamp_v0.0.1".
3. After unzipping the files, you are now ready to use the program. The only file you will have to be concerned about is the actual .exe file in the folder, however, all the other files are required for the solution to run properly.
4. Open Foxtrot (or any other RPA tool) to set up your action. In Foxtrot, you can utilize the functionality of the program via the DOS Command action (alternatively, the Powershell action).

## Usage

When using the program via Foxtrot, the CMD, or any other RPA tool, you need to reference the path to the program exe file. If you placed the program directly on your C: drive as recommended, the path to your program will be similar to: 
```
C:\py-commands-pdfstamp_v0.0.1\py-commands-pdfstamp_v0.0.1.exe
```
TIP: Make sure NOT to surround the path with quotation marks in your commands.

## Commands

The program offers a single command; to stamp a specified PDF file with a specified text. These are the available parameters:
```
-file: "X", required
  This is the file path to the .PDF file you wish to solution to work with.
  
-saveas: "X", default = the value of the file parameter with "_new" appended to the file name
  This is an optional parameter to specify the save as file path.

-text: "X", required
  This is the text to stamp on the PDF file.

-size: "X", default = document standard
  This is an optional parameter to set the size of the text to stamp.

-position: "X, Y", required
  This is pixel coordinates to place the text, starting from the top corner. "0, 0" will be top right corner.

-traces: "true"/"false", default = "false"
  This determines whether you wish the output to include traces, information about the execution.
```

## Examples
```
PROGRAM_EXE_PATH -file "c:\file.pdf" -text "123" -position "100, 50"
PROGRAM_EXE_PATH -file "c:\file.pdf" -saveas "c:\file_handled.pdf" -text "123" -position "150, 150" -size "16"
PROGRAM_EXE_PATH -file "c:\file.pdf" -saveas "c:\file.pdf" -text "Hello there!" -position "250, 200" -size "12" -traces "true"
```
