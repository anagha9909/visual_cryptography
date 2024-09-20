import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import time
import cv2
import numpy as np
from PIL import Image
from flask import Flask, render_template, request, redirect, session, send_file
from Dbconnection import Db
app = Flask(__name__)
app.secret_key="abc"
static_path=r"D:\visual_cryptography\visual_cryptography\static\\"


@app.route('/demo')
def demo():
    return render_template('user/demoooooooo.html')


@app.route('/',methods=['get','post'])
def login():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        db=Db()
        a=db.selectOne("select * from login where username='"+username+"' and password='"+password+"'")
        if a is not None:
            if a['usertype']=='admin':
                session['u_email']=username
                session['log']="log"
                return redirect('/admin_home')
            elif a['usertype']=='user':
                session['log'] = "log"
                session['u_id']=a['login_id']
                session['u_email']=username
                return redirect('/user_home')
            else:
                return '''<script>alert("USER NOT FOUND");window.location="/"</script>'''
        else:
            return '''<script>alert("USER NOT FOUND");window.location="/"</script>'''

    else:
     return render_template('login.html')

@app.route('/admin_home')
def admin_home():
    return render_template('admin/blank-page.html')

@app.route('/view_user')
def view_user():
        db=Db()
        a=db.select("select * from user  ")
        return render_template('admin/viewuser.html',data=a)

@app.route('/view_complaint')
def view_complaint():
    db=Db()
    a=db.select("select * from complaint where reply='pending'")
    return render_template('admin/viewcomplaint.html',data=a)

@app.route('/forget_password',methods=['get','post'])
def forget_password():
    if request.method == "POST":
        username = request.form['mail']
        db = Db()
        a = db.selectOne("select * from login where username='" + username + "'")
        if a is not None:
            if a['usertype'] == 'admin':
                session['u_email'] = username
                session['log'] = "log"
                return redirect('/change_password1')
            elif a['usertype'] == 'user':
                session['log'] = "log"
                session['u_id'] = a['login_id']
                session['u_email'] = username
                if a is not None:

                    otp = random.randint(0000, 9999)
                    print(username)
                    session['otp'] = otp
                    print(session['otp'])

                    try:
                        gmail = smtplib.SMTP('smtp.gmail.com', 587)

                        gmail.ehlo()

                        gmail.starttls()

                        gmail.login('cryptographyvisual01@gmail.com', 'Rsss@123')

                    except Exception as e:
                        print("Couldn't setup email!!" + str(e))

                    msg = MIMEText("Your OTP Is " + str(otp))

                    msg['Subject'] = 'AUTHENTICATION'

                    msg['To'] = username

                    msg['From'] = 'cryptographyvisual01@gmail.com'

                    try:

                        gmail.send_message(msg)

                    except Exception as e:

                        print("COULDN'T SEND EMAIL", str(e))

                return redirect('/otp_verify')
            else:
                return '''<script>alert("USER NOT FOUND");window.location="/"</script>'''
        else:
            return '''<script>alert("USER NOT FOUND");window.location="/"</script>'''

    else:
        return render_template('forgetpasssword.html')
@app.route('/change_password1',methods=['get','post'])
def change_password1():
    if request.method == "POST":

        newp = request.form['textfield2']
        conf_p = request.form['textfield3']
        db = Db()


        if newp==conf_p:
                db=Db()
                db.update("update login set password='"+newp+"' where username='" + str(session['u_email']) + "'")
                return  '''<script>alert("password changed successfully");window.location="/"</script>'''
        else:
                return '''<script>alert("confirm password not matching");window.location="/change_password1"</script>'''

    else:
        return render_template('CHANGEPASSWORD.html')
@app.route('/otp_verify',methods=['get','post'])
def otp_verify():
    if request.method == "POST":
        otp=request.form["textfield"]
        print(otp,session['otp'])
        c=str(session['otp'])
        if otp==c:

            return '''<script>alert("AUTHENTICATION IS SUCCESSFUL");window.location="/change_password1"</script>'''
        else:
            return '''<script>alert('failed');window.location="/otp_verify"</script>'''

    return render_template('OTPVERIFY.html')


@app.route('/send_reply/<id>',methods=['get','post'])
def send_reply(id):
    if request.method=="POST":
        reply=request.form['textarea']
        db=Db()
        db.update("update complaint set reply='"+reply+"',replydate=curdate() where complaintid='"+id+"'")
        return '''<script>alert("REPLY ADDED");window.location="/view_complaint"</script>'''
    else:
        return render_template('admin/sendreply.html')



