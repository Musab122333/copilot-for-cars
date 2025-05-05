"""
YOLOv8 Detector Module
Handles object detection using YOLOv8
"""

from ultralytics import YOLO
import numpy as np
import torch


class YOLODetector:
    """YOLOv8 object detector class"""
    
    def __init__(self, model_path="yolov8n.pt", conf_threshold=0.5, classes_to_detect=None):
        """
        Initialize YOLOv8 detector
        
        Args:
            model_path: Path to YOLOv8 model weights
            conf_threshold: Confidence threshold for detections
            classes_to_detect: List of class names to detect, None for all classes
        """
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.classes_to_detect = classes_to_detect
        
        # Get class names from model
        self.class_names = self.model.names
        
        # Convert class names to indices if specific classes are requested
        self.class_indices = None
        if self.classes_to_detect:
            self.class_indices = []
            for class_name in self.classes_to_detect:
                for idx, name in self.class_names.items():
                    if name.lower() == class_name.lower():
                        self.class_indices.append(idx)
        
        # Print initialization info
        print(f"YOLOv8 Detector initialized with model: {model_path}")
        print(f"Confidence threshold: {conf_threshold}")
        if self.classes_to_detect:
            print(f"Detecting classes: {self.classes_to_detect}")
        else:
            print("Detecting all classes")
    
    def detect(self, frame):
        """
        Perform object detection on a frame
        
        Args:
            frame: BGR image as numpy array
        
        Returns:
            List of dictionaries with detection info
        """
        # Run inference
        results = self.model.predict(
            frame, 
            conf=self.conf_threshold,
            classes=self.class_indices,
            verbose=False
        )
        
        # Extract detections
        detections = []
        
        if results and len(results) > 0:
            # Get boxes
            boxes = results[0].boxes
            
            # Extract and filter detections
            for i in range(len(boxes)):
                # Get box coordinates
                box = boxes.xyxy[i].cpu().numpy()
                x1, y1, x2, y2 = map(int, box)
                
                # Get confidence and class
                conf = float(boxes.conf[i].cpu().numpy())
                cls = int(boxes.cls[i].cpu().numpy())
                label = self.class_names[cls]
                
                # Add detection to list
                detections.append({
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                    'confidence': conf,
                    'class_id': cls,
                    'label': label
                })
        
        return detections
    
    def get_class_name(self, class_id):
        """Get class name from class ID"""
        return self.class_names.get(class_id, "unknown")
