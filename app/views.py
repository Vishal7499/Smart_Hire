from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from app.verify import authentication, review_prediction, suggest_doctor
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from datetime import datetime
import cv2
from keras.models import load_model
from time import sleep
from keras_preprocessing.image import img_to_array
from keras.preprocessing import image
import numpy as np
from .models import *
from .form import feedback_form
from django.http import HttpResponse,StreamingHttpResponse
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators import gzip
import threading


face_classifier = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
classifier = load_model('models/model.h5')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
emotion_result = None
word_count = {}
highest_expression = None
labels = []
lock = threading.Lock()

# Create your views here.
def index(request):
    # return HttpResponse("This is Home page")    
    return render(request, "index.html")

def log_in(request):
    if request.method == "POST":
        # return HttpResponse("This is Home page")  
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, "Log In Successful...!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid User...!")
            return redirect("log_in")
    # return HttpResponse("This is Home page")    
    return render(request, "log_in.html")

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        password = request.POST['password']
        password1 = request.POST['password1']
        # print(fname, contact_no, ussername)
        verify = authentication(fname, lname, password, password1)
        if verify == "success":
            user = User.objects.create_user(username, password, password1)          #create_user
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Your Account has been Created.")
            return redirect("/")
            
        else:
            messages.error(request, verify)
            return redirect("register")
    # return HttpResponse("This is Home page")    
    return render(request, "register.html")


@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def log_out(request):
    logout(request)
    messages.success(request, "Log out Successfuly...!")
    return redirect("/")

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def dashboard(request):
    context = {
        'fname' : request.user.first_name,
        'lname' : request.user.last_name,
    }
    return render(request, "dashboard.html", context)

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def feedback(request):
    context = {
        'fname' : request.user.first_name,
        'lname' : request.user.last_name,
        'form' : feedback_form(),
        'word_count': word_count,
    }
    if request.method == "POST":
        form = feedback_form(request.POST, request.FILES)
        if form.is_valid():
            q1 = form.cleaned_data['q1']
            q2 = form.cleaned_data['q2']
            q3 = form.cleaned_data['q3']
            q4 = form.cleaned_data['q4']
            q5 = form.cleaned_data['q5']
            q6 = form.cleaned_data['q6']
            q7 = form.cleaned_data['q7']
            q8 = form.cleaned_data['q8']
            q9 = form.cleaned_data['q9']
            q10 = form.cleaned_data['q10']
            q11 = form.cleaned_data['q11']
            q12 = form.cleaned_data['q12']
            q13 = form.cleaned_data['q13']
            q14 = form.cleaned_data['q14']
            q15 = form.cleaned_data['q15']
            
            feedback = review_prediction(q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15)
            list1 = [q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,q11,q12,q13,q14,q15]
            total = sum([eval(x) for x in list1])
            feedback_percentage = total/15
            feedback_percentage = round(feedback_percentage,2)
            username = request.user
            name = request.user.first_name + " " + request.user.last_name
            # Update the highest_expression and word_count values
            with lock:
                analyze_emotions()
            
            if highest_expression == '':
                doctor = suggest_doctor()
            else:
                doctor = {'-' : '-'}
            happiness_index = analysis(user_name= username, name =name, q1 = q1,q2 = q2,q3 = q3,q4 = q4,q5 = q5,q6 = q6,q7 = q6,q8 = q8,q9 = q9,q10 = q10,q11 = q11,q12= q12,q13 = q13,q14 = q14,q15 = q15, feedback = feedback, analysis_count = word_count, highest_expression = highest_expression, doc = doctor)
            happiness_index.save()
            messages.success(request, "Exam Submitted!!!")
            # Clear the emotion_result
            with lock:
                emotion_result.clear()
            return redirect("result")

        else:
            messages.error(request, "Invalid Form")
            return redirect("feedback")
    return render(request, "feedback.html", context)

def process_frame(frame):
    global emotion_result
    global labels
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            prediction = classifier.predict(roi)[0]
            label = emotion_labels[prediction.argmax()]
            labels.append(label)
            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame, labels


@gzip.gzip_page
def video_feed(request):
    return StreamingHttpResponse(get_frame(), content_type='multipart/x-mixed-replace; boundary=frame')




def analyze_emotions():
    global word_count
    global highest_expression
    global emotion_result
    global labels
    print(labels)
    for label in labels:
        if label in word_count:
            word_count[label] += 1
        else:
            word_count[label] = 1

    total_words = len(labels)

    for word, count in word_count.items():
        average = count / total_words
        average = average * 100
        average = round(average, 2)
        d = {word: average}
        word_count.update(d)

    if word_count:
        highest_percentage = max(word_count.values())
        highest_emotion = max(word_count, key=word_count.get)
        if highest_emotion == "Sad" or highest_emotion == "Fear":
            highest_expression = "Nervousness Detected!!"
        else:
            highest_expression = "Nervousness Not Detected!!"

                        
def get_frame():
    global emotion_result

    cap = cv2.VideoCapture(0)

    while True:
        _, frame = cap.read()

        processed_frame, labels = process_frame(frame)

        with lock:
            emotion_result = labels

        _, jpeg = cv2.imencode('.jpg', processed_frame)
        frame_bytes = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    cap.release()


def cam_capture(request):
    t = threading.Thread(target=analyze_emotions)
    t.daemon = True
    t.start()

    return render(request, 'cam_capture.html')

@login_required(login_url="log_in")
@cache_control(no_cache = True, must_revalidate = True, no_store = True)
def result(request):
    face_analysis = analysis.objects.last()
    print(face_analysis.doc)
    doctor = eval(face_analysis.doc)
    user_details = eval(face_analysis.analysis_count)
    context = {
        'fname': request.user.first_name,
        'face_analysis' : face_analysis,
        'user_details' : user_details,
        'doctor' : doctor
        }
    
    return render(request, "result.html",context)