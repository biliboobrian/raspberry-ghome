import snowboydecoder
import home_light
import signal

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

def bob_allume_salon():
    home_light.turn_on_screen_light()

def bob_allume_cuisine():
    home_light.turn_on_cuisine_light()

def bob_eteins_salon():
    home_light.turn_off_salon_light()

def bob_eteins_cuisine():
    home_light.turn_off_cuisine_light()

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector_allume_salon = snowboydecoder.HotwordDetector('./resources/bob_allume_salon.pmdl', sensitivity=0.5)
detector_allume_cuisine = snowboydecoder.HotwordDetector('./resources/bob_allume_cuisine.pmdl', sensitivity=0.5)
detector_eteins_salon = snowboydecoder.HotwordDetector('./resources/bob_eteins_salon.pmdl', sensitivity=0.5)
detector_eteins_cuisine = snowboydecoder.HotwordDetector('./resources/bob_eteins_cuisine.pmdl', sensitivity=0.5)

print('Listening... Press Ctrl+C to exit')

# main loop
detector_allume_salon.start(detected_callback=bob_allume_salon, interrupt_check=interrupt_callback, sleep_time=0.03)
detector_allume_cuisine.start(detected_callback=bob_allume_cuisine, interrupt_check=interrupt_callback, sleep_time=0.03)
detector_eteins_salon.start(detected_callback=bob_eteins_salon, interrupt_check=interrupt_callback, sleep_time=0.03)
detector_eteins_cuisine.start(detected_callback=bob_eteins_cuisine, interrupt_check=interrupt_callback, sleep_time=0.03)

detector_allume_salon.terminate()
detector_allume_cuisine.terminate()
detector_eteins_salon.terminate()
detector_eteins_cuisine.terminate()