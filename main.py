import cv2 as cv
import mediapipe as mp 

if False :
    pass
import pyautogui
width = pyautogui.size().width
height = pyautogui.size().height
#print(width,height)

#pip install pyautogui


mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils 

def processImage(img):
    gray_image = cv.cvtColor(img,cv.COLOR_BGR2RGB)
    result = hands.process(gray_image)
    return result

def distance(item1,item2):
    return ((item1.x-item2.x)**2 + (item1.y-item2.y)**2)**0.5
#thumb,index,curser,pointer,pinkey
FINGER_TIPS = [4,8,12,16,20]

NEEDEDFINGERS =[ 16,20]
INDEX_FINGER = 8
THUMB =4
#base 
BASE = 0
wasTrue = False
shouldPrint = 0
dp = []
THRESHOLD =0.2
def draw_hand_connections(img,results):
    global shouldPrint
    global dp 
    global wasTrue 
    global THRESHOLD
    h,w,c = img.shape 
    if False:
        
        color = (0,0,0)
        for point in dp:
            cv.circle(img,point,10,color,cv.FILLED)

   
    if results.multi_hand_landmarks:
        if len(results.multi_handedness) > 0:
            pass
            #print( results.multi_handedness[0])

        for handLms in results.multi_hand_landmarks:
            #print(results.__dict__)
            tips = [handLms.landmark[i] for i in NEEDEDFINGERS ]
            tx = [t.x for t in tips]
            ty = [t.y for t in tips]

            base = handLms.landmark[BASE]
            tbm = handLms.landmark[THUMB]
            try:
                pass
                #print(base.z)
            except:
                print("\r FAILEED") 
            if False and shouldPrint <= 20:
                print(tx,ty)
                print(base.x,base.y)
                
                shouldPrint+=1
            findex = handLms.landmark[INDEX_FINGER]
            dists = [ distance(t,base) < THRESHOLD for t in tips ]
            draw = dists.count(True) ==2
            for i in range(len(tips)):
                item =tips[i]
                cx,cy = int(item.x*w),int(item.y*h)
                color = (0,255,0)
                if dists[i]:
                    color = (255,0,0)
                cv.circle(img,(cx,cy),10,color,cv.FILLED)

            #color base red regardless
            cx,cy = int(base.x*w),int(base.y*h)
            cv.circle(img,(cx,cy),10,(255,0,0),cv.FILLED)

            color = (255,0,0)
            
            cx,cy = int(findex.x*w),int(findex.y*h)
            if draw:
                if wasTrue and not distance(findex,base)<THRESHOLD:
                    dp = []
                    wasTrue = False 
                #dp.append((cx,cy))
                color = (0,0,255)
                cxp,cyp = int(findex.x*width),int(findex.y*height)
                cxp = width-cxp
                pyautogui.moveTo(cxp,cyp)
                if distance(tbm,base) < (THRESHOLD/1.5):
                    
                    color = (0,255,255)
                    pyautogui.click(cxp,cyp)
                    
            else:
                wasTrue = True 
            #color index blue regardless
            cv.circle(img,(cx,cy),10,color,cv.FILLED)
            

            

            


            if True:
                for id, lm in enumerate(handLms.landmark):
                   
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    color = None

                    if id in FINGER_TIPS:
                        color = (0,255,0)
                    if id == BASE:
                        color = (0,0,255)
                    if color != None:
                        cv.circle(img,(cx,cy),10,color,cv.FILLED)
                        mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
        
        return img 
def draw2(img,results):

    h,w,c = img.shape 
    if not results.multi_hand_landmarks:
        return 
    for handLms in results.multi_hand_landmarks:
        for id, lm in enumerate(handLms.landmark):
            
            cx,cy = int(lm.x*w),int(lm.y*h)
            color = None

            if id in FINGER_TIPS:
                color = (0,255,0)
            if id == BASE:
                color = (0,0,255)
            if color != None:
                cv.circle(img,(cx,cy),10,color,cv.FILLED)
                mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)
    return img 
    
def main():
    count = 0
    cam = cv.VideoCapture(0)
    while True:
        success, img = cam.read()
        if not success:
            continue
        results = processImage(img)
        if count ==0 and results :
            count+=1 
            print(str(results))
        #draw2(img,results)
        draw_hand_connections(img,results)
        cv.imshow("hands",cv.flip(img,1))
        if cv.waitKey(1) == ord('q'):
            cam.release()
            cv.destroyAllWindows()
main()