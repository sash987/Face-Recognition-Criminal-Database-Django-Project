import cv2
from django.contrib import messages
from django.shortcuts import render,redirect
from face.forms import Criminal_form 
from face.models import *
import face_recognition
import numpy as np



def base(request):
    return render(request,'base.html')

def search(request):
    query=request.GET['query']
    criminal= Criminal_Face.objects.filter(name__icontains=query)
    params={'criminal': criminal}
    return render(request,"search.html", params)

def view_of_search(request):
    criminal = Criminal_Image.objects.all()
    return render(request,"search.html",{'criminal':criminal})

def create_record(request):
    if request.method == "POST":
        form = Criminal_form(request.POST,request.FILES)
        if form.is_valid():
            name=form.cleaned_data['name']
            fathers_name=form.cleaned_data['fathers_name']
            gender=form.cleaned_data['gender']
            age=form.cleaned_data['age']
            crime=form.cleaned_data['crime']
            crime_image=form.cleaned_data['crime_image']
            reg=Criminal_Face(name=name,fathers_name=fathers_name,gender=gender,age=age,crime=crime,crime_image=crime_image)
            reg.save()
            messages.success(request, 'Criminal record submitted successfully.')
            form = Criminal_form()
    else:
        form = Criminal_form()
    return render(request,'create_record.html',{'form':form }) #,'criminal': criminal })

# Create your views here.
def view(request):
    criminal = Criminal_Face.objects.all()
    return render(request,"view.html",{'criminal':criminal})

def delete(request, id):
    if request.method == 'POST' :
        pi=Criminal_Face.objects.get(pk=id)
        pi.delete()
        messages.error(request, 'Criminal record deleted successfully.')
        return redirect("/view/")


def edit(request, id):
    if request.method == 'POST' :
        pi = Criminal_Face.objects.get(id=id)
        pi.delete()
        form = Criminal_form(request.POST,request.FILES, instance=pi)
        if form.is_valid():
            form.save()
            messages.success(request, 'Criminal record updated successfully.')
    else:
        pi=Criminal_Face.objects.get(id=id)
        form=Criminal_form(instance=pi)
    return render(request,'updated_view.html',{'form':form})
    
def face_rec(request):
    return render(request,"face_rec.html")


