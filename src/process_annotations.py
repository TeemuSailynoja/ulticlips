import json
from argparse import ArgumentParser
from typing import Any
import re

from click import MissingParameter
from networkx import is_empty


# Loop ower sentences.
def parse_annotation_file(segments: list) -> dict[str, Any] | None:
    game: dict[str, Any] = {"points": [dict()]}

    print("Todo: Parse players on field")
    print("Todo: Parse flow")

    re_od = r"(?P<team>home|away)( starts)?( on)? (?P<OD>offense|defense)"
    re_start_point = r"point starts|start now"
    re_end_point = r"point ends|end point"
    re_next_point = r"next point"

    sync_time, offset = sync(segments)

    for i, seg in enumerate(segments):
        # Todo: Allow for pauses and then syncing again.
        # Todo: Allow for corrections
        # Todo: Players on field
        # Marked by (home/away) players (on field) p1, p2, p3,...
        # If point ongoing, these get appended to the list of players, otherwise,
        # these are appended to the players of the next point.
        if False:
            players = ...
            game["points"][-1]["players"].append(players)

        # Todo: Flow
        if False:
            game["points"][-1]["flow"].append(...)

        matched_expressions = [
            {"type": t, "res": res, "start": res.span()[0]}
            for (t, res) in [
                (
                    "od",
                    re.search(
                        re_od,
                        seg["text"].lower(),
                    ),
                ),
                (
                    "start_p",
                    re.search(
                        re_start_point,
                        seg["text"].lower(),
                    ),
                ),
                (
                    "end_p",
                    re.search(
                        re_end_point,
                        seg["text"].lower(),
                    ),
                ),
                (
                    "next_p",
                    re.search(
                        re_next_point,
                        seg["text"].lower(),
                    ),
                ),
            ]
            if res
        ]
        matched_expressions.sort(key=lambda x: x["start"])

        for expr in matched_expressions:
            match expr["type"]:
                case "od":
                    add_od(game, expr["res"])
                case "start_p":
                    add_start_time(game, i, segments, sync_time - offset)
                case "end_p":
                    add_end_time(game, i, segments, sync_time - offset)
                case "next_p":
                    game["points"].append(dict())
    game["points"] = [point for point in game["points"] if point]
    return game


def sync(segments: list[dict]) -> tuple[int, int]:
    re_sync = r"(starting|start) time, (?P<hours>\d{1,2}) hours, (?P<minutes>\d{1,2}) minutes( and|, ) (?P<seconds>\d{1,2}) seconds"
    for i, seg in enumerate(segments):
        res_sync_time = re.search(re_sync, seg["text"].lower().replace("zero", "0"))
        if res_sync_time:
            sync_time = (
                3600 * int(res_sync_time["hours"])
                + 60 * int(res_sync_time["minutes"])
                + int(res_sync_time["seconds"])
            )
            for seg in segments[i:]:
                if re.search(r"(\b[n|N]ow\b)", seg["text"].lower()):
                    offset = 0
                    for w in seg["words"]:
                        if re.search(r"(\b[n|N]ow\b)", w["word"].lower()):
                            offset = int(w["start"])
                            break
                else:
                    continue
                return (sync_time, offset)
    raise MissingParameter(
        "Could not find start time specification. Can't sync video to voice recording."
    )


def add_od(game, res):
    if res["OD"] == "offense":
        game["points"][-1]["team_on_offense"] = res["team"]
    elif res["OD"] == "defense":
        if res["team"] == "home":
            game["points"][-1]["team_on_offense"] = "away"
        elif res["team"] == "away":
            game["points"][-1]["team_on_offense"] = "home"


def add_start_time(game, i, segments, time_delta):
    for seg in segments[i:]:
        if re.search(r"(\bnow\b)", seg["text"].lower()):
            for w in seg["words"]:
                if re.search(r"(\bnow\b)", w["word"].lower()):
                    game["points"][-1]["start_time"] = time_delta + int(w["start"])
                    break
        else:
            continue
        break


def add_end_time(game, i, segments, time_delta):
    for seg in segments[i:]:
        if re.search(r"(\bend\b|\bends\b)", seg["text"].lower()):
            for w in seg["words"]:
                if re.search(r"(\bend\b|\bends\b)", w["word"].lower()):
                    game["points"][-1]["end_time"] = time_delta + int(w["start"])
                    break
        else:
            continue
        break


if __name__ == "__main__":
    import pprint

    parser = ArgumentParser()
    parser.add_argument(
        "-i", "--input", dest="input", help="Path to unprocessed annotations"
    )
    parser.add_argument(
        "-o", "--output", dest="output", help="Desired output file path."
    )
    parser.add_argument(
        "-g",
        "--game_annotations",
        dest="game",
        help="Path to the JSON file containing the processed annotations for the input video. Default: annotations/games/{input_video_filename}.json",
    )
    args = parser.parse_args()
    with open(args.input) as f:
        game = parse_annotation_file(json.load(f)["segments"])
    pprint.pprint(game)
    with open(args.output, "a") as f:
        json.dump(game, f)
