from flask import Flask, request, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)


# Create the uploads directory if it doesn't exist
# uploads_dir = os.path.join(os.getcwdu(), 'uploads')
# os.makedirs(uploads_dir)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
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
        df = pd.read_excel(excel_file_path)
        df.to_json(json_file_path, orient='records', lines=True)

        return send_file(json_file_path, as_attachment=True)


if __name__ == '__main__':
    app.run()
