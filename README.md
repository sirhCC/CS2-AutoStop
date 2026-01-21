# CS2 Auto Strafe Script

This script automatically counter-strafes in CS2 using two different modes: **Key Release Mode** (stops when you release movement keys) and **Mouse1 Mode** (stops when you click to shoot).

## What is Counter-Strafing?

In Counter-Strike, your character has momentum when moving. Counter-strafing is the technique of quickly tapping the opposite direction key to instantly stop your movement, allowing you to shoot accurately faster. This script automates that process.

## Features

- **Two Operation Modes:**
  - **RELEASE Mode**: Counter-strafes when you release a movement key (A/W/S/D)
  - **MOUSE1 Mode**: Counter-strafes when you click to shoot
  
- **Human Mode**: Anti-detection feature with randomized timing (3-10ms reaction delay, 30-75ms tap duration)

- **Smart Detection:**
  - Only counter-strafes if keys are held for 0.35+ seconds (prevents accidental triggers during taps)
  - Skips counter-strafing if you're already moving in opposite direction
  - Doesn't counter-strafe while jumping

- **Runtime Controls:**
  - Toggle between modes without restarting
  - Pause/resume functionality
  - Enable/disable on the fly

## How It Works

### Release Mode
- **Release A (left)** → Automatically taps D (right) to stop
- **Release D (right)** → Automatically taps A (left) to stop  
- **Release W (forward)** → Automatically taps S (backward) to stop
- **Release S (backward)** → Automatically taps W (forward) to stop

### Mouse1 Mode
- **Click Left Mouse Button** → Automatically counter-strafes any active movement direction

## Installation

1. Install Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script with administrator privileges (required for keyboard hooks):
   ```bash
   python auto_strafe.py
   ```

2. The script starts in **RELEASE mode** with **Human Mode enabled**

3. Use the hotkeys to control the script (see below)

4. Play CS2 normally - the script runs in the background

5. Press **END** to stop the script

## Hotkeys

| Key | Function |
|-----|----------|
| **P** | Pause/Resume counter-strafing |
| **PAGE UP** | Enable counter-strafing |
| **PAGE DOWN** | Disable counter-strafing |
| **H** | Toggle Human Mode (anti-detection) ON/OFF |
| **M** | Switch between RELEASE ↔ MOUSE1 modes |
| **END** | Exit the script |

## Configuration

Adjustable parameters in the script:

### Release Mode Settings
- **Minimum hold duration**: 0.35 seconds (prevents accidental counter-strafes on quick taps)
- **Reaction delay**: 3-10ms randomized (human mode) or 6ms fixed
- **Counter-strafe duration**: 30-75ms randomized (human mode) or 50ms fixed

### Mouse1 Mode Settings
- **Reaction delay**: 8-18ms randomized (human mode) or 12ms fixed
- **Counter-strafe duration**: 25-80ms randomized

### Human Mode
- When **ON**: Adds randomization to timing for more natural behavior
- When **OFF**: Uses fixed timing values

## Important Notes

⚠️ **Warning**: Using automation scripts in online games may violate terms of service and result in bans. **Use at your own risk**

## Requirements

- Windows OS
- Python 3.7+
- Administrator privileges (for keyboard hooks)
- Dependencies: `keyboard==0.13.5`, `mouse==0.7.1`

## Technical Details

- Uses threading to prevent blocking user input
- Debounce protection (300ms) on toggle commands
- Real-time key press/release detection and logging
- Cross-key detection to prevent conflicts during direction changes
