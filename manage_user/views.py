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
    video_url = f".//media//{name}.mp4"
    cap = cv2.VideoCapture(video_url) 

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: failed to capture image")
            break
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


def video_feed(request, name):
    return StreamingHttpResponse(stream(name), content_type='multipart/x-mixed-replace; boundary=frame')





# def Home(request, name):
#     video_path = f"D:\\My Project\\Django\\deploy_django\\media\\{name}.mp4"
#     try:
#         cam = VideoCamera(video_path)
#         toggle = request.GET.get("toggle", "false")
#         toggle = toggle.lower() == "true"
#         if toggle:
#             print(">>true: ", toggle)
#             cam.toggle_play(True)
#         else:
#             print(">>false: ", toggle)
#             cam.toggle_play(False)  # Pause video
#         return StreamingHttpResponse(gen(cam, toggle), content_type="multipart/x-mixed-replace;boundary=frame")
#     except:
#         pass
#     return render(request, 'manage_user/app1.html')

# class VideoCamera(object):
#     def __init__(self, video_url):
#         self.video_url = video_url
#         self.backSub = cv2.createBackgroundSubtractorMOG2()
#         self.is_playing = True  # Initialize video playback as True
#         self.stop_requested = True  # Flag to request stopping the loop
#         self.capture_video()

#     def capture_video(self):
#         self.video = cv2.VideoCapture(self.video_url)
#         (self.grabbed, self.frame) = self.video.read()
#         threading.Thread(target=self.update, args=()).start()

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         image = self.frame
#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()

#     def update(self):
#         while True:
#             if self.is_playing:
#                 roi = self.frame[340:1120, 700:1200]
#                 fgMask = self.backSub.apply(roi)
#                 fgMask = cv2.cvtColor(fgMask, 0)
#                 kernel = np.ones((5, 5), np.uint8)
#                 fgMask = cv2.erode(fgMask, kernel, iterations=1)
#                 fgMask = cv2.dilate(fgMask, kernel, iterations=1)
#                 fgMask = cv2.GaussianBlur(fgMask, (3, 3), 0)
#                 fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
#                 _, fgMask = cv2.threshold(fgMask, 130, 255, cv2.THRESH_BINARY)

#                 fgMask = cv2.Canny(fgMask, 20, 200)
#                 contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#                 for i in range(len(contours)):
#                     (x, y, w, h) = cv2.boundingRect(contours[i])
#                     area = cv2.contourArea(contours[i])
#                     if area > 1200:
#                         cv2.drawContours(fgMask, contours[i], 0, (0, 0, 255), 6)
#                         cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 print('--->', self.is_playing)

#                 (self.grabbed, self.frame) = self.video.read()
#             else:
#                 print('BREAK ----', self.stop_requested)
#                 break
#             if self.is_playing == False:
#                 self.video.release()
#                 break
#         print("pausing....", self.is_playing)

#     def toggle_play(self, is_playing):
#         self.is_playing = is_playing
#         if not is_playing:
#             self.stop_requested = False
#             self.video.release()

# def gen(camera, toggle):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
#         if not toggle:
#             break
# class VideoCamera(object):
#     def __init__(self):
#         self.video_url = "https://firebasestorage.googleapis.com/v0/b/orderfood-5a6b6.appspot.com/o/highway.mp4?alt=media&token=267712b6-6b1f-47e8-9893-aa3b6e4c9dba&_gl=1*1316xqm*_ga*MjkzMTI0NDY1LjE2OTU3OTY4MzY.*_ga_CW55HF8NVT*MTY5Nzg2ODU0NC4yNS4x.LjE2OTc4Njg5MTAuMjEuMC4w"
#         self.backSub = cv2.createBackgroundSubtractorMOG2()
#         self.is_playing = True  # Initialize video playback as True
#         self._playback_position = 0  # Initialize playback position
#         self.capture_video()

#     def capture_video(self):
#         self.video = cv2.VideoCapture(self.video_url)
#         (self.grabbed, self.frame) = self.video.read()
#         threading.Thread(target=self.update, args=()).start()

#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         image = self.frame
#         _, jpeg = cv2.imencode('.jpg', image)
#         return jpeg.tobytes()

#     def update(self):
#         while True:
#             if not self.is_playing:
#                 continue  # Pause video when is_playing is False

#             # Set the video capture position based on playback_position
#             self.video.set(cv2.CAP_PROP_POS_FRAMES, self.playback_position)

#             roi = self.frame[340:1120, 700:1200]
#             fgMask = self.backSub.apply(roi)
#             fgMask = cv2.cvtColor(fgMask, 0)

#             kernel = np.ones((5, 5), np.uint8)
#             fgMask = cv2.erode(fgMask, kernel, iterations=1)
#             fgMask = cv2.dilate(fgMask, kernel, iterations=1)
#             fgMask = cv2.GaussianBlur(fgMask, (3, 3), 0)
#             fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
#             _, fgMask = cv2.threshold(fgMask, 130, 255, cv2.THRESH_BINARY)

#             fgMask = cv2.Canny(fgMask, 20, 200)
#             contours, _ = cv2.findContours(fgMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#             for i in range(len(contours)):
#                 (x, y, w, h) = cv2.boundingRect(contours[i])
#                 area = cv2.contourArea(contours[i])
#                 if area > 1200:
#                     print(area)
#                     cv2.drawContours(fgMask, contours[i], 0, (0, 0, 255), 6)
#                     cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)

#             # Get the updated playback position
#             self.playback_position = int(self.video.get(cv2.CAP_PROP_POS_FRAMES))

#             (self.grabbed, self.frame) = self.video.read()

#     def toggle_play(self, is_playing):
#         self.is_playing = is_playing

#     # @property
#     def playback_position(self):
#         return self._playback_position

#     # @playback_position.setter
#     def playback_position(self, value):
#         self._playback_position = value
#         if self._playback_position < 0:
#             self._playback_position = 0

#     def get_playback_position(self):
#         return self.playback_position

# # Home view
# def Home(request):
#     toggle = request.GET.get("toggle", "false")  # Get the "toggle" query parameter
#     toggle = toggle.lower() == "true"  # Convert the value to a boolean

    

#     try:
#         cam = VideoCamera()
#         if toggle:
#             print(">>true: ", toggle)
#             cam.toggle_play(True)  # Start or resume video
#         else:
#             print(">>false: ", toggle)
#             cam.toggle_play(False)  # Pause video
#         return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
#     except:
#         pass
#     return render(request, 'app1.html')

# # Generator function
# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')