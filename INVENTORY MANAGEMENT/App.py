from flask import Flask, render_template, request, url_for
import pymysql
from retry import retry


app = Flask(__name__)

# MySQL configuration
mysql_host = 'localhost'
mysql_user = 'root'
mysql_password = '1234'
mysql_database = 'inventory_management'

# Connect to the MySQL database
db = pymysql.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)
#report
@app.route('/')
def report():
     data = fetch_data_from_table()
     return render_template('report.html', data=data)

#for report table
def fetch_data_from_table():
    cursor = db.cursor()
    query = "SELECT * FROM report"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()

    return data

#add location
@app.route('/location', methods=['GET', 'POST'])
def location():
    if request.method == 'POST':
        location = request.form['location']
        exists = check_location_exists(location,)

        if exists:
            return render_template('location.html',  exists=exists)
           

        else :
            cursor = db.cursor()
            query = "insert into location(location_id) values(%s)"
            cursor.execute(query,( location,))
            db.commit()
            query = "insert into report(location_id,product_id,qty) values(%s,%s,%s)"
            cursor.execute(query,( location,"null",0,))
            db.commit()
            cursor.close()

    return render_template('location.html')

#for checking the exist location
def check_location_exists(location):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM location WHERE location_id = %s"
    cursor.execute(query, (location,))
    result = cursor.fetchone()
    cursor.close()

    return result[0] > 0

#add product
@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'POST':
        product = request.form['product']
        location = request.form['location']
        qty = request.form['qty']
        exists = check_product_exists(product,)
        exist = check_location_exists(location,)
        rep =check__exists(location,product)

        if rep:
            cursor = db.cursor()
            update_quantity_in_table(qty,product,location)
            db.commit

        elif exists and exist :
            cursor = db.cursor()
            query = "insert into report(location_id,product_id,qty) values(%s,%s,%s)"
            cursor.execute(query,( location,product,qty,))
            db.commit()
        elif exist:
            cursor = db.cursor()
            query = "insert into product(product_id) values(%s)"
            cursor.execute(query,( product,))
            cursor = db.cursor()
            query = "insert into report(location_id,product_id,qty) values(%s,%s,%s)"
            cursor.execute(query,( location,product,qty,))
            db.commit()
            cursor.close()

        elif exists:
            cursor = db.cursor()
            query = "insert into location(location_id) values(%s)"
            cursor.execute(query,( location,))
            db.commit()
            query = "insert into report(location_id,product_id,qty) values(%s,%s,%s)"
            cursor.execute(query,( location,product,qty,))
            db.commit()
            cursor.close()

        else :
            cursor = db.cursor()
            query = "insert into location(location_id) values(%s)"
            cursor.execute(query,( location,))
            db.commit()
            query = "insert into report(location_id,product_id,qty) values(%s,%s,%s)"
            cursor.execute(query,( location,product,qty,))
            db.commit()
            query = "insert into product(product_id) values(%s)"
            cursor.execute(query,( product,))
            db.commit()
            cursor.close() 


    return render_template('product.html')

#check product exist
def check_product_exists(product):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM product WHERE product_id = %s"
    cursor.execute(query, (product,))
    result = cursor.fetchone()
    cursor.close()

    return result[0] > 0

#check product and location also
def check__exists(location,product):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM report where location_id = %s and product_id = %s "
    cursor.execute(query, (location,product))
    result = cursor.fetchone()
    cursor.close()

    return result[0] > 0
#update quantity
def update_quantity_in_table(quantity,product,location):
    cursor = db.cursor()
    query = "UPDATE report SET qty = qty + %s where location_id = %s and product_id = %s "
    cursor.execute(query, (quantity,location,product,))
    db.commit()
    cursor.close()
#update the product and quantity
def update_only_quantityt_in_table(quantity,product,location):
    cursor = db.cursor()
    query = "UPDATE report SET qty = qty + %s where location_id = %s "
    cursor.execute(query, (quantity,location,))
    db.commit()
    query = "UPDATE report SET product_id =  %s where location_id = %s "
    cursor.execute(query, (product,location,))
    db.commit()
    cursor.close()   


#move products
@app.route('/movement', methods=['GET', 'POST'])
def movement():
    if request.method == 'POST':
        product = request.form['prod']
        From = request.form['from']
        qty = request.form['qty']
        To = request.form['to']

        exist=check_that_exists(To,product)
        if exist:

            cursor = db.cursor()
            query = "UPDATE report SET qty = qty + %s where location_id = %s and product_id = %s "
            cursor.execute(query, (qty,To,product,))
            db.commit()
            query = "UPDATE report SET qty = qty - %s where location_id = %s and product_id = %s "
            cursor.execute(query, (qty,From,product,))
            db.commit()
            cursor.close()


        else:
            cursor = db.cursor()
            query = "insert into report (location_id,product_id,qty) values(%s,%s,%s)"
            cursor.execute(query, (To,product,qty,))
            db.commit()

            query = "UPDATE report SET qty = qty - %s where location_id = %s and product_id = %s "
            cursor.execute(query, (qty,From,product,))
            db.commit()
        
            cursor.close()
    return render_template('movement.html')

#check product exist
def check_that_exists(location,product):
    cursor = db.cursor()
    query = "SELECT COUNT(*) FROM report where location_id = %s and product_id = %s or 'no'"
    cursor.execute(query, (location,product))
    result = cursor.fetchone()
    cursor.close()

    return result[0] > 0

if __name__ == '__main__':
    app.run(debug=True)
