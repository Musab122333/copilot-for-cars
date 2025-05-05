mport React from 'react';
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Play, Square, Bell, BellOff } from "lucide-react";

interface ControlsProps {
  isRunning: boolean;
  soundAlerts: boolean;
  onStart: () => void;
  onStop: () => void;
  onToggleSound: () => void;
}

const Controls: React.FC<ControlsProps> = ({
  isRunning,
  soundAlerts,
  onStart,
  onStop,
  onToggleSound
}) => {
  return (
    <Card className="bg-black/40 border-gray-800">
      <div className="p-4">
        <h2 className="text-lg font-semibold mb-3 text-white">Controls</h2>
        <div className="flex flex-col sm:flex-row gap-4 items-center">
          <div className="flex gap-3">
            <Button
              onClick={onStart}
              disabled={isRunning}
              className="bg-sentinel-green hover:bg-sentinel-green/80 text-white"
              size="lg"
            >
              <Play className="mr-1 h-4 w-4" /> Start
            </Button>
            <Button
              onClick={onStop}
              disabled={!isRunning}
              variant="destructive"
              size="lg"
            >
              <Square className="mr-1 h-4 w-4" /> Stop
            </Button>
          </div>
          
          <div className="flex items-center space-x-2 ml-auto">
            <Switch 
              id="sound-alerts" 
              checked={soundAlerts}
              onCheckedChange={onToggleSound}
            />
            <Label htmlFor="sound-alerts" className="flex items-center cursor-pointer">
              {soundAlerts ? (
                <>
                  <Bell className="h-4 w-4 mr-1 text-sentinel-purple" /> Sound Alerts
                </>
              ) : (
                <>
                  <BellOff className="h-4 w-4 mr-1 text-gray-500" /> Sound Alerts
                </>
              )}
            </Label>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default Controls;