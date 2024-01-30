# views.py
from django.shortcuts import render
from joblib import load
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from base64 import b64encode, b64decode

# Load the pre-trained model
model = load('./savedModels/model.joblib')

# Create your views here.
@login_required(login_url='login')

def HomePage(request):
    return render (request,'home.html')

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect(predictor)
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')

def BytesToInt(b):
    return int.from_bytes(b, byteorder='big')

def predictor(request):
    return render(request, 'main.html')

def formInfo(request):
    # Load the key for decryption
    with open('./Notebooks/encryption_key.txt', 'rb') as key_file:
        key = key_file.read()
    # Get user input from the form

    age = float(request.GET['age'])
    sex = float(request.GET['sex'])
    bmi = float(request.GET['bmi'])
    children = float(request.GET['children'])
    smoker = float(request.GET['smoker'])
    region = float(request.GET['region'])

    # Make predictions using the model
    input_data = np.array([[age, sex, bmi, children, smoker, region]]) 
    healthcare_charges = model.predict(input_data)[0]  

    # Pass the prediction to the result template
    context = {'healthcare_charges': healthcare_charges}
    print(healthcare_charges)
    
    return render(request, 'result.html', context)