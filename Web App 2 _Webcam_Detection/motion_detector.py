import cv2, time, pandas
from datetime import datetime

first_frame = None # variable to store the first frame
status_list = [None,None]
times = []
df = pandas.DataFrame(columns=['Start','End'])

video = cv2.VideoCapture(1) # triggered camera

while True:
    check, frame = video.read() # read first frame as soon as the camera triggers (image w/out while loop)
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # converting to grap image
    # apply so that can blur the image smoothly to remove noise and increase accuracy in the calculation of the difference
    gray = cv2.GaussianBlur(gray,(21,21),0) # tupple w/ para. of blurriness and 0 for std dev

    # script will run, video will be triggered and then the while loop will start to run and it get the first frame of the VideoCapture
    # this will be stored in the frame variable (beside check), and will convert it to a gray frame and assign that gray numpy to the first_frame variable
    if first_frame is None:
        first_frame = gray
        continue # continue back to the beginning of the loop and DON'T to the rest of the code

    # compare the first frame of the image with the current frame
    delta_frame = cv2.absdiff(first_frame, gray)

    # cv2.threshold method returns 2 index tupple
    # [0] -> [1st value = value needed when using other threshold methods (suggests value for threshold)]
    # [1] -> [2nd value = actual frame that is returned from the threshold method]
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1] # frame, threshold limit is 30, what color assigned: white -> 255 OR black -> 0, threshold method (reserach the diff methods)

    # remove the black holes from big white areas in the image
    # smooth threshold Frame
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2)

    # find contours of dilated threshold frame
    # 2 methods:
    #   (1) find contours - find contours in image and store them in a tuple
    #   (2) draw contours - draws contours in an image
    # find the contours and check if the area of the contour
    # (copy of the frame, draw external contours of objects found in the frame, approx. method that opencv will apply for it reading the numbers)
    (cnts,_) = cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # keep only certain contours above a certain areas
    for contour in cnts:
        if cv2.contourArea(contour) < 100000:
            continue
        status = 1
        # create rectangle moving contour
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3)
    status_list.append(status)

    status_list = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    cv2.imshow('First Frame', gray)
    cv2.imshow('Delta Frame', delta_frame)
    cv2.imshow('Threshold Frame', thresh_frame)
    cv2.imshow('Color Frame', frame)

    key = cv2.waitKey(1)

    if key == ord('q'): # asking for key from keyboard user
        if status == 1:
            times.append(datetime.now())
        break

print(status_list)
print(times)

for i in range(0,len(times),2):
    df = df.append({'Start': times[i], 'End': times[i+1]}, ignore_index = True)

df.to_csv('Times.csv')

video.release()
cv2.destroyAllWindows
