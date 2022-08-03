from flask import Flask, render_template, request, redirect
import csv
import os.path
app = Flask(__name__)

@app.route('/')
def my_home(title=None):
    return render_template('index.html', title='This is my site')

@app.route('/<string:page_name>')
def html_page(page_name, title=None):
    template='%s.html' % (page_name)
    return render_template(template, title=page_name)

def write_to_file(data):
    with open('database.txt', mode='a') as database:
        email = data['email']
        subject = data['subject']
        message = data['message']
        file = database.write(f'\n{email},{subject},{message}')
        
def write_to_csv(data):
    file_exists = os.path.isfile('database.csv')
    
    with open('database.csv', newline='', mode='a+') as database2:
        header_list = ['Email', 'Subject', 'Message']
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        if not file_exists:
            csv_writer.writerow(header_list)

        csv_writer.writerow([email,subject,message])

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_csv(data)
        return redirect('/thankyou')
    else:
        return 'Something went wrong. Try again!'