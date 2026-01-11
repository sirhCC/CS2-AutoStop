# CS2 Auto-Strafe Script

This script automatically counter-strafes in CS2 by tapping the opposite movement key when you release a directional key.

## What is Counter-Strafing?

In Counter-Strike, your character has momentum when moving. Counter-strafing is the technique of quickly tapping the opposite direction key to instantly stop your movement, allowing you to shoot accurately faster. This script automates that process.

## How It Works

- **Release A (left)** → Automatically taps D (right) to stop
- **Release D (right)** → Automatically taps A (left) to stop  
- **Release W (forward)** → Automatically taps S (backward) to stop
- **Release S (backward)** → Automatically taps W (forward) to stop

## Installation

1. Install Python 3.7 or higher
2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the script with administrator privileges (required for keyboard hooks):
   ```
   python auto_strafe.py
   ```
2. Switch to CS2 and play normally
3. Press **END** key to stop the script

## Configuration

You can adjust these settings in the script:

- `tap_duration`: How long the opposite key is pressed (default: 0.01 seconds)
- `cooldown`: Minimum time between counter-strafes (default: 0.1 seconds)

## Important Notes

⚠️ **Warning**: Using automation scripts in online games may violate terms of service and result in bans. Use at your own risk, preferably in offline/practice modes only.

## Requirements

- Windows OS
- Python 3.7+
- Administrator privileges (for keyboard hooks)
