# This program takes a midi, quickly describes it and converts it to CSV

# Refactor ideas
# Split parse and export function
# Message Dict one level higher
#

# Imports

import os
import sys
import mido
import pandas as pd


def main(args):
    for filename in args:
        print(f"===Converting {filename}===")
        convert_to_csv(filename)
        note_frame = pd.DataFrame()


def convert_to_csv(filename):

    mid = mido.MidiFile(filename)
    filename = filename[:-4]
    os.makedirs('output/' + filename, exist_ok=True)

    meta_data_list = []
    note_list = []

    for track_index, track in enumerate(mid.tracks):
        absolute_time = 0
        for message_index, message in enumerate(track):
            absolute_time += message.time
            if message.is_meta:
                meta_message = message.dict()
                if len(meta_message) == 2:
                    meta_data_list.append([
                        track_index, absolute_time, str(
                            message.type), '-'
                    ])
                elif len(meta_message) == 3:
                    meta_message.pop('type')
                    meta_message.pop('time')
                    for key, value in meta_message.items():
                        meta_data_list.append([
                            track_index, absolute_time, str(
                                message.type), str(value)
                        ])
                else:
                    meta_message.pop('type')
                    meta_message.pop('time')
                    for key, value in meta_message.items():
                        meta_data_list.append([
                            track_index, absolute_time, f"{message.type}_{key}", str(
                                value)
                        ])
            elif message.type == 'control_change':
                if 'control=64' in str(message):
                    meta_message = message.dict()
                    meta_data_list.append([
                        track_index, absolute_time, 'pedal', meta_message['value']
                    ])
            elif message.type == 'note_on' or message.type == 'note_off':
                meta_message = message.dict()
                note_list.append([
                    track_index, absolute_time, message.type, meta_message[
                        'note'], meta_message['velocity']
                ])
            note_frame = pd.DataFrame(
                note_list, columns=['track', 'time', 'type', 'note', 'velocity'])
            meta_frame = pd.DataFrame(meta_data_list, columns=[
                'track', 'time', 'key', 'value'])
            note_frame.to_csv(
                f"output/{filename}/{filename}_note.csv", index=False, encoding='utf-8-sig')
            meta_frame.to_csv(
                f"output/{filename}/{filename}_meta.csv", index=False, encoding='utf-8-sig')
    print('Done')


if __name__ == "__main__":
    main(sys.argv[1:])