@app.route('/change_password',methods=['get','post'])
def change_password():
    if request.method == "POST":
        password = request.form['textfield']
        newp = request.form['textfield2']
        conf_p = request.form['textfield3']
        db = Db()
        a = db.selectOne("select * from login where password='" + password + "' and usertype='admin'")
        if a is not None:
            if newp==conf_p:
                db=Db()
                db.update("update login set password='"+newp+"' where usertype='admin'")
                return  '''<script>alert("password changed successfully");window.location="/"</script>'''
            else:
                return '''<script>alert("confirm password not matching");window.location="/change_password"</script>'''
        else:
            return '''<script>alert("wrong credentials");window.location="/change_password"</script>'''
    else:
        return render_template('admin/changepassword.html')

@app.route('/user_change_password',methods=['get','post'])
def user_change_password():
    if  session['log']=="log":
            if request.method == "POST":
                password = request.form['textfield']
                newp = request.form['textfield2']
                conf_p = request.form['textfield3']
                db = Db()
                a = db.selectOne("select * from login where password='" + password + "' and usertype='user' and login_id='"+str(session['u_id'])+"'")
                if a is not None:
                    if newp==conf_p:
                        db=Db()
                        db.update("update login set password='"+newp+"' where usertype='user' and login_id='"+str(session['u_id'])+"'")
                        return  '''<script>alert("password changed successfully");window.location="/"</script>'''
                    else:
                        return '''<script>alert("confirm password not matching");window.location="/user_change_password"</script>'''
                else:
                    return '''<script>alert("wrong credentials");window.location="/user_change_password"</script>'''
            else:
                return render_template('user/changepassword.html')
    else:
        return redirect('/')


############################################user

@app.route('/user_home')
def user_login():

    return render_template('user/blank-page.html')


@app.route('/user_reg',methods=['get','post'])
def user_reg():
    if request.method == "POST":
        username = request.form['textfield']
        email = request.form['textfield2']
        phoneno = request.form['textfield3']
        password = request.form['textfield4']
        confirmpassword = request.form['textfield5']
        date=time.strftime("%Y%m%d_%H%M%S")+".jpg"
        img=request.files['filefield']
        img.save(static_path+"user_imgs\\"+date)
        path="/static/user_imgs/"+date
        db=Db()
        q1=db.selectOne("select * from login where username='"+email+"'")
        if q1 is  None:
                p=db.insert("insert into login values('','"+email+"','"+confirmpassword+"','user')")
                a=db.insert("insert into user values('"+str(p)+"','"+username+"','"+email+"','"+phoneno+"', '"+path+"' )")
                return  '''<script>alert("successfully registered");window.location="/"</script>'''
        else:
            return '''<script>alert("Already registered email");window.location="/user_reg"</script>'''

    return render_template('user/userreg.html')


@app.route('/view_profile',methods=['get','post'])
def view_profile():
    if request.method == "POST":
        db = Db()
        b = db.selectOne("select * from user where uloginid = '" + str(session['u_id']) + "' ")
        return render_template('user/editprofile.html', data=b)
    else :
        db=Db()
        b=db.selectOne("select * from user where uloginid = '"+str(session['u_id'])+"' ")
        return render_template('user/viewprofile.html',data=b)


@app.route('/edit_profile',methods=['post'])
def edit_profile():
    username=request.form["textfield"]
    email = request.form["textfield2"]
    Phoneno = request.form["textfield3"]
    db=Db()
    b=db.update("update user set username='"+username+"',email='"+email+"',Phoneno='"+Phoneno+"' where uloginid='"+str(session['u_id'])+"'")
    return '''<script>alert("Updated");window.location="/view_profile"</script>'''



@app.route('/otp',methods=['get','post'])
def otp():
    if request.method == "POST":
        otp=request.form["textfield"]
        print(otp,session['otp'])
        c=str(session['otp'])
        if otp==c:

            return '''<script>alert("AUTHENTICATION IS SUCCESSFUL");window.location="/"</script>'''
        else:
            return '''<script>alert('failed');window.location="/otp"</script>'''

    return render_template('user/otp.html')

@app.route('/otp_login',methods=['get','post'])
def otp_login():
    if request.method == "POST":
        otp=request.form["textfield"]
        print(otp,session['otp'])
        c=str(session['otp'])
        if otp==c:

            return '''<script>alert("AUTHENTICATION IS SUCCESSFUL");window.location="/user_home"</script>'''
        else:
            return '''<script>alert('failed');window.location="/otp_login"</script>'''

    return render_template('user/otp_login.html')
@app.route('/user_complaint',methods=['get','post'])
def user_complaint():
     if request.method == "POST":
            complaint=request.form["textarea"]
            db=Db()
            db.insert("insert into complaint values(null,'"+str(session['u_id'])+"','"+complaint+"',curdate(),'PENDING','PENDING')")
            return '''<script>alert("complaint sent successfully");window.location="/user_home"</script>'''
     else:
        return render_template('user/complaint.html')


