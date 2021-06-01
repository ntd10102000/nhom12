from flask import Flask,render_template,request,redirect,session
import psycopg2
from db import connection,cursor
import os
import json

app = Flask(__name__)
app.secret_key = "abc"

@app.route('/')
def index():
    sql = "select * from tbl_sp limit 6"
    cursor.execute(sql)
    record = cursor.fetchall()    
    sql = "select * from tbl_sp where id_sp = 33"
    cursor.execute(sql)
    record1 = cursor.fetchall() 
    sql = "select * from tbl_sp where id_sp = 34"
    cursor.execute(sql)
    record2 = cursor.fetchall()     
    return render_template("index.html", r=record, r1=record1, r2=record2)



#@app.route('/')
#def index():
   
    #sql = "select * from sinhvien"

    # Executing a SQL query
   # cursor.execute(sql)
    # Fetch result
    #record = cursor.fetchall()

    #s = "<h1 style='color:red'>Xin chào</h1>"
    
    #return render_template("index.html",r=record)

@app.route("/product")
def product():
    if "username" in session:
        id_sp = request.args.get("id_sp", type = int)
        sql = "select * from tbl_sp"
        cursor.execute(sql)
        record = cursor.fetchall()
        print(record)
        return render_template("ad_product.html",r=record, id_sp=id_sp)
    else:
        return redirect("/login")

@app.route("/insert")
def insert():
    if "username" in session:
        return render_template("insert.html")
    else:
        return redirect("/login")

@app.route("/themmoi",methods=["POST"])
def themmoi():
    if "username" in session:
        ten_sp = request.form.get("ten_sp")
        gia_sp = request.form.get("gia_sp")
        link_anh = ""
        for uploaded_file in request.files.getlist("link_anh"):
            if uploaded_file.filename != "":
                link_anh = uploaded_file.filename
                print(uploaded_file.filename)
                uploaded_file.save(os.path.join("static/images", uploaded_file.filename))

        sql = f"insert into tbl_sp(ten_sp,gia_sp,link_anh) values( N'{ten_sp}', {gia_sp},'../static/images/{link_anh}')"

        # Executing a SQL query
        cursor.execute(sql)
        
        connection.commit()

        return redirect("/product")
    else:
        return redirect("/login")

@app.route("/delete")
def delete():
    if "username" in session:
        id_sp = request.args.get("id_sp", type = int)
        
        sql = f"delete from tbl_sp where id_sp ={id_sp}"

        # Executing a SQL query
        cursor.execute(sql)
        
        connection.commit()

        return redirect("/product")
    else:
        return redirect("/login")



# @app.route("/update<id>")
# def update(id):
#     sanpham = 
#     return render_template("update.html" , sanpham = sanpham)

@app.route("/update",methods=["POST"])
def sua():
    if "username" in session:
        id_sp = request.args.get("id_sp", type = int)
        ten_sp = request.form.get("ten_sp")
        gia_sp = request.form.get("gia_sp")
        link_anh = ""
        for uploaded_file in request.files.getlist("link_anh"):
            if uploaded_file.filename != "":
                link_anh = uploaded_file.filename
                print(uploaded_file.filename)
                uploaded_file.save(os.path.join("static/images", uploaded_file.filename))
    
        sql = f"update tbl_sp set ten_sp='{ten_sp}',gia_sp={gia_sp},link_anh= '../static/images/{link_anh}' where id_sp={id_sp}"

        # Executing a SQL query
        cursor.execute(sql)
        
        connection.commit()

        return redirect("/product")
    else:
        return redirect("/login")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_dn",methods=["POST"])
def login_dn():
    us = request.form.get("us")
    pa = request.form.get("pa")

    sql = "select * from tbl_user where user_name = '"+us+"' and pass_word='"+pa+"'"
    cursor.execute(sql)
    # Fetch result
    record = cursor.fetchall()
    if(len(record)==1):
        session["username"] = us
        return redirect("/product")
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/dangki",methods=["POST"])
def dangki():
    user_name = request.form.get("user_name")
    pass_word = request.form.get("pass_word")

    sql = "insert into tbl_user(user_name,pass_word) values( N'"+user_name+"',  N'"+pass_word+"')"

    # Executing a SQL query
    cursor.execute(sql)
    
    connection.commit()

    return redirect("/login")

@app.route("/shop", methods=["GET"])
def shop():
    keyword = request.args.get("search", type = str)
    max_s = request.args.get("max", type = int)
    min_s = request.args.get("min", type = int)
    sql = f"SELECT * FROM tbl_sp;"
    if keyword != None:
        sql = f"select * from tbl_sp WHERE ten_sp LIKE N'%{keyword}%';"
    elif max_s != None and min_s != None:
        sql = f"select * from tbl_sp WHERE gia_sp BETWEEN '{min_s}' AND '{max_s}';"
    cursor.execute(sql)
    record = cursor.fetchall()
    if record:
        err = ""
    else:
        err = f"Không tìm thấy sản phẩm nào chứa '{keyword}'"
    connection.commit()
    return render_template("shop.html", r = record, err = err)

@app.route("/maps")
def maps():
    cursor.execute("select title, address, time, img, long, lat from db_maps")
    version = cursor.fetchall() 
    geo_json = []
    for row in version:
        geo_json.append({
            "loc": [row[5], row[4]],
            "title": row[0],
            "address": row[1],
            "time": row[2],
            "img": row[3]
        })
    # cursor.close()
    return render_template("maps.html", data = json.dumps(geo_json))

@app.route("/collection")
def collection():
    sql = "select * from tbl_sp where id_sp = 33"
    cursor.execute(sql)
    record1 = cursor.fetchall() 
    sql = "select * from tbl_sp where id_sp = 34"
    cursor.execute(sql)
    record2 = cursor.fetchall()
    return render_template("collection.html", r1 = record1, r2 = record2)

@app.route("/shoes")
def shoes():
    sql = "select * from tbl_sp limit 6"
    cursor.execute(sql)
    record = cursor.fetchall()
    return render_template("shoes.html", r = record)

@app.route("/racing_boots")
def racing_boots():
    return render_template("racing_boots.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")