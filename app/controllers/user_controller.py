from flask import render_template, redirect, url_for, request, redirect, flash
from flask_login import current_user, login_user, logout_user, login_required
from ..models.models import User,Key
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

class UserController:
    @login_required
    def profile(self):
        a=RSA()
        user = current_user
        key = Key.query.filter_by(username=user.username).first()
        d,n=int(key.d),int(key.n)
        b=decrypted_user(user.id,a.decrypt(user.fullname,d,n),user.username,a.decrypt(user.email,d,n),a.decrypt(user.user_type,d,n))

        return render_template("profile.html", user=b)
