# This program takes a midi, quickly describes it and converts it to CSV

# Imports

import os
import sys
import mido
import pandas as pd


def main(args):
    for filename in args:
        print(f"==={filename}===")
        convert_to_csv(filename)
        note_frame = pd.DataFrame()


def convert_to_csv(filename):

    mid = mido.MidiFile(filename)
    filename = filename[:-4]
    os.makedirs('output/' + filename)

    meta_data_list = []
    for track_index, track in enumerate(mid.tracks):
        absolute_time = 0
        for message_index, message in enumerate(track):
            absolute_time += message.time
            if message.is_meta:
                meta_message = message.dict()
                if len(meta_message) == 2:
                    meta_data_list.append([
                        track_index, absolute_time, str(
                            message.type), 'EOF'
                    ])
                elif len(meta_message) == 3:
                    meta_message.pop('type')
                    meta_message.pop('time')
                    for key, value in meta_message.items():
                        meta_data_list.append([
                            track_index, absolute_time, str(
                                message.type), value
                        ])
                else:
                    meta_message.pop('type')
                    meta_message.pop('time')
                    for key, value in meta_message.items():
                        meta_data_list.append([
                            track_index, absolute_time, f"{message.type}_{key}", value
                        ])
                meta_frame = pd.DataFrame(meta_data_list, columns=[
                                          'track', 'time', 'key', 'value'])
                meta_frame.to_csv(
                    f"output/{filename}/{filename}.csv", index=False)


if __name__ == "__main__":
    main(sys.argv[1:])
