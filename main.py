import argparse

from enums import Mode, Info
from tiktokbot import TikTok


def banner() -> None:
    """
    Prints a banner with the name of the tool and its version number.
    """
    print(Info.BANNER)

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-user",
                        dest="user",
                        help="record a live from the username.",
                        action='store')
    parser.add_argument("-room_id",
                        dest="room_id",
                        help="record a live from the room_id.",
                        action='store')
    parser.add_argument("-mode",
                        dest="mode",
                        help="recording mode: (manual,automatic) [Default: manual]\n[manual] => manual live recording\n[automatic] => automatic live recording when the user is in live).",
                        default="manual",
                        action='store')
    parser.add_argument("-output",
                        dest="output",
                        help="output dir",
                        action='store')
    parser.add_argument("-ffmpeg", 
                        dest="ffmpeg",
                        help="recording via ffmpeg, allows real-time conversion to mp4",
                        action="store_const",
                        const=True)
    parser.add_argument("-duration",
                        dest="duration",
                        help="duration in seconds to record the live [Default: None]",
                        type=int,
                        default=None,
                        action='store')
    parser.add_argument("--auto-convert",
                    dest="auto_convert",
                    help="enable auto video conversion [Default: False]",
                    action='store_true')

    args = parser.parse_args()
    return args


def main():
    banner()

    user = None
    mode = None
    room_id = None
    use_ffmpeg = None

    args = parse_args()

    try:
        if not args.user and not args.room_id:
            raise Exception("[-] Missing user/room_id value")

        if not args.mode:
            raise Exception("[-] Missing mode value")
        if args.mode and args.mode != "manual" and args.mode != "automatic":
            raise Exception("[-] Incorrect -mode value")

        if args.user and args.room_id:
            raise Exception("[-] Enter the username or room_id, not both.")
        
        user = args.user
        room_id = args.room_id
        if args.mode == "manual":
            mode = Mode.MANUAL
        else:
            mode = Mode.AUTOMATIC

        if args.ffmpeg:
            use_ffmpeg = True
        elif mode == Mode.AUTOMATIC:
            raise Exception("[-] To use automatic mode, add -ffmpeg flag.")
    except Exception as ex:
        print(ex)
        exit(1)

    try:
        bot = TikTok(
            output=args.output,
            mode=mode,
            user=user,
            room_id=room_id,
            use_ffmpeg=use_ffmpeg,
            duration=args.duration,
            convert=args.auto_convert
        )
        bot.run()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
