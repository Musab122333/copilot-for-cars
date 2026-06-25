# AI Co-pilot for Cars

A proof-of-concept road safety system that uses computer vision and motion detection to monitor video input, alert on abnormal events, and optionally log or record activity.

## Repository Structure

- `Backend/`
  - `main_script.py` - main Python application entrypoint for camera capture, YOLO object detection, motion detection, alerts, recording, and logging.
  - `config.yaml` - YAML configuration file for model paths, detection thresholds, and output behavior.
  - `yolov8n.pt` - YOLOv8 model weights used by the detector.
  - `detectors/`
    - `yolo_detector.py` - runs YOLOv8 inference and sends ESP32 alerts for selected objects.
    - `motion_detector.py` - detects motion across video frames using frame differencing and contour analysis.
  - `utils/`
    - `alert_system.py` - voice and console alerts using `pyttsx3`.
    - `logger.py` - CSV logging for detection and motion events.
    - `config.py` - YAML configuration loader and validator.

- `frontend/`
  - React/Vite UI files that call backend endpoints for start/stop/toggle sound and fetch detection data.
  - `vite.config.ts` proxies API calls to `http://localhost:8000`.
  - Note: `frontend/package.json` is currently empty and needs dependency configuration before the frontend can be installed and launched.

- `requirements (1).txt` - Python dependency list for the backend.
- `app1.tsx` - additional React component file found in the repo root.

## Features

- YOLOv8 object detection using `ultralytics`
- Real-time motion detection with OpenCV
- Voice alerts and console notifications
- Optional logging to CSV
- Optional video recording of the detection output
- Configurable thresholds and classes via YAML
- ESP32 alert integration over Wi-Fi TCP for selected object classes

## Prerequisites

- Python 3.10+ installed
- Node.js and npm installed for frontend development (if using the React UI)
- `Backend/yolov8n.pt` available in the repository
- A camera device connected and accessible by OpenCV

## Backend Setup

1. Create and activate a virtual environment:

```powershell
cd "c:\Users\musab\Downloads\Road safety"
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r "requirements (1).txt"
```

3. Run the backend detection application:

```powershell
python Backend\main_script.py --config Backend\config.yaml --camera 0 --record --log
```

4. Press `q` in the video window to stop.

## Configuration

The backend loads configuration from `Backend/config.yaml`.

Key options:

- `yolo.model_path` - path to the YOLO model file
- `yolo.confidence` - detection confidence threshold
- `yolo.classes` - optional class list to restrict detection
- `motion.threshold` - pixel difference threshold for motion
- `motion.min_area` - minimum contour area for motion alerts
- `alerts.use_sound` - enable voice alerts
- `alerts.sound_cooldown` - cooldown between spoken alerts
- `logging.log_dir` - directory for CSV logs
- `recording.output_dir` - directory for recorded video output

## Frontend Notes

The `frontend` directory contains React components and a Vite configuration for a control UI. It is wired to proxy API requests to `http://localhost:8000` for endpoints:

- `POST /start-detection`
- `POST /stop-detection`
- `POST /toggle-sound`
- `GET /detections`

Current status:

- `frontend/package.json` is empty, so the frontend app cannot be installed or started until dependencies are added.
- The backend server implementation for these API endpoints is not present in the repository. The React UI currently serves as a design reference rather than a working control panel.

## Notes

- The YOLO detector sends an alert to an ESP32 at `192.168.150.87:3333` when selected object classes are detected.
- The alert system uses `pyttsx3` for spoken alerts, which may require additional system audio configuration.
- The project appears to be a design-thinking prototype with core detection logic in `Backend/` and frontend UI scaffolding in `frontend/`.

## Suggested Improvements

- Add a backend HTTP server to expose the frontend API endpoints.
- Populate `frontend/package.json` with Vite/React dependencies.
- Add a more complete frontend camera feed component.
- Rename `requirements (1).txt` to `requirements.txt` for standard usage.

