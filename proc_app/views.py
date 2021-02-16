from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from .forms import UserInput
from .models import Candidate,Candidate_Proc

from threading import Thread
import cv2
import cv2
import face_recognition
from gaze_tracking import GazeTracking
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
c=0
name1,email1,title1=None,None,None
# Create your views here.
#send_mail(subject, message, sender, recipients)
def index(request):
    return render(request,'index.html')
def input(request):
    context={}
    context['form']=UserInput()
    return render(request,'regi.html',context)
def testinput(request):
    return render(request,'test_input.html')

def reg(request):
    if request.method=='POST':
        form=UserInput(request.POST,request.FILES)
        if form.is_valid():
            name=form.cleaned_data.get('name')
            last=form.cleaned_data.get('last_name')
            gmail=form.cleaned_data.get('Gmail')
            pic=form.cleaned_data.get('picture')
            try:
                a=Candidate.objects.get(gmail=gmail)
                return HttpResponse('User Already Exist with this mail')
            except:
                obj=Candidate(
                    first_name=name, 
                    last_name=last,
                    gmail=gmail,
                    picture=pic
                )
                obj.save()
                return HttpResponse("User Registration Done!")
            
    #send_mail('Thanks You For Registration', 'Your registration is done', 'rajsuryvanshi72@gmail.com', [gmail])
    return HttpResponse("Invalid Inputs")


def veri(request):
     results=None
     global name1
     global email1
     global title1
     try:

        if request.method=='POST':
            gmail=request.POST['gmail']
            a=Candidate.objects.get(gmail=gmail)
            name1=a.first_name
            title1=a.last_name
            email1=gmail
            known_image = face_recognition.load_image_file(a.picture)
            cap=cv2.VideoCapture(0)
            while(1):
                ret,pic=cap.read()
                if cv2.waitKey(0):
                    cv2.imwrite('testimage.jpg',pic)
                    print('image done')
                    break
            cap.release()
            unknown_image = face_recognition.load_image_file("testimage.jpg")
            biden_encoding = face_recognition.face_encodings(known_image)[0]
            unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

            results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
            print(results)
        if results[0]==True:
            return render(request,'start_test.html')
        else:
            return render(request,"user_invalid.html")
     except:
         return render(request,"user_invalid.html")

    
def start_cam():
    global webcam
    global gaze
    global c
    while True:
    # We get a new frame from the webcam
        _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
        gaze.refresh(frame)

        frame = gaze.annotated_frame()
        text = ""
        
        if gaze.is_blinking():
            text = "Blinking"
        elif gaze.is_right():
            c+=1
            text = "Looking right"
        elif gaze.is_left():
            c+=1
            text = "Looking left"
        elif gaze.is_center():
            text = "Looking center"

        cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)

        left_pupil = gaze.pupil_left_coords()
        right_pupil = gaze.pupil_right_coords()
        cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
        cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

        cv2.imshow("Demo", frame)
        if cv2.waitKey(1) == 27:
            webcam.release()
            cv2.destroyWindow("Demo")
            print("In cam",c)
            obj=Candidate_Proc(
                    first_name=name1, 
                    last_name=title1,
                    gmail=email1,
                    Gaze_Score=c//11
                )
            obj.save()
            break
def stop(request):
    global webcam
    global c
    webcam.release()
    cv2.destroyAllWindows()
    obj=Candidate_Proc(
                    first_name=name1, 
                    last_name=title1,
                    gmail=email1,
                    Gaze_Score=c//11
                )
    obj.save()
    print("in stop",c)
    return HttpResponseRedirect('home')

def startproc(request):

    """
    Demonstration of the GazeTracking library.
    Check the README.md for complete documentation.
    """
    Thread(target = start_cam).start()
    return render(request,'test_page.html')