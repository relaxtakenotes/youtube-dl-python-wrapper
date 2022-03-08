import pyperclip
import traceback
import subprocess
import shlex
import colorama
import sys
import ctypes
colorama.init(convert=True)
had_output = bool()

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    had_output = False
    end_result = str()
    while True:
        out = process.stdout.read(1).decode()
        if out == '' and process.poll() is not None:
            break
        if out != '':
            had_output = True
            sys.stdout.write(out)
            end_result += out
    if not had_output:
        raise ValueError("No output. Check if you entered the parameters or the url right.")
    if "[error]" in end_result.lower():
        raise Exception("Something went wrong. I don't know. Look above...")

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

    print(f"{colorama.Fore.GREEN}[Task done!]{colorama.Style.RESET_ALL}")
    ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)
    input()

    return True

if __name__ == "__main__":
    while True:
        try:
            if main():
                break
        except Exception:
            print(f"{colorama.Fore.RED}{traceback.format_exc()}{colorama.Style.RESET_ALL}")
            print(f"{colorama.Fore.RED}[Execution failed. Press any button to try again or press ctrl+c to exit.]{colorama.Style.RESET_ALL}")
            input()
