from flask import Flask, redirect, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import PrimaryKeyConstraint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///indian_banks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class indian_Banks(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    ifsc = db.Column(db.String(50), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    def __repr__(self) -> str:
        return f"{self.sno}-{self.ifsc}"

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method == 'POST':
        ifsc = request.form['ifsc']
        branch = request.form['branch']
        address = request.form['address']
        indian_banks = indian_Banks(ifsc=ifsc, branch=branch, address=address)
        db.session.add(indian_banks)
        db.session.commit()
    allindian_Banks=indian_Banks.query.all()
    return render_template('index.html',allindian_Banks=allindian_Banks)
    

@app.route("/search/<string:ifsc>", methods=['GET'])
def ifsc(ifsc):
    if request.method == "GET":
        ifsc = request.form['ifsc']
        indian_banks =indian_Banks.query.filter_by(ifsc=ifsc).first()
        return redirect("/")
    
    return render_template('ifsc.html',indian_banks=indian_banks)

@app.route("/edit/<int:sno>",methods=['GET','POST'])
def edit(sno):
    if request.method=='POST':
        ifsc = request.form['ifsc']
        branch = request.form['branch']
        address = request.form['address']
        indian_banks =indian_Banks.query.filter_by(sno=sno).first()
        indian_banks.ifsc = ifsc
        indian_banks.branch = branch
        indian_banks.address = address
        db.session.add(indian_banks)
        db.session.commit()
        return redirect("/")
    indian_banks =indian_Banks.query.filter_by(sno=sno).first()
    return render_template('edit.html',indian_banks=indian_banks)

@app.route("/delete/<int:sno>")
def delete(sno):
    indian_banks =indian_Banks.query.filter_by(sno=sno).first()
    db.session.delete(indian_banks)
    db.session.commit()
    return redirect("/")           


if __name__ == "__main__":
    app.run(debug=True, port=8000)    