def face_recognition_cam(request):
    video_capture = cv2.VideoCapture(0)
    # Load a sample picture and learn how to recognize it.

    afzal_guru_image = face_recognition.load_image_file("training_images/Afzal Guru/1.jpg")
    afzal_guru_face_encoding = face_recognition.face_encodings(afzal_guru_image)[0]

    arun_gawli_image = face_recognition.load_image_file("training_images/Arun Gawli/2.jpg")
    arun_gawli_face_encoding = face_recognition.face_encodings(arun_gawli_image)[0]

    dawood_ibrahim_image = face_recognition.load_image_file("training_images/Dawood Ibrahim/2.jpg")
    dawood_ibrahim_face_encoding = face_recognition.face_encodings(dawood_ibrahim_image)[0]

    haji_mastan_image = face_recognition.load_image_file("training_images/Haji Mastan/2.jpg")
    haji_mastan_face_encoding = face_recognition.face_encodings(haji_mastan_image)[0]

    nathuram_godse_image = face_recognition.load_image_file("training_images/Nathuram Godse/2.jpg")
    nathuram_godse_face_encoding = face_recognition.face_encodings(nathuram_godse_image)[0]

    veerappan_image = face_recognition.load_image_file("training_images/Veerappan/2.jpg")
    veerappan_face_encoding = face_recognition.face_encodings(veerappan_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        afzal_guru_face_encoding,
        arun_gawli_face_encoding,
        dawood_ibrahim_face_encoding,
        haji_mastan_face_encoding,
        nathuram_godse_face_encoding,
        veerappan_face_encoding
    ]

    known_face_names = [
        "Afzal Guru",
        "Arun Gawli",
        "Dawood Ibrahim",
        "Haji Mastan",
        "Nathuram Godse",
        "Veerappan",
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    output_faces = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                if name not in output_faces:
                    output_faces.append(name)

                face_names.append(name)

        process_this_frame = not process_this_frame

        #print(output_faces)
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video (PRESS \'Q\' TO CLOSE THE WINDOW) ', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    if "Unknown" in output_faces:
        output_faces.remove('Unknown')
    #print(output_faces)
    if len(output_faces) == 0 :
        return redirect("http://localhost:8000")
    a=output_faces[0]
    criminal= Criminal_Face.objects.filter(name__contains=a)
    return render(request,'search.html',{'criminal':criminal})
    

def face_recognition_video(request):
    #video_capture = cv2.VideoCapture(0)
    video_capture = cv2.VideoCapture('images/testing/modi.mp4')

    # Load a sample picture and learn how to recognize it.
    modi_image = face_recognition.load_image_file("images/modi_1.jpg")
    modi_face_encoding = face_recognition.face_encodings(modi_image)[0]

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        modi_face_encoding,
    ]

    known_face_names = [
        "Modi",
    ]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    output_faces = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                if name not in output_faces:
                    output_faces.append(name)

                face_names.append(name)

        process_this_frame = not process_this_frame

        #print(output_faces)
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video (PRESS \'Q\' TO CLOSE THE WINDOW) ', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    if "Unknown" in output_faces:
        output_faces.remove('Unknown')
    #print(output_faces)
    if len(output_faces) == 0 :
        return redirect("http://localhost:8000")
    a=output_faces[0]
    criminal= Criminal_Face.objects.filter(name__contains=a)
    return render(request,'search.html',{'criminal':criminal})
    


def face_recognition_img(request):
    # Load the jpg files into numpy arrays
    afzal_guru_image = face_recognition.load_image_file("training_images/Afzal Guru/1.jpg")
    arun_gawli_image = face_recognition.load_image_file("training_images/Arun Gawli/2.jpg")
    dawood_ibrahim_image = face_recognition.load_image_file("training_images/Dawood Ibrahim/2.jpg")
    haji_mastan_image = face_recognition.load_image_file("training_images/Haji Mastan/2.jpg")
    nathuram_godse_image = face_recognition.load_image_file("training_images/Nathuram Godse/2.jpg")
    veerappan_image = face_recognition.load_image_file("training_images/Veerappan/2.jpg")
    unknown_image = face_recognition.load_image_file("testing_images/Dawood Ibrahim.jpg")

    # Get the face encodings for each face in each image file
    # Since there could be more than one face in each image, it returns a list of encodings.
    # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
    try:
        afzal_guru_face_encoding = face_recognition.face_encodings(afzal_guru_image)[0]
        arun_gawli_face_encoding = face_recognition.face_encodings(arun_gawli_image)[0]
        dawood_ibrahim_face_encoding = face_recognition.face_encodings(dawood_ibrahim_image)[0]
        haji_mastan_face_encoding = face_recognition.face_encodings(haji_mastan_image)[0]
        nathuram_godse_face_encoding = face_recognition.face_encodings(nathuram_godse_image)[0]
        veerappan_face_encoding = face_recognition.face_encodings(veerappan_image)[0]
        unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    except IndexError:
        print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
        quit()

    known_faces = [
        afzal_guru_face_encoding,
        arun_gawli_face_encoding,
        dawood_ibrahim_face_encoding,
        haji_mastan_face_encoding,
        nathuram_godse_face_encoding,
        veerappan_face_encoding
    ]

    known_face_names = [
        "Afzal Guru",
        "Arun Gawli",
        "Dawood Ibrahim",
        "Haji Mastan",
        "Nathuram Godse",
        "Veerappan",
    ]

    # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
    results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    name="Unknown"
    i=0
    x=True
    for result in results :
        if (result):
            name=known_face_names[i]
        i=i+1
    
    criminal= Criminal_Face.objects.filter(name__contains=name)
    return render(request,'search.html',{'criminal':criminal})
    #return render(request,'img_face_reg_demo.html')

