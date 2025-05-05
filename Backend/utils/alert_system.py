"""
Alert System Module
Handles alert notifications for detected objects and motion
"""

import time
import threading
import pyttsx3


class AlertSystem:
    """Alert system for notifications"""
    
    def __init__(self, use_sound=True, sound_cooldown=3.0):
        """
        Initialize alert system
        
        Args:
            use_sound: Whether to use voice alerts
            sound_cooldown: Cooldown period between alerts (seconds)
        """
        self.use_sound = use_sound
        self.sound_cooldown = sound_cooldown
        self.last_alert_time = 0
        self.alert_lock = threading.Lock()
        
        # Initialize text-to-speech engine if sound is enabled
        self.engine = None
        if self.use_sound:
            try:
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 150)  # Speed of speech
                self.engine.setProperty('volume', 0.9)  # Volume
                print("Voice alert system initialized")
            except Exception as e:
                print(f"Warning: Could not initialize speech engine: {e}")
                self.use_sound = False
    
    def trigger(self, message, priority=False):
        """
        Trigger an alert
        
        Args:
            message: Alert message
            priority: If True, bypass cooldown period
        """
        current_time = time.time()
        
        # Always print to console
        print(f"ALERT: {message}")
        
        # Check cooldown for sound alerts
        if self.use_sound and self.engine:
            with self.alert_lock:
                if priority or (current_time - self.last_alert_time >= self.sound_cooldown):
                    self.last_alert_time = current_time
                    # Run in a separate thread to prevent blocking
                    threading.Thread(target=self._speak_alert, args=(message,), daemon=True).start()
    
    def _speak_alert(self, message):
        """
        Speak an alert message using text-to-speech
        
        Args:
            message: Message to speak
        """
        try:
            self.engine.say(message)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Warning: Could not play voice alert: {e}")
