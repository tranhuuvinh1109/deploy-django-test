from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Project
from .serializers import ProjectSerializer
import cv2
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
def stream(name):
    video_url = f".//media//{name}.mp4"
    cap = cv2.VideoCapture(video_url)
    if not cap.isOpened():
        print("Không thể mở video từ URL.")
        return
    backSub = cv2.createBackgroundSubtractorMOG2()

    while True:
        ret, frame = cap.read()
        roi = frame[340: 1120, 700:1200]
        if not ret:
            print("Error: failed to capture image")
            break
        fgMask = backSub.apply(roi)
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
                cv2.drawContours(fgMask, contours[i], 0, (0, 0, 255), 6)
                cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
        _, jpeg = cv2.imencode('.jpg', frame)
        print("Image")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


def video_stream(request, name):
    return StreamingHttpResponse(stream(name), content_type='multipart/x-mixed-replace; boundary=frame')

# import ffmpeg
# def stream(name):
#     # video_url = f"./media/highway.mp4"
#     video_url='https://firebasestorage.googleapis.com/v0/b/realtime-cnn.appspot.com/o/highway.mp4?alt=media&token=faf701bb-26e4-4750-8dbc-eaa4d9db476d'
#     cap = cv2.VideoCapture(video_url)

#     process = (
#         ffmpeg
#         .input('pipe:', format='rawvideo', pix_fmt='bgr24', s='{}x{}'.format(int(cap.get(3)), int(cap.get(4))))
#         .output('pipe:', format='rawvideo', pix_fmt='yuv420p')
#         .run_async(pipe_stdin=True, pipe_stdout=True)
#     )

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             print("Error: failed to capture image")
#             break

#         # Giảm chất lượng của frame
#         # Ví dụ: resize frame xuống cỡ 640x480
#         frame = cv2.resize(frame, (640, 480))

#         # Chuyển frame sang định dạng rawvideo để gửi qua ffmpeg
#         in_frame = frame[:, :, ::-1].tobytes()

#         # Gửi frame qua ffmpeg
#         process.stdin.write(in_frame)

#         # Đọc frame tiếp theo
#         _, jpeg = cv2.imencode('.jpg', frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

#     # Kết thúc quá trình ffmpeg khi hết video
#     process.stdin.close()

# def video_stream(request, name):
#     return StreamingHttpResponse(stream(name), content_type='multipart/x-mixed-replace; boundary=frame')