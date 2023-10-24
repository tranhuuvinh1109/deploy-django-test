from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project
from .serializers import ProjectSerializer
import cv2

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
def stream(name):
    video_url = ''
    if name == 'danang':
        video_url='https://firebasestorage.googleapis.com/v0/b/realtime-cnn.appspot.com/o/danang.mp4?alt=media&token=18e11ee5-2410-4cb0-8fa3-8fba80761e34'
    else:
        video_url='https://firebasestorage.googleapis.com/v0/b/realtime-cnn.appspot.com/o/highway.mp4?alt=media&token=faf701bb-26e4-4750-8dbc-eaa4d9db476d'
    # video_url = f".//media//{name}.mp4"
    cap = cv2.VideoCapture(video_url) 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


def video_stream(request, name):
    return StreamingHttpResponse(stream(name), content_type='multipart/x-mixed-replace; boundary=frame')
