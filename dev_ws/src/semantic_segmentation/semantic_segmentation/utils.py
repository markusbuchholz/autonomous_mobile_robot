from collections import OrderedDict
import numpy as np
import cv2
import math

def convert_state_dict(state_dict):
    """Converts a state dict saved from a dataParallel module to normal
       module state_dict inplace
       :param state_dict is the loaded DataParallel model_state
    """
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = k[7:]  # remove `module.`
        new_state_dict[name] = v
    return new_state_dict

def takeSecond(elem):
    return elem[1]

def find_nearest_idx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

def segmented2scan(warped_img, warped_center):
    h,w,_ = warped_img.shape
    pixel_per_meter_x = (w - 2*100)/2.7 #Horizontal distance between src points in the real world ( I assumed 4 meters)
    pixel_per_meter_y = (h - 2*100)/8.0 #Vertical distance between src points in the real world ( I assumed 20 meters)
    lower_limit = np.array([50,50,50])
    upper_limit = np.array([200, 200, 200])
    mask = cv2.inRange(np.uint8(warped_img), lower_limit, upper_limit)

    contours, hierarchy = cv2.findContours(mask*200,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #contours_warped = warped_img.copy()
    for contour in contours:
        cv2.drawContours(warped_img, contour, -1, (0, 255, 0), 3)

    # Detect distances and angles to points in contour
    scan_distances = []
    scan_angles = []
    for contour in contours:
        for point in contour:
            distance = math.sqrt(((point[0][0]-warped_center[0])/pixel_per_meter_x)**2 + ((point[0][1]-warped_center[1])/pixel_per_meter_y)**2)
            angle = -math.atan2((point[0][0] - warped_center[0])/pixel_per_meter_x, (warped_center[1]-point[0][1])/pixel_per_meter_y)
            scan_distances.append(distance)
            scan_angles.append(angle)
    
    #arrange contour data
    scan_array = np.array(([scan_distances, scan_angles])).T
    scan_list = list(scan_array)
    scan_list.sort(key=takeSecond)
    scan_array = np.array(scan_list)
    #Resample data to form scan_data
    angle_range = [-50.0, 50.0]
    angle_increment = 0.5
    scan_distances = []
    max_distance = 15.0
    scan_angles = []
    if scan_array.shape[0]>20:
        for angle in np.arange(angle_range[0], angle_range[1], angle_increment):
            rads = angle*math.pi/180.0
            scan_angles.append(rads)
            idx = find_nearest_idx(scan_array[:,1], rads)
            if(scan_array[idx,0] < max_distance):
                scan_distances.append(scan_array[idx,0])
            else:
                scan_distances.append(0.0)
    return scan_distances, angle_increment*math.pi/180.0
    #print("hello")
    
    