import os
import pymysql.cursors
from flask import Flask,render_template, redirect, url_for, request
app = Flask(__name__) 
 
con=pymysql.connect('localhost','root','','silverstone')
emaill=''
valuee=''
typee=''
@app.route('/')
def main():
   return render_template('index.html',flag=0)
   
@app.route('/logout')
def logout():
   return render_template('index.html',flag=0)
 
@app.route('/loginpage',methods=["GET","POST"]) 
def loginpage():			
	return render_template('loginn.html')

@app.route('/login',methods=["GET","POST"])
def login():
	if request.method =='POST':
		cur=con.cursor()
		cur.execute("SELECT * FROM login")
		for r in range(0,100):
			row = cur.fetchone()
			if row is None:
				cur.close()
				return render_template('loginn.html',error=1)
			else:
				if request.form['mail'] == row[1] and request.form['pass'] == row[4]:
				   global emaill
				   global valuee
				   global typee
				   emaill=row[1]
				   valuee=row[2]
				   typee=row[0]
				   cur.close()
				   return render_template('index.html',flag=1,value=valuee,type=typee)
	else:
		return 'INVALID CREDENTIALS'
		 
@app.route('/insertlogin',methods=["GET","POST"])
def insertlogin():
	if request.form["action"] == "Register":
		name=request.form['Username']
		email=request.form['email']
		password=request.form['Password']
		type=request.form['Type']
		mobile=request.form['mobile']
		a=con.cursor()
		a.execute("INSERT INTO login (type,email,name,mobile,password) VALUES (%s,%s,%s,%s,%s)",(type,email,name,mobile,password))
		con.commit()
		a.close()
		return render_template('index.html')
   
@app.route('/granite',methods=["GET","POST"])
def granite():
    return render_template('granite.html')

@app.route('/tiles',methods=["GET","POST"])
def tiles():
    return render_template('tiles.html')	
	
@app.route('/marble',methods=["GET","POST"])
def marble():
    return render_template('marble.html') 
	
@app.route('/back',methods=["GET","POST"])
def back():
	c=con.cursor()
	c.execute("select * from checkorder")
	for r in range(0,100):
		amt=c.fetchone()
		if amt is None:
			break
		else:
			if amt[0]==emaill:
				if amt[6]=="Paid":
					return render_template('index.html',flag=1,value=valuee,type=typee,paid=1)
	return render_template('index.html',flag=1,value=valuee,type=typee,paid=0) 
	
