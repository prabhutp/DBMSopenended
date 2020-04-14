from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prabhu'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def index():
    cur =  mysql.connection.cursor()
    r=cur.execute("SELECT id FROM stock")
    r1=cur.execute("SELECT cus_id FROM customer")
    r2=cur.execute("SELECT sup_id FROM suppliers")
    r3=r2=cur.execute("SELECT * FROM purchase")
    return render_template("index.html",data=r,data1=r1,data2=r2,data3=r3)

@app.route('/stock',methods=['GET','POST'])
def stock():
    if(request.method=="POST"):
        form = request.form
        stock_id =  form['Id']
        name = form['Name']
        quantity = form['Quan']
        cur =  mysql.connection.cursor()
        r=cur.execute("SELECT id FROM stock")
        result=cur.fetchall()
        flag=0
        if r>0:
            for row in range(0,r):
                if (json.dumps(result[row]["id"])) == stock_id:
                    cur.execute("UPDATE stock SET quantity=quantity+%s WHERE id=%s",(quantity,stock_id))
                    flag=1
            if flag==0:    
                cur.execute("INSERT INTO stock(id,name,quantity) VALUES(%s,%s,%s)",(stock_id,name,quantity))
        else:
            cur.execute("INSERT INTO stock(id,name,quantity) VALUES(%s,%s,%s)",(stock_id,name,quantity))        
        mysql.connection.commit()
    cur =  mysql.connection.cursor()    
    result_value = cur.execute("SELECT * FROM stock")
    if (result_value > 0):
        data = cur.fetchall()
        return render_template('stock.html',data=data)    
    return render_template("stock.html")

@app.route('/suppliers',methods=['GET','POST'])
def Supliers():
    if(request.method=="POST"):
        print("Inside POST")
        form = request.form
        sup_id =  form['Buyer_id']
        sup_name = form['Buy_Name']
        address = form['address']
        stock_id = form['stock_id']
        quan = form['quan']
        cur =  mysql.connection.cursor()
        r = cur.execute("SELECT * FROM product")
        result=cur.fetchall()
        flag=0
        if r>0:
            print("Inside if")
            for row in range(0,r):
                if ((json.dumps(result[row]["prod_id"])) == stock_id):
                    print("Inside for")
                    amt = result[row]["amt"]
                    flag=1
                    re = cur.execute("SELECT * FROM suppliers")
                    res=cur.fetchall()
                    if re>0:
                        print("Inside re")
                        for ro in range(0,re):
                            if (((json.dumps(res[ro]["stock_id"]))) == stock_id) and (((json.dumps(res[ro]["sup_id"])) == sup_id )):
                                cur.execute("UPDATE stock SET quantity=quantity+%s WHERE id=%s",(quan,stock_id))
                                cur.execute("UPDATE suppliers SET quan=quan+%s WHERE stock_id=%s",(quan,stock_id))
                                cur.execute("UPDATE suppliers SET amt=amt+%s WHERE stock_id=%s",((int(amt)*int(quan)),stock_id))
                                mysql.connection.commit()
                                result_value = cur.execute("SELECT * FROM suppliers")
                                if (result_value > 0):
                                    data1 = cur.fetchall()
                                    return render_template("suppliers.html",data1=data1)
                                data1 = cur.fetchall()    
                                return render_template("suppliers.html",data1=data1)
                            else:
                                cur.execute("INSERT INTO suppliers(sup_id,sup_name,address,stock_id,quan,amt) VALUES(%s,%s,%s,%s,%s,%s)",(sup_id,sup_name,address,stock_id,quan,amt))
                                mysql.connection.commit()
                                result_value = cur.execute("SELECT * FROM suppliers")
                                if (result_value > 0):
                                    data1 = cur.fetchall()
                                    return render_template("suppliers.html",data1=data1)
                                data1 = cur.fetchall()    
                                return render_template("suppliers.html",data1=data1)
                    else:
                        print("Inside else")
                        cur.execute("INSERT INTO suppliers(sup_id,sup_name,address,stock_id,quan,amt) VALUES(%s,%s,%s,%s,%s,%s)",(sup_id,sup_name,address,stock_id,quan,amt))
                        mysql.connection.commit()
                        result_value = cur.execute("SELECT * FROM suppliers")
                        print(result_value)
                        if (result_value > 0):
                            data1 = cur.fetchall()
                            return render_template("suppliers.html",data1=data1)
                        data1 = cur.fetchall()    
                        return render_template("suppliers.html",data1=data1)                   
            if flag==0:
                print("Inside second if")
                data="Product Details not in Product Table"
                return render_template("suppliers.html",data=data)
        else:
            data="Product Details not in Product Table"
            print("Inside else")
            return render_template("suppliers.html",data=data)        
         
        mysql.connection.commit()
    cur =  mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM suppliers")
    if (result_value > 0):
        print("at bottom")
        data1 = cur.fetchall()
        return render_template('suppliers.html',data1=data1)
    data1 = cur.fetchall()            
    return render_template("suppliers.html",data1=data1)

@app.route('/customers',methods=['GET','POST'])
def customers():
    if(request.method=="POST"):
        form = request.form
        cus_id = form['cus_id']
        cus_name = form['cus_name']
        cus_add = form['cus_add']
        cur =  mysql.connection.cursor()
        cur.execute("INSERT INTO customer(cus_id,cus_name,cus_add) VALUES(%s,%s,%s)",(cus_id,cus_name,cus_add))
        mysql.connection.commit()
    cur =  mysql.connection.cursor()    
    result_value = cur.execute("SELECT * FROM customer")
    if (result_value > 0):
        data = cur.fetchall()
        return render_template('customers.html',data=data)    
    return render_template("customers.html")     

