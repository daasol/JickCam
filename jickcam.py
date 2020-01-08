#미리 깔아주어야 하는 패키지 3가지
# 1. numpy
# 2. opencv-python
# 3. opencv-conrtib-python : 오브젝트 트레킹 패키지가 포함되어있어서 깔아주어야함.

import cv2
import numpy as np

video_path = 'girlfriend.mp4'
capture = cv2.VideoCapture(video_path) #비디오를 읽는 함수

output_size =(375, 667) #비디오를 저장할 사이즈 스마트폰 풀사이즈
                        #이하 비디오 저장을 위한 opencv 설정
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('%s_output.mp4'%(video_path.split('.')[0]), fourcc, capture.get(cv2.CAP_PROP_FPS), output_size)
#mp4코덱으로 저장.
#파일 이름으로 저장, 코덱, FPS (1초당 몇 프레임) < 우리가 불러온 프레임으로 저장한다, 사이즈는 output_size로 저장.



if not capture.isOpened() : #윈도우에 비디오를 가져옴
    exit()

tracker = cv2.TrackerCSRT_create() #적당히 정확도와 속도가 높음

ret, img = capture.read() #첫번째 프레임을 img에 저장한다.
cv2.namedWindow('Select Window') #ROI를 셋팅하는 윈도우의 이름을 Select Window라고 할것
cv2.imshow('Select Window', img) #ROT를 설정하는 Select Window의 프레임을 보여줘

rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
cv2.destroyWindow('Select Window')
                #Select Window에서 ROT를 설정, 이미지의 센터에서 시작하지 말고, 중심점을 보여라 (과녁)
                #첫번째 프레임이 뜨고, 추적하고 싶은 물체에 사각형을 지정해줌. ROI 셋팅 끗

#ROI를 설정한을 트래커함, rect로 설정한 부분을 쫓아감.
#ROI가 영상을 넘어가는 경우 (영상이 너무 작거나, ROI사이즈가 너무 크거나 ) 에러가 남 --> 예외처리 해줘야함.
tracker.init(img, rect)

while True : #여기서 이미지를 프레임마다 읽고, rect를 따라가는 ROI와 계속 비교함.
    ret, img = capture.read()

    if not ret : #비디오를 모두 읽어서 끝났을 때 ret이 false가 된다.
        exit()

    success, box = tracker.update(img) #트레킹한 내용 success(트래킹 결과를 boolean), box(트래킹 결과를 rect)

    left, top, width, height = [int(v) for v in box]
    #output_size만큼으로 ROI 사각형만큼 조절하기.
    center_x = left +width / 2
    center_y = top + height /2

    result_top = int(center_y -output_size[1] /2)
    result_bottom = int(center_y +output_size[1] /2)
    result_left = int(center_x - output_size[0]/2)
    result_right= int(center_x + output_size[0]/2)

    #result_img = img[result_top:result_bottom, result_left:result_right]
    #새로 저장할 영상에 네모 rect가 같이 저장되므로 없애주기 위하여 원래 이미지에 copy함수를 씀 (rect가 없어짐)
    result_img = img[result_top:result_bottom, result_left:result_right].copy()
    out.write(result_img)
    cv2.rectangle(img, pt1=(left, top), pt2=(left+width, top+height), color=(255, 255, 255), thickness=2)
    #box에서 for문을 돌린 후 나온 v의 값을 integer로 변환한 후, 차례로 윈 위 넓이 높이 순으로 넣어라.

    cv2.imshow('result_img', result_img)
    if cv2.waitKey(1) ==ord('q') :
        break

    cv2.imshow('img', img)
    if cv2.waitKey(1) == ord('q') :#1초의 딜레이가 있어야 윈도우에 잘 표시가 된다. 그렇지 않으면 윈도우 백그라운드에서 돌다가 꺼져버림
        break

# ROI셋팅: 사용자가 관심있는 영역을 지정해줘야함, opencv가 지원함.