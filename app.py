from flask import Flask, render_template, request
import pickle


app = Flask(__name__)


with open("rf_salary_model.pkl","rb")as file:
    salary_model=pickle.load(file)
    
with open("lb_salary.pkl","rb")as file:
    lb_salary=pickle.load(file)

with open("lb1_salary.pkl","rb")as file:
    lb1_salary=pickle.load(file)

def salaryPrediction(Age=33, Gender="Female", Education_Level="Bachelor's Degree", Job_Title="Software Engineer", Years_of_Experience=3):
    lst = []

    lst.append(Age)

    if Gender == "Female":
        lst.append(0)
    elif Gender == "Male":
        lst.append(1)
    elif Gender == "Other":
        lst.append(2)

    Education_Level_encoded = lb1_salary.transform([Education_Level])
    lst.extend(Education_Level_encoded)

    Job_Title_encoded = lb_salary.transform([Job_Title])
    lst.extend(Job_Title_encoded)

    lst.append(Years_of_Experience)

    result = salary_model.predict([lst])
    return result[0]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        Age = float(request.form.get("Age"))
        Gender = request.form.get("Gender")
        Education_Level = request.form.get("Education_Level")
        Job_Title = request.form.get("Job_Title")
        Years_of_Experience = float(request.form.get("Years_of_Experience"))

        result = salaryPrediction(
            Age=Age,
            Gender=Gender,
            Education_Level=Education_Level,
            Job_Title=Job_Title,
            Years_of_Experience=Years_of_Experience
        )

        return render_template("predict.html", prediction=result)

    return render_template("predict.html")

if __name__ == "__main__":
    app.run(debug=True)