@app.route('/purchase',methods=['GET','POST'])
def purchase():
    if(request.method=="POST"):
        form = request.form
        cus_id = form['cus_id']
        stock_id = form['stock_id']
        quan = form['quan']
        amt = form['amt']
        paid = form['paid_amt']
        cur =  mysql.connection.cursor()
        re1 = cur.execute("SELECT id,quantity FROM stock")
        res1=cur.fetchall()
        if re1>0:
            print("Inside re")
            for ro in range(0,re1):
                if (((json.dumps(res1[ro]["id"]))) == stock_id):
                    if int(((json.dumps(res1[ro]["quantity"])))) >= int(quan): 
                        re = cur.execute("SELECT * FROM purchase")
                        res=cur.fetchall()
                        flag=0
                        toamt=0
                        status=1
                        if re>0:
                            print("Inside re")
                            for ro in range(0,re):
                                if (((json.dumps(res[ro]["cus_id"]))) == cus_id) and (((json.dumps(res[ro]["stock_id"])) == stock_id )):
                                    flag=1
                                    notpaid = (int(json.dumps(res[ro]["amt"]))+int(amt)) - (int(json.dumps(res[ro]["paid"]))+int(paid))
                                    if notpaid>0:
                                        status=0
                                    cur.execute("UPDATE purchase SET quan=quan+%s,amt=%s,paid=%s,notpaid=%s,status=%s",(quan,(int(json.dumps(res[ro]["amt"]))+int(amt)),(int(json.dumps(res[ro]["paid"]))+int(paid)),int(notpaid),int(status)))
                                    cur.execute("UPDATE stock SET quantity=quantity-%s WHERE id=%s",(quan,stock_id))
                                    mysql.connection.commit()
                            if flag==0:        
                                not_paid = int(amt)-int(paid)
                                if(int(not_paid)>0):
                                    status=0
                                cur.execute("INSERT INTO purchase(cus_id,stock_id,quan,amt,paid,notpaid,status) VALUES(%s,%s,%s,%s,%s,%s,%s)",(cus_id,stock_id,quan,amt,paid,not_paid,status))
                                cur.execute("UPDATE stock SET quantity=quantity-%s WHERE id=%s",(quan,stock_id))
                                mysql.connection.commit()
                        else:        
                            not_paid = int(amt)-int(paid)
                            if(int(not_paid)>0):
                                status=0
                            cur.execute("INSERT INTO purchase(cus_id,stock_id,quan,amt,paid,notpaid,status) VALUES(%s,%s,%s,%s,%s,%s,%s)",(cus_id,stock_id,quan,amt,paid,not_paid,status))
                            cur.execute("UPDATE stock SET quantity=quantity-%s WHERE id=%s",(quan,stock_id))
                            mysql.connection.commit()
    cur =  mysql.connection.cursor()    
    result_value = cur.execute("SELECT * FROM purchase")
    if (result_value > 0):
        data = cur.fetchall()
        return render_template('purchase.html',data=data)    
    return render_template("purchase.html")

@app.route('/product',methods=['GET','POST'])
def product():
    if(request.method=="POST"):
        form = request.form
        prod_id = form['prod_id']
        prod_name = form['prod_name']
        amt = form['amt']
        min_quan = form['min_quan']
        cur =  mysql.connection.cursor()
        r=cur.execute("SELECT prod_id FROM product")
        result=cur.fetchall()
        flag=0
        if r>0:
            for row in range(0,r):
                if (json.dumps(result[row]["prod_id"])) == prod_id:
                    cur.execute("UPDATE product SET amt=%s,min=%s WHERE prod_id=%s",(int(amt),int(min_quan),int(prod_id)))
                    flag=1
            if flag==0:    
                cur.execute("INSERT INTO product(prod_id,prod_name,amt,min) VALUES(%s,%s,%s,%s)",(int(prod_id),prod_name,int(amt),int(min_quan)))
        else:
            cur.execute("INSERT INTO product(prod_id,prod_name,amt,min) VALUES(%s,%s,%s,%s)",(int(prod_id),prod_name,int(amt),int(min_quan)))
        mysql.connection.commit()    
    cur =  mysql.connection.cursor()    
    result_value = cur.execute("SELECT * FROM product")
    if (result_value > 0):
        data = cur.fetchall()
        return render_template('product.html',data=data)    
    return render_template("product.html") 

@app.route('/notpaid')
def notpaid():
    cur =  mysql.connection.cursor()
    result_value = cur.execute("SELECT * FROM purchase")
    if (result_value > 0):
        data = cur.fetchall()
        return render_template('notpaid.html',data=data)
    return render_template('notpaid.html')    

@app.route('/limitedstocks')
def limited():
    cur =  mysql.connection.cursor()
    result_value = cur.execute("SELECT s.id,s.name,s.quantity FROM stock s,product p where s.id=p.prod_id and s.quantity<p.min")
    if (result_value > 0):
        data = cur.fetchall()
        return render_template('limited_stocks.html',data=data)
    return render_template('limited_stocks.html')

if __name__ == '__main__':
    app.run(port=8000,debug=True)