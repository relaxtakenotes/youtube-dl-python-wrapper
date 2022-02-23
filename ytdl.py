import pyperclip
import traceback
import subprocess
import shlex
import colorama
import sys
colorama.init(convert=True)

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        out = process.stdout.read(1).decode()
        if out == '' and process.poll() is not None:
            break
        if out != '':
            sys.stdout.write(out)

def main():
    link = pyperclip.paste()
    print(f"{colorama.Fore.CYAN}Your link: {link}{colorama.Style.RESET_ALL}")
    print(f"{colorama.Fore.CYAN}(A)udio, (V)ideo+Audio, (C)ustom, Update (L)ink: {colorama.Style.RESET_ALL}", end='')
    choice = input() # colorama doesnt seem to work properly when put in the input function so yeah

    match choice.lower():
        case "a":
            print(f"{colorama.Fore.CYAN}[Downloading audio...]{colorama.Style.RESET_ALL}")
            run_command(f'youtube-dl -o "%USERPROFILE%\\Desktop\\%(uploader)s - %(title)s.%(ext)s" --extract-audio --audio-format mp3 --audio-quality 0 {link}')
        case "v":
            run_command(f"youtube-dl -F {link}")
            video_code = input("Choose the video parameter: ")
            print(f"{colorama.Fore.CYAN}[Downloading the video...]{colorama.Style.RESET_ALL}")
            run_command(f'youtube-dl -o "%USERPROFILE%\\Desktop\\%(uploader)s - %(title)s.%(ext)s" -f {video_code}+140 {link}')
        case "c":
            run_command(f"youtube-dl -F {link}")
            params = input("Choose the parameters(<video_param>+<audio_param>): ")
            print(f"{colorama.Fore.CYAN}[Downloading the video with custom parameters...]{colorama.Style.RESET_ALL}")
            run_command(f'youtube-dl -o "%USERPROFILE%\\Desktop\\%(uploader)s - %(title)s.%(ext)s" -f {params} {link}')
        case "l":
            main()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        print(traceback.format_exc())
        print("Press any button to exit.")
        input()
