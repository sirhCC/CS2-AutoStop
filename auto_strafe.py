"""
CS2 Auto Strafe - Counter-strafe to stop faster and be more accurate
"""

import keyboard
import mouse
import time
import threading
import random

class AutoStrafe:
    def __init__(self):
        self.enabled = True
        self.running = False
        self.last_key_time = {}  # Track when each key was pressed
        self.human_mode = True  # Anti-detection mode (randomized timing)
        self.counter_strafe_count = 0
        self.mode = 'release'  # 'release' or 'mouse1'
        self.last_toggle_time = 0  # Prevent rapid toggles
    
    def on_key_release(self, key):
        """Handle key release and counter-strafe"""
        if not self.enabled or self.mode != 'release':
            print(f"Release {key.upper()}: Skipped (enabled={self.enabled}, mode={self.mode})")
            return
        
        # Check how long the key was held
        if key not in self.last_key_time:
            print(f"Release {key.upper()}: No press time recorded")
            return
        
        release_time = time.time()
        hold_duration = release_time - self.last_key_time[key]
        print(f"Release {key.upper()}: Press={self.last_key_time[key]:.3f}, Release={release_time:.3f}, Held for {hold_duration:.3f}s")
        
        # Reset the time so next press is fresh
        self.last_key_time[key] = 0
        
        # Only counter-strafe if key was held for more than 0.35 seconds
        if hold_duration < 0.35:
            print(f"  -> Too short (need 0.35s+)")
            return
        
        # Get opposite key
        opposite = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}[key]
        
        # ONLY check if opposite key is already pressed - if so, user is switching direction
        if keyboard.is_pressed(opposite):
            print(f"  -> Opposite key {opposite.upper()} pressed, skipping")
            return
        
        print(f"  -> Counter-strafing with {opposite.upper()}")
        
        def do_counter_strafe():
            # Small delay to catch direction changes
            if self.human_mode:
                reaction_delay = random.uniform(0.003, 0.010)
            else:
                reaction_delay = 0.006
            time.sleep(reaction_delay)
            
            # After delay, check if user started moving in any direction
            if keyboard.is_pressed('a') or keyboard.is_pressed('d') or keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('space'):
                return
            
            # Randomized counter-strafe duration
            if self.human_mode:
                duration = random.uniform(0.030, 0.075)
            else:
                duration = 0.050
            
            keyboard.press(opposite)
            time.sleep(duration)
            keyboard.release(opposite)
            
            print(f"Stop: {opposite.upper()} (held {hold_duration:.2f}s)")
            self.counter_strafe_count += 1
        
        # Run in thread so it doesn't block user input
        threading.Thread(target=do_counter_strafe, daemon=True).start()
    
    def on_key_press(self, key):
        """Track when keys are pressed for hold duration detection"""
        # Only record the first press, not repeated presses
        if key not in self.last_key_time or self.last_key_time[key] == 0:
            self.last_key_time[key] = time.time()
            print(f"Press: {key.upper()} at {self.last_key_time[key]:.3f}")
    
    def on_mouse1_press(self):
        """Auto counter-strafe when shooting"""
        if not self.enabled or self.mode != 'mouse1':
            return
        
        # Don't counter-strafe if jumping
        if keyboard.is_pressed('space'):
            return
        
        # Find which movement keys are currently pressed
        moving_keys = []
        if keyboard.is_pressed('a'):
            moving_keys.append('a')
        if keyboard.is_pressed('d'):
            moving_keys.append('d')
        if keyboard.is_pressed('w'):
            moving_keys.append('w')
        if keyboard.is_pressed('s'):
            moving_keys.append('s')
        
        if not moving_keys:
            return  # Not moving
        
        # Counter-strafe the movement
        def do_shoot_stop():
            # Small delay for realism
            if self.human_mode:
                time.sleep(random.uniform(0.008, 0.018))
            else:
                time.sleep(0.012)
            
            # Re-check if still moving (user might have already released)
            still_moving = []
            if keyboard.is_pressed('a'):
                still_moving.append('a')
            if keyboard.is_pressed('d'):
                still_moving.append('d')
            if keyboard.is_pressed('w'):
                still_moving.append('w')
            if keyboard.is_pressed('s'):
                still_moving.append('s')
            
            if not still_moving:
                return
            
            # Counter-strafe all active movement directions
            opposites = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}
            duration = random.uniform(0.025, 0.080)
            
            for key in still_moving:
                opposite = opposites[key]
                keyboard.press(opposite)
            
            time.sleep(duration)
            
            for key in still_moving:
                opposite = opposites[key]
                keyboard.release(opposite)
            
            print(f"Stop [shoot]: {', '.join([opposites[k].upper() for k in still_moving])}")
            self.counter_strafe_count += 1
        
        threading.Thread(target=do_shoot_stop, daemon=True).start()
    
    def enable(self):
        """Enable auto strafe"""
        current_time = time.time()
        if current_time - self.last_toggle_time < 0.3:  # 300ms debounce
            return
        self.last_toggle_time = current_time
        self.enabled = True
        print(f"\n>>> ENABLED <<<")
    
    def disable(self):
        """Disable auto strafe"""
        current_time = time.time()
        if current_time - self.last_toggle_time < 0.3:  # 300ms debounce
            return
        self.last_toggle_time = current_time
        self.enabled = False
        print(f"\n>>> DISABLED <<<")
    
    def toggle(self):
        """Toggle auto strafe on/off"""
        current_time = time.time()
        if current_time - self.last_toggle_time < 0.3:  # 300ms debounce
            return
        self.last_toggle_time = current_time
        if self.enabled:
            self.disable()
        else:
            self.enable()
    
    def toggle_human_mode(self):
        """Toggle human-like randomization"""
        self.human_mode = not self.human_mode
        status = "ON" if self.human_mode else "OFF"
        print(f"\n>>> HUMAN MODE: {status} <<<")
    
    def toggle_mode(self):
        """Toggle between release mode and mouse1 mode"""
        if self.mode == 'release':
            self.mode = 'mouse1'
            print(f"\n>>> MODE: MOUSE1 (shoot to stop) <<<")
        else:
            self.mode = 'release'
            print(f"\n>>> MODE: KEY RELEASE (release to stop) <<<")
    
    def start(self):
        """Start the script"""
        print("=" * 50)
        print("CS2 AUTO STRAFE")
        print("=" * 50)
        print("Two modes:")
        print("  RELEASE: Auto stop when releasing movement keys")
        print("  MOUSE1: Auto stop when clicking to shoot")
        print("\nControls:")
        print("- P: Pause/Resume")
        print("- PAGE UP: Enable | PAGE DOWN: Disable")
        print("- H: Toggle Human Mode (anti-detection)")
        print("- M: Switch Mode (Release ↔ Mouse1)")
        print("- END: Exit")
        print("=" * 50)
        print("Status: ENABLED | Human: ON | Mode: RELEASE")
        print("=" * 50)
        
        self.running = True
        
        # Hook movement key presses (for peek detection)
        keyboard.on_press_key('a', lambda _: self.on_key_press('a'))
        keyboard.on_press_key('d', lambda _: self.on_key_press('d'))
        keyboard.on_press_key('w', lambda _: self.on_key_press('w'))
        keyboard.on_press_key('s', lambda _: self.on_key_press('s'))
        
        # Hook movement key releases
        keyboard.on_release_key('a', lambda _: self.on_key_release('a'))
        keyboard.on_release_key('d', lambda _: self.on_key_release('d'))
        keyboard.on_release_key('w', lambda _: self.on_key_release('w'))
        keyboard.on_release_key('s', lambda _: self.on_key_release('s'))
        
        # Hook mouse1 (left click)
        try:
            mouse.on_button(self.on_mouse1_press, buttons=['left'], types=['down'])
            print("Mouse1 hook: ACTIVE")
        except Exception as e:
            print(f"Mouse1 hook: FAILED ({e})")
            self.mode = 'release'  # Fallback to release mode
        
        # Pause/Resume key
        keyboard.on_press_key('p', lambda _: self.toggle())
        
        # Human mode toggle
        keyboard.on_press_key('h', lambda _: self.toggle_human_mode())
        
        # Mode toggle
        keyboard.on_press_key('m', lambda _: self.toggle_mode())
        
        # Enable/Disable keys
        keyboard.on_press_key('page up', lambda _: self.enable())
        keyboard.on_press_key('page down', lambda _: self.disable())
        
        # Wait for END
        keyboard.wait('end')
        self.stop()
    
    def stop(self):
        """Stop the script"""
        self.running = False
        keyboard.unhook_all()
        print("\n" + "=" * 50)
        print("Stopped")
        print("=" * 50)


if __name__ == "__main__":
    auto_strafe = AutoStrafe()
    try:
        auto_strafe.start()
    except KeyboardInterrupt:
        auto_strafe.stop()
