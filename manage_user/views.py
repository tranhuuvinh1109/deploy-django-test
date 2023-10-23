from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project
from .serializers import ProjectSerializer
import cv2
import threading
import numpy as np

@api_view(['POST'])
def create_new_project(request):
    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_all_projects(request):
    if request.method == 'GET':
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

def Home(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'app1.html')

def get_image(request):
    # cam = VideoCamera()
    # image = cam.get_frame()
    # return JsonResponse({'image': image.decode('utf-8')})
    cam = VideoCamera()
    image = cam.get_frame()
    return HttpResponse(image, content_type="image/jpeg")

class VideoCamera(object):
    def __init__(self):
        video_url = "https://firebasestorage.googleapis.com/v0/b/orderfood-5a6b6.appspot.com/o/highway.mp4?alt=media&token=267712b6-6b1f-47e8-9893-aa3b6e4c9dba&_gl=1*1316xqm*_ga*MjkzMTI0NDY1LjE2OTU3OTY4MzY.*_ga_CW55HF8NVT*MTY5Nzg2ODU0NC4yNS4x.LjE2OTc4Njg5MTAuMjEuMC4w"
        self.video = cv2.VideoCapture(video_url)
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        # self.fps = self.video.get(cv2.CAP_PROP_FPS)  # Get the FPS of the video
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            roi = self.frame[340:1120, 700:1200]
            fgMask = self.backSub.apply(roi)
            fgMask = cv2.cvtColor(fgMask, 0)

            kernel = np.ones((5, 5), np.uint8)
            fgMask = cv2.erode(fgMask, kernel, iterations=1)
            fgMask = cv2.dilate(fgMask, kernel, iterations=1)
            fgMask = cv2.GaussianBlur(fgMask, (3, 3), 0)
            fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
            _, fgMask = cv2.threshold(fgMask, 130, 255, cv2.THRESH_BINARY)

            fgMask = cv2.Canny(fgMask, 20, 200)
            contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for i in range(len(contours)):
                (x, y, w, h) = cv2.boundingRect(contours[i])
                area = cv2.contourArea(contours[i])
                if area > 1200:
                    print(area)
                    cv2.drawContours(fgMask, contours[i], 0, (0, 0, 255), 6)
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
