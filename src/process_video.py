from argparse import ArgumentParser
from glob import glob
import json
import ffmpeg


def get_fps(path: str) -> int:
    probe = ffmpeg.probe(filename=args.input)
    video_info = next(s for s in probe["streams"] if s["codec_type"] == "video")
    return int(video_info["r_frame_rate"].split("/")[0])


def split_points(input_path: str, output_path: str, points: list[dict]) -> None:
    input = ffmpeg.input(filename=input_path)
    fps = get_fps(path=input_path)

    for idx, point in enumerate(points):
        (
            input.trim(start_frame=point["start"] * fps, end_frame=point["end"] * fps)
            .setpts("PTS-STARTPTS")
            .output(f"-{idx+1}.".join(output_path.split(sep=".")))
            .run()
        )


def join_points(input_paths: list[str], output_path: str) -> None:
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

    split_points(
        input_path=args.input,
        output_path=args.output,
        points=json.load(args.game)["points"],
    )

    join_points(
        input_paths=glob(args.output.split(".")[0] + "*." + args.output.split(".")[1]),
        output_path=args.output,
    )
