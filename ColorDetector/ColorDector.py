import numpy as np 
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import cv2
clicked  = False
colorname = r =g =b='None'
def predictionModel(data):
    global color
    #  when n =1 it has high precision , and as increases precision decreases . 
    neigh = KNeighborsClassifier(n_neighbors=1)
    #selecting Only Required Attribute
    y = color['Color_Name']
    x = color.drop(['Color_Name'], axis = 1)
    # Knn Fitting 
    neigh.fit(x, y)
    Knn_Res = neigh.predict((data))
    return Knn_Res

def selectDataset():
    global color
    indexes = ['Color','Color_Name','HexVal','R','G','B'] 
    color = pd.read_csv('resources/colors.csv',names= indexes)
    color.drop(['Color','HexVal'],axis=1 ,inplace=True)
    return

def getRGB(event,x,y,flags,param):
    global clicked,colorname,r,g,b,color;
    if event == cv2.EVENT_LBUTTONDBLCLK:
        clicked = True
        img,model = param
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)
        selectDataset()
        if model == 1:
            data = np.array([r,b,g])
            colorname =predictionModel([data])  
            colorname = "".join(map(str,colorname))
        elif model ==2:
            minimum = 10000
            for i in range(len(color)):
                d = abs(r- int(color.loc[i,"R"])) + abs(g- int(color.loc[i,"G"]))+ abs(b- int(color.loc[i,"B"]))
                if(d<=minimum):
                    minimum = d
                    colorname = color.loc[i,"Color_Name"] 
        
        return 
    
def getColorName(img,x,y,model):
    global clicked,colorname,r,g,b,color;
    b,g,r = img[y,x]
    b = int(b)
    g = int(g)
    r = int(r)
    selectDataset()
    if model == 1:
        data = np.array([r,b,g])
        colorname =predictionModel([data])  
        colorname = "".join(map(str,colorname))
    elif model ==2:
        minimum = 10000
        for i in range(len(color)):
            d = abs(r- int(color.loc[i,"R"])) + abs(g- int(color.loc[i,"G"]))+ abs(b- int(color.loc[i,"B"]))
            if(d<=minimum):
                minimum = d
                colorname = color.loc[i,"Color_Name"] 
    return 
        
        

def ColorDetector(image,xValue,yValue,model):
    global clicked,colorname,r,g,b
    
    frame  = cv2.imread(image)
    frame = cv2.resize(frame,(1200,700))
    # cv2.imshow("Color Detector",frame)
    # params = [frame,model]
    # cv2.setMouseCallback('Color Detector',getRGB,params)
    getColorName(frame,xValue,yValue,model)
    cv2.destroyAllWindows()
    return (colorname,r,g,b)
    # while True:
    #     if 0xFF ==27:
    #         cv2.destroyAllWindows()
    #         return (colorname,r,g,b)
    #     else:
    #         cv2.waitKey(1)
        
    # while True:
    #     if clicked or 0xFF ==27:
    #         clicked = False
    #         cv2.destroyAllWindows()
    #         return (colorname,r,g,b)
    #     else:
    #         cv2.waitKey(1)
     
    