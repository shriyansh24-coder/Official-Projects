import json
import os
import sys


def get_data_file():

    if getattr(sys, "frozen", False):

        base_path = os.path.dirname(
            sys.executable
        )

    else:

        base_path = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

    data_folder = os.path.join(
        base_path,
        "data"
    )

    os.makedirs(
        data_folder,
        exist_ok=True
    )

    return os.path.join(
        data_folder,
        "playlist.json"
    )


def save_playlist(songs):

    data_file = get_data_file()

    try:

        with open(
            data_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                songs,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError as error:

        print(
            f"Could not save playlist: {error}"
        )


def load_playlist():

    data_file = get_data_file()

    if not os.path.exists(
        data_file
    ):

        return []

    try:

        with open(
            data_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

            if isinstance(data, list):
                return data

            return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []