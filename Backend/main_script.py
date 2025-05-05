"""
Computer Vision Co-pilot - Main Application
Detects objects, tracks motion, and alerts on abnormal activity using YOLOv8
"""

import cv2
import time
import argparse
import numpy as np
from pathlib import Path

# Import local modules
from detectors.yolo_detector import YOLODetector
from detectors.motion_detector import MotionDetector
from utils.alert_system import AlertSystem
from utils.logger import Logger
from utils.config import load_config


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="AI Co-pilot Detection System")
    parser.add_argument('--config', type=str, default='config.yaml', 
                        help='Path to configuration file')
    parser.add_argument('--camera', type=int, default=0, 
                        help='Camera index (default: 0)')
    parser.add_argument('--record', action='store_true', 
                        help='Record video output')
    parser.add_argument('--log', action='store_true', 
                        help='Log detections')
    return parser.parse_args()


def main():
    """Main application entry point"""
    # Parse arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_config(args.config)
    
    # Initialize components
    yolo_detector = YOLODetector(
        model_path=config['yolo']['model_path'],
        conf_threshold=config['yolo']['confidence'],
        classes_to_detect=config['yolo']['classes']
    )
    
    motion_detector = MotionDetector(
        threshold=config['motion']['threshold'],
        min_area=config['motion']['min_area'],
        blur_size=config['motion']['blur_size']
    )
    
    alert_system = AlertSystem(
        use_sound=config['alerts']['use_sound'],
        sound_cooldown=config['alerts']['sound_cooldown']
    )
    
    logger = None
    if args.log:
        log_dir = Path(config['logging']['log_dir'])
        log_dir.mkdir(exist_ok=True)
        logger = Logger(log_dir / f"detections_{time.strftime('%Y%m%d_%H%M%S')}.csv")
    
    # Open camera
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print(f"Error: Could not open camera {args.camera}")
        return
    
    # Configure video writer if recording
    video_writer = None
    if args.record:
        output_dir = Path(config['recording']['output_dir'])
        output_dir.mkdir(exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        video_writer = cv2.VideoWriter(
            str(output_dir / f"detection_{time.strftime('%Y%m%d_%H%M%S')}.avi"),
            fourcc, fps, (width, height)
        )
    
    # Process first frame for motion detection
    ret, prev_frame = cap.read()
    if not ret:
        print("Error: Could not read from camera")
        return
    
    motion_detector.set_prev_frame(prev_frame)
    
    print("Starting detection. Press 'q' to quit.")
    
    try:
        while True:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read from camera")
                break
            
            # Clone frame for detections
            display_frame = frame.copy()
            
            # Run object detection
            yolo_results = yolo_detector.detect(frame)
            
            # Run motion detection
            motion_results = motion_detector.detect(frame)
            
            # Combine detections for display
            if yolo_results:
                # Process YOLO detections
                for obj in yolo_results:
                    # Draw bounding box
                    cv2.rectangle(
                        display_frame, 
                        (obj['x1'], obj['y1']), 
                        (obj['x2'], obj['y2']), 
                        (0, 255, 0), 2
                    )
                    
                    # Draw label with confidence
                    label = f"{obj['label']} {obj['confidence']:.2f}"
                    cv2.putText(
                        display_frame, label, 
                        (obj['x1'], obj['y1'] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                    )
                    
                    # Trigger alert for detected objects
                    alert_system.trigger(f"{obj['label']} detected")
                    
                    # Log detection
                    if logger:
                        logger.log_detection(obj['label'], obj['confidence'])
            
            # Draw motion detection areas
            if motion_results:
                for area in motion_results:
                    x, y, w, h = area
                    cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(
                        display_frame, "Motion", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
                    )
                
                # Trigger motion alert
                alert_system.trigger("Sudden motion detected", priority=True)
                
                # Log motion
                if logger:
                    logger.log_motion()
            
            # Add timestamp
            cv2.putText(
                display_frame,
                time.strftime("%Y-%m-%d %H:%M:%S"),
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
            )
            
            # Show output
            cv2.imshow("AI Co-pilot Detection", display_frame)
            
            # Write frame if recording
            if video_writer:
                video_writer.write(display_frame)
            
            # Check for exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    except KeyboardInterrupt:
        print("Detection stopped by user")
    
    finally:
        # Cleanup
        cap.release()
        if video_writer:
            video_writer.release()
        cv2.destroyAllWindows()
        if logger:
            logger.close()
        print("Application closed")


if __name__ == "__main__":
    main()
