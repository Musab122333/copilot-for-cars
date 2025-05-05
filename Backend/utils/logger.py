"""
Logger Module
Handles logging of detections and events
"""

import csv
import time
from datetime import datetime


class Logger:
    """Logger for detection events"""
    
    def __init__(self, log_file_path):
        """
        Initialize logger with log file path
        
        Args:
            log_file_path: Path to log file
        """
        self.log_file_path = log_file_path
        
        # Create and initialize CSV file with headers
        with open(self.log_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp', 
                'event_type', 
                'object_class', 
                'confidence',
                'notes'
            ])
        
        print(f"Logger initialized. Logging to {log_file_path}")
    
    def log_detection(self, object_class, confidence, notes=""):
        """
        Log an object detection event
        
        Args:
            object_class: Detected object class name
            confidence: Detection confidence score
            notes: Additional notes
        """
        self._write_log('detection', object_class, confidence, notes)
    
    def log_motion(self, notes=""):
        """
        Log a motion detection event
        
        Args:
            notes: Additional notes
        """
        self._write_log('motion', 'motion', 1.0, notes)
    
    def log_event(self, event_type, notes=""):
        """
        Log a general event
        
        Args:
            event_type: Type of event
            notes: Additional notes
        """
        self._write_log(event_type, '', 0.0, notes)
    
    def _write_log(self, event_type, object_class, confidence, notes):
        """
        Write an entry to the log file
        
        Args:
            event_type: Type of event
            object_class: Detected object class
            confidence: Detection confidence
            notes: Additional notes
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        try:
            with open(self.log_file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    timestamp,
                    event_type,
                    object_class,
                    f"{confidence:.4f}",
                    notes
                ])
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def close(self):
        """Close the logger (currently a no-op)"""
        pass  # Nothing to do, as we open/close the file for each write