@app.route('/addtocart',methods=["GET","POST"])
def addtocart():
	if request.method=='POST':
		if request.form["marble"] == "Add to Cart":
			category=request.form['category']
			type=request.form['type']
			color=request.form['color']
			name=request.form['marblee']
			quantity=int(request.form['quantity'])
			size=int(request.form['size'])
			amount=int(size*quantity*100)
			b=con.cursor()
			b.execute("select * from marble")
			data=b.fetchall()
			for row in data:
				if name==row[4]:
					id=int(row[0])
			b.execute("drop trigger sizecheck")
			b.execute("CREATE TRIGGER sizecheck BEFORE INSERT ON cart FOR EACH ROW IF NEW.size = %s THEN SET NEW.size = %s; END IF",("0","1"))
			b.execute("INSERT INTO cart (p_id,id,category,type,color,name,size,quantity,amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(emaill,id,category,type,color,name,size,quantity,amount))
			con.commit()
			b.close()
			return redirect(url_for('marble'))  
		else:
			return redirect(url_for('main'))
	else:
		return redirect(url_for('main'))

@app.route('/gaddtocart',methods=["GET","POST"])
def gaddtocart():
	if request.method=='POST':
		if request.form["marble"] == "Add to Cart":
			category=request.form['category']
			type=request.form['type']
			color=request.form['color']
			name=request.form['marblee']
			quantity=int(request.form['quantity'])
			size=int(request.form['size'])
			amount=int(size*quantity*150)
			b=con.cursor()
			b.execute("select * from granite")
			data=b.fetchall()
			for row in data:
				if name==row[4]:
					id=int(row[0])
			b.execute("drop trigger sizecheck")
			b.execute("CREATE TRIGGER sizecheck BEFORE INSERT ON cart FOR EACH ROW IF NEW.size = %s THEN SET NEW.size = %s; END IF",("0","1"))
			b.execute("INSERT INTO cart (p_id,id,category,type,color,name,size,quantity,amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(emaill,id,category,type,color,name,size,quantity,amount))
			con.commit()
			b.close()
			return redirect(url_for('granite'))  
		else:
			return redirect(url_for('main'))
	else:
		return redirect(url_for('granite'))

@app.route('/taddtocart',methods=["GET","POST"])
def taddtocart():
	if request.method=='POST':
		if request.form["marble"] == "Add to Cart":
			category=request.form['category']
			type=request.form['type']
			color=request.form['color']
			name=request.form['marblee']
			quantity=int(request.form['quantity'])
			size=int(request.form['size'])
			amount=int(size*quantity*70)
			b=con.cursor()
			b.execute("select * from tiles")
			data=b.fetchall()
			for row in data:
				if name==row[4]:
					id=int(row[0])
			b.execute("drop trigger sizecheck")
			b.execute("CREATE TRIGGER sizecheck BEFORE INSERT ON cart FOR EACH ROW IF NEW.size = %s THEN SET NEW.size = %s; END IF",("0","1"))
			b.execute("INSERT INTO cart (p_id,id,category,type,color,name,size,quantity,amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(emaill,id,category,type,color,name,size,quantity,amount))
			con.commit()
			b.close()
			return redirect(url_for('tiles'))  
		else:
			return redirect(url_for('main'))
	else:
		return redirect(url_for('main'))

@app.route('/invoice',methods=["GET","POST"])
def invoice():
	tot=0
	gst=0
	e=con.cursor()
	e.execute("select * from cart")
	for r in range(0,100):
		t=e.fetchone()
		if t is None:
			break;
		else:
			if t[0]==emaill:
				c=con.cursor()
				c.execute("INSERT INTO checkorder (p_id,id,name,size,quantity,amount,Payment) VALUES (%s,%s,%s,%s,%s,%s,%s)",(emaill,t[1],t[5],t[6],t[7],t[8],"Pending"))
				con.commit()
				c.close()
	e.close()
	c=con.cursor()
	c.execute("select * from cart")
	for r in range(0,100):
		amt=c.fetchone()
		if amt is None:
			c.execute("select * from cart")
			data=c.fetchall()
			c.execute("select * from login")
			details=c.fetchall()
			amount=int(tot+(tot*.18))
			name=''
			phone=''
			c.execute("SELECT * FROM login")
			for r in range(0,100):
				a=c.fetchone()
				if a is None:
					break
				else:
					if a[1]==emaill:
						name=a[2]
						phone=a[3]
						break
			c.execute("select * from checkorder")
			for r in range(0,100):
				chk=c.fetchone()
				if chk is None:
					break
				else:
					if chk[0]==emaill:
						if chk[6]=="Paid":
							c.close()
							con.commit()
							return render_template('invoice.html',data=data,tot=tot,gst=int(tot*.18),amount=amount,details=details,email=emaill,name=name,phone=phone,paid=1,amountt=0)
			c.close()
			con.commit()
			return render_template('invoice.html',data=data,tot=tot,gst=int(tot*.18),amount=amount,details=details,email=emaill,name=name,phone=phone,paid=0)
		else:
			if amt[0]==emaill:
				tot=tot+int(amt[8])
	con.commit()
	c.close()
	return render_template('invoice.html',data=data)

@app.route('/updateinvoice',methods=["GET","POST"])
def updateinvoice():
	tot=0
	gst=0
	sid=request.form['id']
	c=con.cursor()
	c.execute("delete from checkorder where p_id=%s and id=%s",(emaill,sid))
	c.execute("delete from cart where p_id=%s and id=%s",(emaill,sid))
	c.execute("select * from cart")
	for r in range(0,100):
		amt=c.fetchone()
		if amt is None:
			c.execute("select * from cart")
			data=c.fetchall()
			c.execute("select * from login")
			details=c.fetchall()
			amount=int(tot+(tot*.18))
			name=''
			phone=''
			c.execute("SELECT * FROM login")
			for r in range(0,100):
				a=c.fetchone()
				if a is None:
					break
				else:
					if a[1]==emaill:
						name=a[2]
						phone=a[3]
						break
			c.execute("select * from checkorder")
			for r in range(0,100):
				chk=c.fetchone()
				if chk is None:
					break
				else:
					if chk[0]==emaill:
						if chk[6]=="Paid":
							c.close()
							con.commit()
							return render_template('invoice.html',data=data,tot=tot,gst=int(tot*.18),amount=amount,details=details,email=emaill,name=name,phone=phone,paid=1,amountt=0)
			c.close()
			con.commit()
			return render_template('invoice.html',data=data,tot=tot,gst=int(tot*.18),amount=amount,details=details,email=emaill,name=name,phone=phone,paid=0)
		else:
			if amt[0]==emaill:
				tot=tot+int(amt[8])
	con.commit()
	c.close()
	return render_template('invoice.html',data=data)

@app.route('/payment',methods=["GET","POST"])
def payment():
	return render_template('payment.html')
	
@app.route('/backinvoice',methods=["GET","POST"])
def backinvoice():
	tot=0
	gst=0
	c=con.cursor()
	c.execute("select * from cart")
	for r in range(0,100):
		amt=c.fetchone()
		if amt is None:
			c.execute("select * from cart")
			data=c.fetchall()
			c.execute("select * from login")
			details=c.fetchall()
			amount=int(tot+(tot*.18))
			name=''
			phone=''
			c.execute("SELECT * FROM login")
			for r in range(0,100):
				a=c.fetchone()
				if a is None:
					break
				else:
					if a[1]==emaill:
						name=a[2]
						phone=a[3]
						break
			con.commit()
			return render_template('invoice.html',data=data,tot=tot,gst=int(tot*.18),amount=amount,details=details,email=emaill,name=name,phone=phone,amountt=0,paid=1)
		else:
			if amt[0]==emaill:
				c.execute("UPDATE checkorder set Payment=%s WHERE p_id=%s",("Paid",emaill))
				tot=tot+int(amt[8])
	con.commit()
	c.close()
	return render_template('invoice.html',data=data)
	
@app.route('/stock',methods=["GET","POST"])
def stock():
	d=con.cursor()
	d.execute("select * from marble")
	marbleinfo=d.fetchall()
	d.execute("select * from granite")
	graniteinfo=d.fetchall()
	d.execute("select * from tiles")
	tilesinfo=d.fetchall()
	d.execute("select * from checkorder")
	orderinfo=d.fetchall()
	d.execute("select * from cart")
	cartinfo=d.fetchall()
	con.commit()
	d.close()
	return render_template('stock.html',marble=marbleinfo,granite=graniteinfo,tiles=tilesinfo,order=orderinfo,cart=cartinfo)

@app.route('/updatecart',methods=["GET","POST"])
def updatecart():
	d=con.cursor()
	pid=request.form['p_id']
	d.execute("delete from cart where p_id=%s",(pid))
	d.execute("delete from checkorder where p_id=%s",(pid))
	d.execute("select * from marble")
	marbleinfo=d.fetchall()
	d.execute("select * from granite")
	graniteinfo=d.fetchall()
	d.execute("select * from tiles")
	tilesinfo=d.fetchall()
	d.execute("select * from checkorder")
	orderinfo=d.fetchall()
	d.execute("select * from cart")
	cartinfo=d.fetchall()
	con.commit()
	d.close()
	return render_template('stock.html',marble=marbleinfo,granite=graniteinfo,tiles=tilesinfo,order=orderinfo,cart=cartinfo)
	
if __name__ == "__main__":
   app.run()
   
   
   
   
   
   
   