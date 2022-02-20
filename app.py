from flask import Flask, redirect, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///xyz.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    no = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(10), nullable=False) 
    password = db.Column(db.String(10), nullable=False)
    conf_password = db.Column(db.String(10), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.no} - {self.email}"



@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conf_password = request.form['conf_password']
        xyz = Todo(name=name, email=email, password=password , conf_password=conf_password)
        db.session.add(xyz)
        db.session.commit()
    
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/delete/<int:no>')
def delete(no):
    xyz = Todo.query.filter_by(no=no).first()
    db.session.delete(xyz)
    db.session.commit()
    return redirect("/")

@app.route('/Update/<int:no>' , methods=['GET', 'POST'])
def update(no):
    if request.method=='POST':
         email = request.form['email']
         password = request.form['password']
         xyz = Todo.query.filter_by(no=no).first()
         xyz.email = email
         xyz.password = password
         db.session.add(xyz)
         db.session.commit()
         return redirect("/")
     
    xyz = Todo.query.filter_by(no=no).first()
    return  render_template('update.html', xyz=xyz) 




if __name__ == "__main__":
    app.run(debug=True, port=8000)