@app.route('/view_form')
def view_form():
        db= Db()
        a = db.select("select * from upload where userid = '" + str(session['u_id']) + "'  ")
        return render_template('user/viewform.html', data=a)
@app.route('/view_reply')
def view_reply():
        db=Db()
        a = db.select("select * from complaint where userid = '" + str(session['u_id']) + "'  ")
        return render_template('user/viewreply.html',data=a)

@app.route('/logout')
def logout():
    session['log']=""
    session.clear()
    return redirect('/')

@app.route('/upload',methods=['get','post'])
def upload():
    if request.method == "POST":
        email=session['u_email']
        file = request.files["fileField"]
        varr=file
        print(varr,file)
        title = request.form["textfield"]

        ext = str(file.filename).split(".")[-1]
        dt = time.strftime("%Y%m%d_%H%M%S")



        file.save(static_path+"temp\\a."+ext)
        fname=""
        pswd=random.randint(1000,9999)

        img_path = static_path + "temp\\a." + ext
        img = Image.open(img_path)

        im = Image.open(static_path + "temp\\a." + ext)
        im.save(static_path + "orggg\\" + dt + '.' + ext)
        var2 = "/static/orgg/" + dt + '.' + ext
        img_data = img.load()
        #
        # print(img.size)
        width = img.size[0]
        height = img.size[1]

        R_share = Image.new('RGB', img.size)
        G_share = Image.new('RGB', img.size)
        B_share = Image.new('RGB', img.size)

        pix_R_share = R_share.load()
        pix_G_share = G_share.load()
        pix_B_share = B_share.load()

        for i in range(width):
            for j in range(height):
                print("HHHHHHHHHH  ", i, j)
                pix_data = img_data[i, j]
                R, G, B = pix_data
                pix_R_share[i, j] = (R, 0, 0)
                pix_G_share[i, j] = (0, G, 0)
                pix_B_share[i, j] = (0, 0, B)
        R_share.save(static_path + "server1\\" + dt + ".png")
        G_share.save(static_path + "server2\\" + dt + ".png")
        B_share.save(static_path + "server3\\" + dt + ".png")
        from  imageshuffle import imageshuffle
        img_R = Image.open(static_path + "server1\\" + dt + ".png")
        img_G = Image.open(static_path + "server2\\" + dt + ".png")
        img_B = Image.open(static_path + "server3\\" + dt + ".png")
        ar_R = np.asarray(img_R)
        ar_G = np.asarray(img_G)
        ar_B = np.asarray(img_B)
        key = pswd
        s = imageshuffle.Rand(key)
        enc_R = s.enc(ar_R)
        enc_G = s.enc(ar_G)
        enc_B = s.enc(ar_B)
        img_R = Image.fromarray(enc_R)
        img_G = Image.fromarray(enc_G)
        img_B = Image.fromarray(enc_B)
        img_R.save(static_path + "server1\\" + dt + ".png")
        img_G.save(static_path + "server2\\" + dt + ".png")
        img_B.save(static_path + "server3\\" + dt + ".png")
        path = "/static/server1/" + dt + ".png"
        print(pswd)
        print("keyyyyyyyyyy",key)
        db = Db()
        db.insert("insert into upload values(null,'" + str(session['u_id']) + "','" + path + "',curdate(),'image','1','" + title + "','" + str(var2) + "')")
        # try:
        #     gmail = smtplib.SMTP('smtp.gmail.com', 587)
        #
        #     gmail.ehlo()
        #
        #     gmail.starttls()
        #
        #     gmail.login('anaghabalan22@gmail.com', 'qivjjgzglqzxjgys')
        #
        # except Exception as e:
        #     print("Couldn't setup email!!" + str(e))
        #
        # msg = MIMEText("Your file secret key is",str(key))
        #
        # msg['Subject'] = 'AUTHENTICATION'
        #
        # msg['To'] = email
        #
        # msg['From'] = 'anaghabalan22@gmail.com'
        #
        # try:
        #
        #     gmail.send_message(msg)
        #     print("kkkkkkk")
        #
        # except Exception as e:
        #     print("COULDN'T SEND EMAIL", str(e))

        import smtplib
        s1 = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s1.starttls()
        s1.login("anaghabalan22@gmail.com", "qivjjgzglqzxjgys")
        msg = MIMEMultipart()  # create a message.........."
        msg['From'] = "anaghabalan22@gmail.com"
        msg['To'] = email
        msg['Subject'] ="eLock"
        body = "Your Password is:- - " + str(key)
        msg.attach(MIMEText(body, 'plain'))
        s1.send_message(msg)
        return '''<script>alert("Uploaded successfully");window.location="/user_home"</script>'''
    return render_template('user/upload.html')


