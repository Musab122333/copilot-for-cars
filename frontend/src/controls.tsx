import Controls from "./Controls";
import { useState } from "react";
import { startDetection, stopDetection, toggleSound } from "./api";

function App() {
  const [isRunning, setIsRunning] = useState(false);
  const [soundAlerts, setSoundAlerts] = useState(false);

  const handleStart = async () => {
    await startDetection();
    setIsRunning(true);
  };

  const handleStop = async () => {
    await stopDetection();
    setIsRunning(false);
  };

  const handleToggleSound = async () => {
    await toggleSound();
    setSoundAlerts(!soundAlerts);
  };

  return (
    <div>
      <Controls
        isRunning={isRunning}
        soundAlerts={soundAlerts}
        onStart={handleStart}
        onStop={handleStop}
        onToggleSound={handleToggleSound}
      />
    </div>
  );
}

export default App;
