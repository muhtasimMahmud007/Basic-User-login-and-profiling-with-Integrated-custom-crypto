from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import User,Key
from datetime import datetime
from ..extensions import db
import sympy
class Inverse_mod:
  def __init__(self):
    pass

  def inverse_mod(self,a,b):
    if sympy.gcd(a,b)!=1:
        return "Impossible"
    r1=a
    r2=b
    g=r1//r2
    r=r1%r2
    t1=0
    t2=1
    t=t1-g*t2
    #print(g,r1,r2,r,t1,t2,t)
    while(r!=0):
      r1=r2
      r2=r
      t1=t2
      t2=t
      g=r1//r2
      r=r1%r2
      t=t1-g*t2

      #print(g,r1,r2,r,t1,t2,t)
    if t2<0:
      return t2+a
    return t2

class RSA:
  def __init__(self):
    pass
  def PubPri_generate(self):
    p = sympy.randprime(2**127, 2**128)
    q = sympy.randprime(2**127, 2**128)

    while q == p:
        q = sympy.randprime(2**127, 2**128)

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = sympy.randprime(2**20,2**24)
    inverse=Inverse_mod()
    d=inverse.inverse_mod(phi_n,e)
    return n,e,d
  
  def encrypt(self,massage,e,n):
      m = int(massage.encode("utf-8").hex(),16)
      return str(pow(m,e,n))
  def decrypt(self,cipher,d,n):
    m = pow(int(cipher),d,n)
    return bytes.fromhex(hex(m)[2:]).decode('utf-8')


class decrypted_user:
    def __init__(self,id,fullname,username,email,user_type):
        self.id = id
        self.fullname = fullname
        self.username = username
        self.email = email
        self.user_type = user_type
        self.is_active=True

# class RSA:
#     def __init__(self):
#         self.p=177769235309576172295977201645684439211
#         self.q=327611503085735285490699287447298257467
#         self.e=11
#         self.d=37061338606836737607019368854217371339027413322507567951439618479346439953911
#         self.n = self.p * self.q
#     def encrypt(self,massage):
#         m = int(massage.encode("utf-8").hex(),16)
#         c = pow(m,self.e,self.n)
#         return str(c)
#     def decrypt(self,cipher):
#         m = pow(int(cipher),self.d,self.n)
#         return bytes.fromhex(hex(m)[2:]).decode('utf-8')
class AuthController:
    def login(self):
        if request.method == "POST":
            if current_user.is_authenticated:
                return redirect(url_for("home"))

            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).first()

            if user is None:
                flash("Username not found", "error")
                return redirect(url_for("auth.login"))
            elif user.match_password(password):
                # b=decrypted_user(user.id,a.decrypt(user.fullname),a.decrypt(user.username),a.decrypt(user.email),a.decrypt(user.user_type))
                login_user(user, remember=True)
                flash("Logged in successfully!", "success")
                return redirect(url_for("user.profile"))
            else:
                flash("Wrong Password", "error")
                return redirect(url_for("auth.login"))

        return render_template("login.html")

    def register(self):
        a=RSA()
        n,e,d=a.PubPri_generate()
        if current_user.is_authenticated:
            return redirect(url_for("user.profile", username=current_user.username))

        if request.method == "POST":
            name = request.form.get("name")
            username = request.form.get("username")
            email = request.form.get("email")
            password1 = request.form.get("password1")
            password2 = request.form.get("password2")
            user_type = request.form.get("user_type")

            if password1 != password2:
                flash("Passwords do not match", "error")
                return redirect(url_for("auth.register"))

            if User.query.filter_by(username=username).first():
                flash("Username already exists", "error")
                return redirect(url_for("auth.register"))

            if User.query.filter_by(email=a.encrypt(email,e,n)).first():
                flash("Email already exists", "error")
                return redirect(url_for("auth.register"))

            if password1 != password2:
                flash("Passwords do not match", "error")
                return redirect(url_for("auth.register"))

            if len(password1) < 4:
                flash("Password must be at least 4 characters", "error")
                return redirect(url_for("auth.register"))

            
            user = User(
                    fullname=a.encrypt(name,e,n),
                    username=username,
                    email=a.encrypt(email,e,n),
                    password=password1,
                    user_type=a.encrypt(user_type,e,n)
                )
            key=Key(
               username=username,
               e=str(e),
               d=str(d),
               n=str(n)
            )
            

            db.session.add(user)
            db.session.commit()
            db.session.add(key)
            db.session.commit()

            login_user(user, remember=True)

            # flash("Account created successfully!", "success")

            return redirect(url_for("user.profile"))

        return render_template("register.html")

    @login_required
    def update_password(self):
        if request.method == "POST":
            old_password = request.form.get("old_password")

            password1 = request.form.get("password1")
            password2 = request.form.get("password2")

            if password1 != password2:
                # flash("Passwords do not match", "error")
                return redirect(url_for("auth.update_password"))

            if not current_user.match_password(old_password):
                # flash("Old password is incorrect", "error")
                return redirect(url_for("auth.update_password"))

            if len(password1) < 4:
                # flash("Password must be at least 4 characters", "error")
                return redirect(url_for("auth.register"))

            current_user.password = password1

            db.session.commit()

            return redirect(url_for("user.profile"))

        return render_template("update_password.html")

    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for("auth.login"))
