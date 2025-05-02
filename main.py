from flask import Flask, render_template,request,make_response,redirect,jsonify, Response
import json
import pymongo
import time

#Declarations
app = Flask(__name__)
current_name = []
with open('config.json', 'r') as c:
    base = json.load(c)
    params = base["params"]

#Connecting to the database
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['attendence_system']
collections = db['teachers']

#App Routes

@app.route("/",methods=['get','post'])
def index():
      print(len(current_name))
      if len(current_name) == 0:
          return redirect("/login")
      if request.form.get('sub_btn') == 'logout':
          current_name.pop()
          return redirect('/login')
      
      if request.form.get("sub_btn") == 'start':
          return redirect("/attendence")
          
      
      return render_template('index.html',name=current_name[0])

@app.route("/login",methods=['get','post'])
def login():
    error=None
    if request.method == 'POST':
        email = request.form.get('email-address')
        password = request.form.get('password')
        collected_data = collections.find()
        for i in collected_data:
            if i['email'] == email:
                if i['password'] == password:
                    print("Login is successful")
                    current_name.append(i['name'])
                    return redirect("/")
                else:
                    error = "Email or password is invalid"    
                    print("Error")
    return render_template("login.html", error=error)


@app.route("/signup", methods=['get', 'post'])
def signup():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    position = request.form.get('position')
    password = request.form.get('password')
    cpassword = request.form.get('cpassword')
    fullname = f"{first_name} {last_name}"
    error = None
    
    return render_template("signup.html")


@app.route("/attendence")
@app.route("/attendence")
def attendence():
    if len(current_name) == 0:
        return redirect("/login")  # Redirect to login if no user is logged in
    
    collection2 = db['attendence']
    data = []
    collect = collection2.find()
    for i in collect:
        data.append({
            "name":i["name"],
            "usn":i["usn"],
            "date":i["date"],
            "time":i["time"],
            "status":i["status"]
        })
    
    length = len(data)
    print(data)
    return render_template("attendence.html", name=current_name[0], data= data, length=length)


#Running the application
app.run(params['url'], int(params['port']), debug=True)