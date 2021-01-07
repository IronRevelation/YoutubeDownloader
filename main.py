import pafy
import PySimpleGUI as sg
import os
import threading


def to_raw(string):
    return fr"{string}"


def remove_bad_characters(string):
    temp = to_raw(string)
    temp = temp.replace('"', '')
    temp = temp.replace('/', '-')
    temp = temp.replace('\\', '-')
    temp = temp.replace('>', '')
    temp = temp.replace('<', '')
    temp = temp.replace('|', '-')
    temp = temp.replace('?', '')
    temp = temp.replace('*', '')
    temp = temp.replace(':', ' ')
    return temp


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


def download_single_file(video, type):
    if type == 'Video':
        download_video(video)
    elif type == 'Audio':
        download_audio(video)
    else:
        window['-OUTPUT-'].update("Unknown error, please retry")
        return
    window.write_event_value('-THREAD DONE-', remove_bad_characters(video.title))


def download_playlist(playlist, type):
    pl_title = remove_bad_characters(playlist['title'])

    if not os.path.exists(pl_title):
        os.makedirs(pl_title)

    for video in playlist['items']:
        if type == 'Video':
            download_video(video['pafy'])
            try:
                os.rename(video['pafy'].title+'.mp4', pl_title + '\\'+video['pafy'].title+'.mp4')
            except:
                os.remove(video['pafy'].title+'.mp4')
        elif type == 'Audio':
            download_audio(video['pafy'])
            try:
                os.rename(video['pafy'].title + '.mp3', pl_title + '\\' + video['pafy'].title + '.mp3')
            except:
                os.remove(video['pafy'].title+'.mp4')
        else:
            window['-OUTPUT-'].update("Unknown error, please retry")
            return
    window.write_event_value('-THREAD DONE-', "playlist")


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
                t1 = threading.Thread(target=download_single_file, args=(video,values[1]), daemon=True)
                t1.start()
            except Exception as e:
                print(e)
                try:
                    playlist = pafy.get_playlist(values[0])
                    t1 = threading.Thread(target=download_playlist, args=(playlist, values[1]), daemon=True)
                    t1.start()
                except Exception as ex:
                    print(ex)
                    window['-OUTPUT-'].update("Error: invalid link, please retry")
        if event == '-THREAD DONE-':
            window['-OUTPUT-'].update("")
            sg.popup_non_blocking(str(values['-THREAD DONE-'])+' successfully downloaded', icon="logo.ico")

    window.close()


