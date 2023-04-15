# This program takes a midi, quickly describes it and converts it to CSV

# Imports

import sys
import mido
import pandas as pd


def main(args):
    for filename in args:
        mid = mido.MidiFile(filename)
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

        for metadata in meta_data_list:
            print(metadata)

        meta_frame = pd.DataFrame(columns=['Type', 'Value', 'Time'])
        note_frame = pd.DataFrame()


if __name__ == "__main__":
    main(sys.argv[1:])
