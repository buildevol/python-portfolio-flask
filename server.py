from flask import Flask, render_template, url_for, request, redirect
import csv
import pathlib

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(f"{page_name}.html")


@app.route('/thankyou/<string:name>')
def thank_you(name):
    return render_template("thankyou.html", name=name)


def write_to_file(data):
    with open('database.txt', mode='a') as database:
        name = data["name"]
        email = data["email"]
        message = data["message"]
        database.write(f'{name},{email},{message}\n')


def write_to_csv(data):
    databasePath = pathlib.Path("database.csv")
    isPresent = databasePath.exists()
    print(isPresent)
    with open('database.csv', mode='a', newline='') as database:
        field_names = ['name', 'email', 'message']
        writer = csv.DictWriter(database, fieldnames=field_names)
        if (not isPresent):
            writer.writeheader()
        writer.writerow(data)


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    error = None
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            print(data)
            write_to_csv(data)
            return redirect(url_for("thank_you", name=data["name"]))
        except:
            return 'An error occurred hence, unable to update database.'
    else:
        return "An error is encountered."
