import psycopg2
#connect to database
conn=psycopg2.connect(user="postgres",dbname="rizack_shop",password="Abdirizack@38",port=5432,host="localhost")

cur=conn.cursor()

#TO GET PRODUCTS  
def get_data(products):
    query=f"SELECT * FROM {products}"
    cur.execute(query)
    data=cur.fetchall()
    return data

#insert data..PRODUCTS
def insert_products(VALUES):
    insert="INSERT INTO products(name,buying_price,selling_price,stock_quantity) VALUES(%s,%s,%s,%s);"
    cur.execute(insert,VALUES)
    conn.commit()



#TO GET SALES 


def get_data(Sales):
    query=f"SELECT * FROM {Sales}"
    cur.execute(query)
    data=cur.fetchall()
    return data



#insert data..SALES
def insert_sales(VALUES):
    insert="INSERT INTO sales(Product_ID, Quantity, Time) VALUES(%s,%s,now());"
    cur.execute(insert,VALUES)
    conn.commit()

    #insert data..USERS
def insert_users(VALUES):
    query="INSERT INTO users(full_name,email,password) VALUES(%s,%s,%s);"
    cur.execute(query,VALUES)
    conn.commit()

    # Create a function to check email existence:
def check_email(email):
    query='SELECT * FROM users where email=%s'
    cur.execute(query,(email,))
    data=cur.fetchone()
    return data

#Compare email and password
def email_and_password(email,password):
    query='SELECT* FROM users where email=%s and password=%s'
    cur.execute(query,(email,password))
    data=cur.fetchall()
    return data
    
#display profit per product
def profit_product():
    profits ="select name,sum((selling_price-buying_price)*quantity) from products join sales on products.id=sales_id group by name;"
    cur.execute(profits)
    data=cur.fetchall()
    return data
  

#profit per day

def profit_per_day():
    query="select date(sales.time) as sales_date,sum((selling_price-buying_price)*quantity)as profits from products join sales on sales_id=products.id group by sales_date order by sales_date asc"
    cur.execute(query)
    data=cur.fetchall()
    return data


# sales per product
def get_sales_per_product():

    query= "select p.name,sum(quantity*selling_price)as total_sales_per_product from products as p join sales on sales_id=p.id group by p.name;"
    cur.execute(query)
    data=cur.fetchall()
    return data


# get sales per day
def get_sales_per_day():
    
    query= "select date(sales.time)as sales_date,sum(selling_price*quantity)as profits from products join sales on sales_id=products.id group by sales_date order by sales_date ASC;" 
    cur.execute(query)
    data=cur.fetchall()
    return data

  