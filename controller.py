from audio import *
from smart_lights import Light
import time
colormap = {
    # 'W' : (255, 0),
    # 'V' : (128, 0, 128),
    'B' : (0, 0, 255),
    'C' : (72, 255, 220),
    'G' : (34, 139, 34),
    'Y' : (255,215,0),
    'P' : (255,12,34),
    'R' : (255, 0, 0)
}

def main():
    max_val = 100
    colors = list(colormap.keys())
    partition_size = max_val//(len(colors) - 1)
    audio, stream = init_audio()
    reading_light = Light('10.0.0.12')  # change address
    room_light = Light('10.0.0.24')
    room_light._turn_off()
    reading_light._turn_off()
    counter = 0
    while True: # audio loop
        if(counter==1000):
            counter = 0
        time.sleep(0.3)
        if keyboard.is_pressed('q'):
            reading_light._turn_off()
            room_light._turn_off()
            break
        amplitude = audio_to_amp(stream, max_val)
        color_index = int(amplitude)//partition_size
        reading_light._change_color(colormap[colors[color_index]])
        # counter+=1
        # if(counter%2==1):
        room_light._change_color(colormap[colors[len(colors) - 1 - color_index]])
            # counter = 0
        bars="#"*int(amplitude)
        print(int(amplitude), bars)
    # stop Recording
    close_audio(stream, audio)

if __name__ == '__main__':
    main()