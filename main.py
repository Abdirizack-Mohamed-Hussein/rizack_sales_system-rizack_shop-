from flask import Flask, render_template,request,redirect,url_for,flash,session
# importing from database.py
from database import get_data,insert_products,insert_sales,insert_users,check_email,email_and_password,\
profit_product,profit_per_day,get_sales_per_product,get_sales_per_day


# create an instance of this class
app = Flask(__name__)
app.secret_key='Abdirizack'

@app.route('/')

def base():
   if 'email' in session:
        return redirect(url_for('dashboard'))
  
   return render_template('base.html')


@app.route('/home')
def home():

   return render_template('home.html')

@app.route("/dashboard")
def dashboard():
     # protect dashboard
    if "email" not in session:
        flash("Login to access this page")
        return redirect(url_for("login"))
    
    #display profit per product
    pr_profit=profit_product()
    p_name=[]
    p_profit=[]

    for i in pr_profit:
        p_name.append(i[0])
        p_profit.append(float(i[1]))

        #display profit per day
    profit_day=profit_per_day()
    date=[]
    date_profit=[]
    for i in profit_day:
        date.append(str(i[0]))
        date_profit.append(float(i[1]))

        # display sales per product
    sales_per_product = get_sales_per_product()
    product_name=[]
    quantity=[]
    

    for i in sales_per_product:        
        quantity.append(float(i[1]))
      #   SALES PER DAY
    sales_per_day=get_sales_per_day()
    dates_sales=[]

    for i in sales_per_day:     
        dates_sales.append(float(i[1]))
    
    return render_template("dashboard.html",p_name=p_name,p_profit=p_profit,date=date,date_profit=date_profit,\
                           product_name=product_name,quantity=quantity,dates_sales=dates_sales)

# REGISTER ROUTE
@app.route("/Register",methods=["POST","GET"])
def Register():
#get form data
 if request.method=="POST":
        full_name=request.form["full_name"]
        email=request.form["email"]
        password=request.form["password"]

        # CHECK EMAIL
        checking_email=check_email(email)
        
        if checking_email==None:
#insert to database
           new_users=(full_name,email,password)
           insert_users(new_users)
           flash("Registration Successfully done")
           return redirect(url_for("login"))
        else: 
             flash("Email already exist use a different email or login")
           
        
 return render_template('register.html')


# LOGIN ROUTE
@app.route("/Login",methods=["POST","GET"])
def login():
    # Check if user is already logged in
    if "email" in session:
        flash("You are already logged in.")
        return redirect(url_for("dashboard"))  # Redirect to dashboard if logged in
    #get form data
    if request.method=="POST":
       email=request.form["email"]
       password=request.form["password"]

        # VERIFY EMAIL
       verify_email=check_email(email)
       if verify_email==None:
            flash("Email does not exist, Kindly Register")
            return redirect(url_for("register"))
       else:
            check_password=email_and_password(email,password)
            if len(check_password)<1:
                flash("Invalid email or Password")
            else:
                session["email"]=email
                return redirect(url_for("dashboard"))

    return render_template("login.html")

# LOGOUT ROUTE
@app.route('/logout')
def logout():
    # remove the email from the session if it's there
    session.pop('email', None)
    flash( "You're Out!")
    return redirect(url_for('login'))

@app.route('/products')
def products():
    # protect products
    if "email" not in session:
        flash("Login to access this page")
        return redirect(url_for("login"))
    products=get_data("products")
    
    return render_template('products.html',products=products)


# adding products
@app.route("/add products",methods=["POST","GET"])
def add_product():
    #get form data
    p_name=request.form["product_name"]
    b_price=request.form["buying_price"]
    s_price=request.form["selling_price"]
    s_quantity=request.form["stock_quantity"]

    #insert to database
    new_prod=(p_name,b_price,s_price,s_quantity)
    insert_products(new_prod)
    return redirect(url_for("products"))

@app.route('/Sales')
def sales():
     # protect sales
    if "email" not in session:
        flash("Login to access this page")
        return redirect(url_for("login"))

    sales=get_data("sales")
    #fetching the products
    products=get_data("products") #displaying the products names
 
    return render_template("sales.html",sales=sales,products=products )


#creating route for making a sale
@app.route("/make_sales",methods=["POST","GET"])
def make_sale():
    #get the form data
    pid=request.form["pid"]
    quantity=request.form["stock_quantity"]
    new_sale=(pid,quantity)
    insert_sales(new_sale)
   
    return redirect(url_for("sales"))

  

if __name__ == '__main__':
    app.run(debug=True)
