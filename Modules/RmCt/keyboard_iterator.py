from pynput import keyboard

# Expand this dictionary with more keys as needed:
SPECIAL_KEYS = {
    keyboard.Key.enter: "Enter",
    keyboard.Key.space: " ",
    keyboard.Key.shift: "Shift",
    keyboard.Key.shift_l: "Shift",
    keyboard.Key.shift_r: "Shift",
    keyboard.Key.ctrl: "Ctrl",
    keyboard.Key.ctrl_l: "Ctrl",
    keyboard.Key.ctrl_r: "Ctrl",
    keyboard.Key.alt: "Alt",
    keyboard.Key.alt_l: "Alt",
    keyboard.Key.alt_r: "Alt",
    keyboard.Key.backspace: "Backspace",
    keyboard.Key.tab: "Tab",
    keyboard.Key.esc: "Esc",
    keyboard.Key.up: "Up",
    keyboard.Key.down: "Down",
    keyboard.Key.left: "Left",
    keyboard.Key.right: "Right",
    keyboard.Key.delete: "Delete",
    keyboard.Key.caps_lock: "CapsLock",
}

pressed_keys = set()

def get_key_string(key):
    # For character keys (alphanumeric), return the character
    if hasattr(key, 'char') and key.char is not None:
        return key.char
    # For special keys, return mapped name or fallback
    return SPECIAL_KEYS.get(key, str(key))

def on_press(key):
    pressed_keys.add(key)

def on_release(key):
    pressed_keys.discard(key)

def get_pressed_keys():
    return [get_key_string(k) for k in pressed_keys]

# Start global listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

class Keyboard_Iterator:
    def __init__(self):
        self.Pressed = []
        self.Held = []

        # Special key Booleans
        self.Enter = False
        self.Space = False
        self.Shift = False
        self.Ctrl = False
        self.Alt = False
        self.Backspace = False
        self.Tab = False
        self.Esc = False

    def Update(self):
        NewKeys = get_pressed_keys()
        NewPressed = []
        for key in NewKeys:
            if key not in self.Held:
                NewPressed.append(key)
        self.Held = NewKeys
        self.Pressed = NewPressed

        # Update all special key attributes
        self.Enter = "Enter" in self.Held
        self.Space = " " in self.Held
        self.Shift = "Shift" in self.Held
        self.Ctrl = "Ctrl" in self.Held
        self.Alt = "Alt" in self.Held
        self.Backspace = "Backspace" in self.Held
        self.Tab = "Tab" in self.Held
        self.Esc = "Esc" in self.Held




Old = "Wow,This"
New = Old[:-1]
print(New)



if __name__ == "__main__":
    import time

    The_Keyboard_Iterator = Keyboard_Iterator()

    while True:
        The_Keyboard_Iterator.Update()
        print("Pressed this frame:", The_Keyboard_Iterator.Pressed)
        print(
            f"Enter: {The_Keyboard_Iterator.Enter}, "
            f"Space: {The_Keyboard_Iterator.Space}, "
            f"Shift: {The_Keyboard_Iterator.Shift}, "
            f"Ctrl: {The_Keyboard_Iterator.Ctrl}, "
            f"Alt: {The_Keyboard_Iterator.Alt}, "
            f"Backspace: {The_Keyboard_Iterator.Backspace}, "
            f"Tab: {The_Keyboard_Iterator.Tab}, "
            f"Esc: {The_Keyboard_Iterator.Esc}"
        )
        time.sleep(0.2)
