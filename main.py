import pafy
import PySimpleGUI as sg
import os
import threading

def to_raw(string):
    return fr"{string}"


def remove_bad_characters(string):
    string = to_raw(video.title)
    string = string.replace('"', '')
    string = string.replace('/', '-')
    string = string.replace('\\', '-')
    string = string.replace('>', '')
    string = string.replace('<', '')
    string = string.replace('|', '-')
    string = string.replace('?', '')
    string = string.replace('*', '')
    string = string.replace(':', ' ')
    return string


def convert_format(file_name, previous_extension, extension):
    os.system('ffmpeg.exe -y -i "' + file_name + '.' + previous_extension + '" "' + file_name + '.' + extension + '"')


def download_video(video):
    title = remove_bad_characters(video.title)
    best_video = video.getbest()
    extension = best_video.extension
    best_video.download(title + '.' + extension)
    if best_video.extension != 'mp4':
        convert_format(title, extension, "mp4")
        os.remove(title + '.' + extension)


def download_audio(video):
    title = remove_bad_characters(video.title)
    audio = video.getbest()
    extension = audio.extension
    audio.download(title + '.' + audio.extension)
    if audio.extension != 'mp3':
        convert_format(title, extension, "mp3")
        os.remove(title + '.' + extension)


layout = [[sg.Text('Enter video link:'), sg.InputText()],
              [sg.Text('Select type:'), sg.Combo(['Video', 'Audio'], default_value='Video', readonly=True)],
              [sg.Text(size=(40, 1), key='-OUTPUT-')],
              [sg.Button('Download'), sg.Button('Quit')]]
window = sg.Window('Youtube downloader', layout, icon="logo.ico")


if __name__ == '__main__':
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Quit':
            break
        if event == 'Download':
            window['-OUTPUT-'].update("Downloading...")
            try:
                video = pafy.new(values[0])
                if values[1] == 'Video':
                    t1 = threading.Thread(target=download_video, args=(video,), daemon=True)
                    t1.start()
                elif values[1] == 'Audio':
                    t1 = threading.Thread(target=download_audio, args=(video,), daemon=True)
                    t1.start()
                else:
                    window['-OUTPUT-'].update("Unknown error, please retry")
                    continue
                window['-OUTPUT-'].update("File successfully downloaded!")
            except Exception as e:
                print(e)
                window['-OUTPUT-'].update("Error: invalid link, please retry")

    window.close()


