from argparse import ArgumentParser
from glob import glob
import json
from os import read
import ffmpeg


def get_fps(path: str) -> int:
    """Extract the fps of the video indicated by a file path."""
    probe = ffmpeg.probe(filename=args.input)
    video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
    return int(video_info["r_frame_rate"].split("/")[0])


def split_points(input_path: str, output_path: str, points: list[dict]) -> None:
    """Split video into points and save the points as separate points

    Args:
        input_path (str): path to the full video
        output_path (str): desired output path to the point clips.
        points (list[dict]): a dictionary containing information "start_time"
                             and "end_time" for each point.
    """
    input = ffmpeg.input(filename=input_path)
    fps = get_fps(path=input_path)

    for idx, point in enumerate(points):
        (
            input.trim(
                start_frame=point["start_time"] * fps, end_frame=point["end_time"] * fps
            )
            .setpts("PTS-STARTPTS")
            .output(f"-{idx+1}.".join(output_path.split(sep=".")))
            .run()
        )


def join_videos(input_paths: list[str], output_path: str) -> None:
    """Clue a set of videos into a single one.

    Args:
        input_paths (list[str]): list of filepaths of the clips to join.
        output_path (str): desired destination to the combined video.
    """
    (
        ffmpeg.concat(
            *[ffmpeg.input(filename=input_path) for input_path in input_paths]
        )
        .output(output_path)
        .run()
    )


if __name__ == "__main__":
    # Parse command line arguments. For now here, but should probably be moved to a separate function.
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", dest="input", help="Path to input mp4")
    parser.add_argument(
        "-o", "--output", dest="output", help="Path to desired output mp4"
    )
    parser.add_argument(
        "-g",
        "--game_annotations",
        dest="game",
        help="Path to the JSON file containing the processed annotations for the input video. Default: annotations/games/{input_video_filename}.json",
    )
    args = parser.parse_args()

    # Read the json data for point annotations
    with open(args.game, "r") as f:
        points = json.load(f)["points"]

    # Generate a separate video file for each point.
    split_points(
        input_path=args.input,
        output_path=args.output,
        points=points,
    )

    # Join the points into a single video.
    join_videos(
        input_paths=glob(args.output.split(".")[0] + "*." + args.output.split(".")[1]),
        output_path=args.output.replace("points", "output"),
    )
