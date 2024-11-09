from flask import Flask, render_template
from flask_socketio import SocketIO
import pyautogui

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('move_event')
def handle_move_event(data):
    sensivity = 3
    delta_x = data.get('deltaX')
    delta_y = data.get('deltaY')
    pyautogui.moveRel(delta_x * sensivity, delta_y * sensivity)  # Move the mouse relatively to its current position


@socketio.on('log')
def handle_log(data):
    print(data)
    pass

@socketio.on('touch_event')
def handle_touch_event(data):
    action = data.get('action')
    if action == 'left_click':
        pyautogui.click()
    elif action == 'right_click':
        pyautogui.click(button='right')
    elif action == 'double_click':
        pyautogui.doubleClick()
    elif action == 'scroll':
        scroll_sens = 4
        delta_scroll = int(data.get('value'))
        pyautogui.scroll(-delta_scroll*scroll_sens)  # Negate for correct scroll direction


@socketio.on('keyboard_event')
def handle_keyboard_event(data):
    text = data.get('text')
    prev_text = data.get('prev_text')
    print(prev_text, text)

    if text == 'backspace':
        pyautogui.press('backspace')
    elif text == 'enter':
        pyautogui.press('enter')
    elif text == 'space':
        pyautogui.press('space')
    else:
        # Regular typing for other keys
        pyautogui.typewrite(text)

    print(f"Received keyboard event: {text}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug= True)


