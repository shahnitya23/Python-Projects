# importing the Flask class object from the flask library
from flask import Flask, render_template

# instantiating that class object
# __name__ special var. that will get the value of the name of the python script
# Python file/script assigns the name '__main__' as the string to the file
    # __name__ == '__main__'
    # Case 2 - Script imported:
        # __name__ = 'script1'
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/projects/')
def projects():
    return render_template('projects.html')

@app.route('/clubs/')
def clubs():
    return render_template('clubs.html')

@app.route('/Work Experience/')
def work_exp():
    return render_template('work_exp.html')

@app.route('/Contact/')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug = True)
