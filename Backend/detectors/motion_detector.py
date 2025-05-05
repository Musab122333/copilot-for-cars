
"""
Motion Detector Module
Detects abnormal motion using frame differencing
"""

import cv2
import numpy as np


class MotionDetector:
    """Motion detector class using frame differencing"""
    
    def __init__(self, threshold=25, min_area=5000, blur_size=21):
        """
        Initialize motion detector
        
        Args:
            threshold: Threshold for frame difference binarization
            min_area: Minimum contour area to consider as motion
            blur_size: Size of Gaussian blur kernel for noise reduction
        """
        self.threshold = threshold
        self.min_area = min_area
        self.blur_size = blur_size
        self.prev_gray = None
        
        print(f"Motion Detector initialized with threshold={threshold}, min_area={min_area}")
    
    def set_prev_frame(self, frame):
        """
        Set the previous frame for motion detection
        
        Args:
            frame: BGR image as numpy array
        """
        # Convert to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.prev_gray = cv2.GaussianBlur(gray, (self.blur_size, self.blur_size), 0)
    
    def detect(self, frame):
        """
        Detect motion in current frame
        
        Args:
            frame: BGR image as numpy array
        
        Returns:
            List of (x, y, w, h) coordinates for motion areas
        """
        # If no previous frame, set it and return no motion
        if self.prev_gray is None:
            self.set_prev_frame(frame)
            return []
        
        # Convert current frame to grayscale and blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (self.blur_size, self.blur_size), 0)
        
        # Compute absolute difference between the current and previous frames
        frame_diff = cv2.absdiff(self.prev_gray, gray)
        
        # Apply threshold to get binary image
        _, thresh = cv2.threshold(frame_diff, self.threshold, 255, cv2.THRESH_BINARY)
        
        # Dilate the thresholded image to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Process contours
        motion_areas = []
        for contour in contours:
            # Filter by area
            if cv2.contourArea(contour) < self.min_area:
                continue
            
            # Get bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)
            motion_areas.append((x, y, w, h))
        
        # Update previous frame
        self.prev_gray = gray
        
        return motion_areas
