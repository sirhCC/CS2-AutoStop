"""
CS2 Auto Strafe - Counter-strafe to stop faster and be more accurate
"""

import keyboard
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
    
    def enable(self):
        """Enable auto strafe"""
        self.enabled = True
        print(f"\n>>> ENABLED <<<")
    
    def disable(self):
        """Disable auto strafe"""
        self.enabled = False
        print(f"\n>>> DISABLED <<<")
    
    def toggle(self):
        """Toggle auto strafe on/off"""
        if self.enabled:
            self.disable()
        else:
            self.enable()
    
    def toggle_human_mode(self):
        """Toggle human-like randomization"""
        self.human_mode = not self.human_mode
        status = "ON" if self.human_mode else "OFF"
        print(f"\n>>> HUMAN MODE: {status} <<<")
    
    def start(self):
        """Start the script"""
        print("=" * 50)
        print("CS2 AUTO STRAFE")
        print("=" * 50)
        print("Release a movement key → Auto tap opposite to stop")
        print("\nControls:")
        print("- P: Pause/Resume")
        print("- PAGE UP: Enable | PAGE DOWN: Disable")
        print("- H: Toggle Human Mode (anti-detection)")
        print("- END: Exit")
        print("=" * 50)
        print("Status: ENABLED | Human Mode: ON")
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
        
        # Pause/Resume key
        keyboard.on_press_key('p', lambda _: self.toggle())
        
        # Human mode toggle
        keyboard.on_press_key('h', lambda _: self.toggle_human_mode())
        
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
