import React, { useState, useEffect } from "react";
import Controls from "./Controls";
import CameraFeed from "./CameraFeed";
import { startDetection, stopDetection, toggleSound, getDetections } from "./api";

interface BoundingBox {
  id: number;
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
  color: string;
}

const App: React.FC = () => {
  const [isRunning, setIsRunning] = useState(false);
  const [soundAlerts, setSoundAlerts] = useState(false);
  const [detections, setDetections] = useState<BoundingBox[]>([]);

  // Poll detection data every second when running
  useEffect(() => {
    let interval: NodeJS.Timeout;

    if (isRunning) {
      interval = setInterval(async () => {
        try {
          const detectionData = await getDetections();
          setDetections(detectionData);
        } catch (error) {
          console.error("Error fetching detections:", error);
        }
      }, 1000);
    } else {
      setDetections([]);
    }

    return () => clearInterval(interval);
  }, [isRunning]);

  const handleStart = async () => {
    try {
      await startDetection();
      setIsRunning(true);
    } catch (error) {
      console.error("Failed to start detection:", error);
    }
  };

  const handleStop = async () => {
    try {
      await stopDetection();
      setIsRunning(false);
    } catch (error) {
      console.error("Failed to stop detection:", error);
    }
  };

  const handleToggleSound = async () => {
    try {
      await toggleSound();
      setSoundAlerts((prev) => !prev);
    } catch (error) {
      console.error("Failed to toggle sound alerts:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-6 space-y-6">
      <Controls
        isRunning={isRunning}
        soundAlerts={soundAlerts}
        onStart={handleStart}
        onStop={handleStop}
        onToggleSound={handleToggleSound}
      />

      <CameraFeed
        isActive={isRunning}
        detections={detections}
      />
    </div>
  );
};

export default App;
