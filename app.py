from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mayank0808@localhost/billing_system'
db = SQLAlchemy(app)

class Client(db.Model):
    Client_ID = db.Column(db.BIGINT, primary_key=True)
    Name = db.Column(db.String(50))
    Phone_No = db.Column(db.BIGINT)
    Address = db.Column(db.String(75))
class Vendor(db.Model):
    GST_No = db.Column(db.BIGINT, primary_key=True)
    Name = db.Column(db.String(50))
    Phone_No = db.Column(db.BIGINT)
    Address = db.Column(db.String(75))
    Material = db.Column(db.String(75))
class Contractor(db.Model):
    GST_No = db.Column(db.BIGINT, primary_key=True)
    Name = db.Column(db.String(50))
    Phone_No = db.Column(db.BIGINT)
    Address = db.Column(db.String(75))
    Service = db.Column(db.String(75))
class Company(db.Model):
    Name = db.Column(db.String(50), primary_key=True)
    Address = db.Column(db.String(75))
    Phone_No = db.Column(db.BIGINT)
class Admin(db.Model):
    Admin_ID = db.Column(db.BIGINT, primary_key=True)
    Username = db.Column(db.String(75))
    Password = db.Column(db.String(75))
class Project(db.Model):
    Project_ID = db.Column(db.BIGINT, primary_key=True)
    Name = db.Column(db.String(50))
    Vendor = db.Column(db.BIGINT, db.ForeignKey('vendor.GST_No'))
    Contractor = db.Column(db.BIGINT, db.ForeignKey('contractor.GST_No'))
    Client = db.Column(db.BIGINT, db.ForeignKey('client.Client_ID'))
class VendorContractorsJunction(db.Model):
    ID = db.Column(db.BIGINT, primary_key=True)
    GST_No = db.Column(db.BIGINT)
    IsVendor = db.Column(db.Boolean)


# Define other table classes similarly (Vendor, Contractor, Company, Admin, Project, VendorContractorsJunction, Bills, Installment)

# Define the Bill model
class Bill(db.Model):
    Bill_ID = db.Column(db.BIGINT, primary_key=True)
    Issue_Date = db.Column(db.DATE)
    Service = db.Column(db.String(75))
    Quantity = db.Column(db.BIGINT)
    Cost = db.Column(db.FLOAT(20, 3))
    SGST = db.Column(db.FLOAT(10, 3))  # Use FLOAT for SGST and CGST
    CGST = db.Column(db.FLOAT(10, 3))
    Total_Amount = db.Column(db.FLOAT(20, 3))
    Status = db.Column(db.String(10))
    VendorContractor_ID = db.Column(db.BIGINT, db.ForeignKey('vendor_contractors_junction.ID'))
    Project_ID = db.Column(db.BIGINT, db.ForeignKey('project.Project_ID'))
    Balance = db.Column(db.FLOAT(20, 3))

@app.before_first_request
def create_tables():
    db.create_all()
    
@app.route('/')
def index():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)

@app.route('/vendors')
def vendors():
    vendors = Vendor.query.all()
    return render_template('vendors.html', vendors=vendors)
@app.route('/contractors')
def contractors():
    contractors = Contractor.query.all()
    return render_template('contractors.html', contractors=contractors)
@app.route('/companies')
def companies():
    companies = Company.query.all()
    return render_template('companies.html', companies=companies)
@app.route('/admins')
def admins():
    admins = Admin.query.all()
    return render_template('admins.html', admins=admins)
@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/junctions')
def junctions():
    junctions = VendorContractorsJunction.query.all()
    return render_template('junctions.html', junctions=junctions)

@app.route('/add_bill', methods=['GET', 'POST'])
def add_bill():
    if request.method == 'POST':
        bill_data = request.form
        new_bill = Bill(
            Bill_ID=12,
            Issue_Date=bill_data['issue_date'],
            Service=bill_data['service'],
            Quantity=bill_data['quantity'],
            Cost=bill_data['cost'],
            SGST=bill_data['cost']*0.025,
            CGST=bill_data['cost']*0.025,
            Total_Amount=bill_data['cost']+(0.05*bill_data['cost']),
            Status=bill_data['status'],
            VendorContractor_ID=bill_data['vendor_contractor_id'],
            Project_ID=bill_data['project_id'],
            Balance=bill_data['balance']
        )
        db.session.add(new_bill)
        db.session.commit()
        return redirect(url_for('bills'))
    return render_template('add_bill.html')

@app.route('/bills')
def bills():
    bills = Bill.query.all()
    return render_template('bills.html', bills=bills)
if __name__ == '__main__':
    app.run(debug=True)


