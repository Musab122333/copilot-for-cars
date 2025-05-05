"""
Configuration Module
Handles loading and validation of configuration
"""

import yaml
import os
from pathlib import Path


def load_config(config_path):
    """
    Load configuration from YAML file
    
    Args:
        config_path: Path to configuration file
    
    Returns:
        Dict with configuration
    """
    # Check if config file exists
    if not os.path.exists(config_path):
        print(f"Warning: Config file {config_path} not found, using default configuration")
        return get_default_config()
    
    # Load config
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Validate and merge with defaults
        return validate_config(config)
    
    except Exception as e:
        print(f"Error loading config file: {e}")
        print("Using default configuration")
        return get_default_config()


def get_default_config():
    """
    Get default configuration
    
    Returns:
        Dict with default configuration
    """
    return {
        'yolo': {
            'model_path': 'yolov8n.pt',
            'confidence': 0.5,
            'classes': ['person', 'car', 'motorbike', 'bicycle', 'truck', 'dog', 'cat']
        },
        'motion': {
            'threshold': 25,
            'min_area': 5000,
            'blur_size': 21
        },
        'alerts': {
            'use_sound': True,
            'sound_cooldown': 3.0
        },
        'logging': {
            'log_dir': 'logs'
        },
        'recording': {
            'output_dir': 'recordings'
        }
    }


def validate_config(config):
    """
    Validate configuration and fill missing values with defaults
    
    Args:
        config: Configuration dict to validate
    
    Returns:
        Validated configuration dict
    """
    default_config = get_default_config()
    
    # Ensure all required sections exist
    for section in default_config:
        if section not in config:
            config[section] = default_config[section]
        else:
            # Ensure all required keys exist in each section
            for key in default_config[section]:
                if key not in config[section]:
                    config[section][key] = default_config[section][key]
    
    return config


def save_config(config, config_path):
    """
    Save configuration to YAML file
    
    Args:
        config: Configuration dict
        config_path: Path to save configuration file
    """
    try:
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        print(f"Configuration saved to {config_path}")
    except Exception as e:
        print(f"Error saving configuration: {e}")