@app.route('/get_file/<fid>',methods=['get','post'])
def get_file(fid):
    if request.method == "POST":
        secretkey = request.form["textfield"]
        file=request.files["BROWSE"]
        db=Db()
        a=db.selectOne("select * from upload where   fileid='"+fid+"' ")
        orgg_pth=a['path']
        orgg_fname=orgg_pth.split("/")[3]
        print("HHH   ", orgg_fname)
        orgg_file=cv2.imread(static_path+"orggg\\"+orgg_fname)
        if a is not None:
            db_filename=a['file']
            fname="/static/server1/"+file.filename
            if fname==db_filename:
                db_type=a['type']
                db_no_of_page=a['no_of_page']
                if str(db_type)== "image":
                    name=db_filename.split('/')[-1]
                    share1_path=static_path+"server1\\"+name
                    share2_path=static_path+"server2\\"+name
                    share3_path=static_path+"server3\\"+name
                    img_share1 = Image.open(share1_path)
                    img_share2 = Image.open(share2_path)
                    img_share3 = Image.open(share3_path)
                    share1_data = img_share1.load()
                    share2_data = img_share2.load()
                    share3_data = img_share3.load()
                    width = img_share1.size[0]
                    height =img_share1.size[1]
                    ar_sh1 = np.asarray(img_share1)
                    ar_sh2 = np.asarray(img_share2)
                    ar_sh3 = np.asarray(img_share3)
                    from  imageshuffle import imageshuffle
                    key=secretkey
                    s = imageshuffle.Rand(key)
                    enc_R = s.dec(ar_sh1)
                    enc_G = s.dec(ar_sh2)
                    enc_B = s.dec(ar_sh3)
                    img_sh1 = Image.fromarray(enc_R)
                    img_sh2 = Image.fromarray(enc_G)
                    img_sh3 = Image.fromarray(enc_B)
                    # unshuffled images
                    img_sh1.save(static_path + "temp2\\share1_" + name)
                    img_sh2.save(static_path + "temp2\\share2_" + name)
                    img_sh3.save(static_path + "temp2\\share3_" + name)

                    img_share1 = Image.open(static_path + "temp2\\share1_" + name)
                    img_share2 = Image.open(static_path + "temp2\\share2_" + name)
                    img_share3 = Image.open(static_path + "temp2\\share3_" + name)
                    share1_data = img_share1.load()
                    share2_data = img_share2.load()
                    share3_data = img_share3.load()

                    orig = Image.new('RGB', img_share1.size)

                    pix_img = orig.load()


                    for i in range(width):
                        for j in range(height):
                            pix_data1 = share1_data[i, j]
                            pix_data2 = share2_data[i, j]
                            pix_data3 = share3_data[i, j]
                            R1, G1, B1 = pix_data1
                            R2, G2, B2 = pix_data2
                            R3, G3, B3 = pix_data3
                            pix_img[i, j] = (R1, G2, B3)
                    orig.save(static_path + "temp2\\" + name)
                    img_final=cv2.imread(static_path + "temp2\\" + name)
                    psnr=PSNR(orgg_file, img_final)
                    print("--------------------")
                    print("PSNR value : ", psnr)
                    return send_file(static_path + "temp2\\"+name , as_attachment=True)

            else:
                return '''<script>alert("invalid share");window.location="/view_form"</script>'''
        else:
            return '''<script>alert("file removed");window.location="/view_form"</script>'''
    return render_template('user/getfile.html')



def PSNR(firstImage,secondImage):
    target_data = firstImage.astype(float)
    ref_data = secondImage.astype(float)
    diff = ref_data - target_data
    diff = diff.flatten('C')
    rmse = np.math.sqrt(np.mean(diff ** 2.))
    print("RMSE  ", rmse)
    if rmse == 0:
        return rmse
    else:
        psnrResultValue = 20 * np.math.log10(255. / rmse)
        print("PSNR:", + psnrResultValue)
        return psnrResultValue

def send_mail(message, email):
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)

        gmail.ehlo()

        gmail.starttls()

        gmail.login('anaghabalan22@gmail.com', 'qivjjgzglqzxjgys')

    except Exception as e:
        print("Couldn't setup email!!" + str(e))

    msg = MIMEText(message)

    msg['Subject'] = 'AUTHENTICATION'

    msg['To'] = email

    msg['From'] = 'anaghabalan22@gmail.com'

    try:

        gmail.send_message(msg)

    except Exception as e:

        print("COULDN'T SEND EMAIL", str(e))
    return "ok"


if __name__ == '__main__':
    app.run(port=1234)
