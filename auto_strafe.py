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
        self.human_mode = True  # Anti-detection mode
        self.success_rate = 0.95  # 95% accuracy (miss 5% of counter-strafes)
        self.counter_strafe_count = 0
        self.mouse1_stop = True  # Auto stop when shooting
        self.last_toggle_time = 0  # Prevent rapid toggles
    
    def on_key_release(self, key):
        """Handle key release and counter-strafe"""
        if not self.enabled:
            return
        
        # Don't counter-strafe if jumping (bunny hopping)
        if keyboard.is_pressed('space'):
            return
        
        # Get opposite key
        opposite = {'a': 'd', 'd': 'a', 'w': 's', 's': 'w'}[key]
        
        def do_counter_strafe():
            # Human-like: Occasionally miss counter-strafes (not perfect)
            if self.human_mode and random.random() > self.success_rate:
                print(f"Miss (human)")
                return
            
            # Human-like: Variable reaction time (10-25ms instead of fixed)
            reaction_delay = random.uniform(0.010, 0.025)
            time.sleep(reaction_delay)
            
            # If user is pressing any movement key or jumping, don't counter-strafe
            if keyboard.is_pressed('a') or keyboard.is_pressed('d') or keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('space'):
                return
            
            # Check if this is a quick peek (opposite key was pressed recently)
            current_time = time.time()
            if opposite in self.last_key_time:
                time_since_opposite = current_time - self.last_key_time[opposite]
                # If opposite was pressed within 200ms, likely peeking - don't counter-strafe
                if time_since_opposite < 0.2:
                    return
            
            # Human-like: More varied counter-strafe duration (20-90ms)
            duration = random.uniform(0.020, 0.090)
            
            # Human-like: Occasionally do imperfect double-tap (5% chance)
            double_tap = self.human_mode and random.random() < 0.05
            
            keyboard.press(opposite)
            time.sleep(duration)
            keyboard.release(opposite)
            
            # Human-like: Small random delay between taps
            if double_tap:
                time.sleep(random.uniform(0.010, 0.030))
                mini_tap = random.uniform(0.015, 0.040)
                keyboard.press(opposite)
                time.sleep(mini_tap)
                keyboard.release(opposite)
                print(f"Stop: {opposite.upper()} [double]")
            else:
                print(f"Stop: {opposite.upper()}")
            
            self.counter_strafe_count += 1
        
        # Run in thread so it doesn't block user input
        threading.Thread(target=do_counter_strafe, daemon=True).start()
    
    def on_key_press(self, key):
        """Track when keys are pressed for peek detection"""
        self.last_key_time[key] = time.time()
    
    def on_mouse1_press(self):
        """Auto counter-strafe when shooting"""
        if not self.enabled or not self.mouse1_stop:
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
            # Human-like: Occasionally miss (same as key release)
            if self.human_mode and random.random() > self.success_rate:
                return
            
            # Tiny delay for realism
            time.sleep(random.uniform(0.005, 0.015))
            
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
    
    def toggle_mouse1_stop(self):
        """Toggle mouse1 auto-stop"""
        self.mouse1_stop = not self.mouse1_stop
        status = "ON" if self.mouse1_stop else "OFF"
        print(f"\n>>> MOUSE1 STOP: {status} <<<")
    
    def start(self):
        """Start the script"""
        print("=" * 50)
        print("CS2 AUTO STRAFE")
        print("=" * 50)
        print("Release a movement key → Auto tap opposite to stop")
        print("Click Mouse1 while moving → Auto stop to shoot")
        print("\nControls:")
        print("- P: Pause/Resume")
        print("- PAGE UP: Enable | PAGE DOWN: Disable")
        print("- H: Toggle Human Mode (anti-detection)")
        print("- M: Toggle Mouse1 Auto-Stop")
        print("- END: Exit")
        print("=" * 50)
        print("Status: ENABLED | Human: ON | Mouse1: ON")
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
            self.mouse1_stop = False
        
        # Pause/Resume key
        keyboard.on_press_key('p', lambda _: self.toggle())
        
        # Human mode toggle
        keyboard.on_press_key('h', lambda _: self.toggle_human_mode())
        
        # Mouse1 stop toggle
        keyboard.on_press_key('m', lambda _: self.toggle_mouse1_stop())
        
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
