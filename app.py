from flask import Flask, request, send_file, render_template
import pandas as pd
import os
import sys
import json
import math
import xlrd

from convert_C3D_US_TurnOut import convertToUSJson

# Create the uploads directory if it doesn't exist
uploads_dir = os.path.join(os.getcwd(), 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Save the uploaded file
        excel_file_path = os.path.join('uploads', file.filename)
        file.save(excel_file_path)
        
        # Convert to JSON
        json_file_path = excel_file_path + '.json'
        #df = pd.read_excel(excel_file_path)
        #df.to_json(json_file_path, orient='records', lines=True)        
        #return send_file(json_file_path, as_attachment=True)
        data = xlrd.open_workbook(excel_file_path) # open xls file
        sheet1 = data.sheet_by_index(0) # sheet start index 0
        nrows = sheet1.nrows # row number
        #print("The row number in the sheet is: " + str(nrows))
        standardfile = '/Users/bcaufield/source/Python/convert_c3d/US_Imperial_base.json'  # We need to add this to the form as a variable
        convertToUSJson(excel_file_path, standardfile, json_file_path, True, sheet1, nrows)  # Call the "convertToUSJson" function with the defined "standardFile"
        
        return send_file(json_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
