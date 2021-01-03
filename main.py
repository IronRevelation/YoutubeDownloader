import pafy
import PySimpleGUI as sg
import os


def to_raw(string):
    return fr"{string}"


layout = [[sg.Text('Enter video link:'), sg.InputText()],
            [sg.Text('Select type:'), sg.Combo(['Video', 'Audio'], default_value='Video', readonly=True)],
            [sg.Text(size=(40,1), key='-OUTPUT-')],
            [sg.Button('Download'), sg.Button('Quit')]]

# Create the Window
window = sg.Window('Youtube downloader', layout, icon="logo.ico")
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':
        break
    try:

        video = pafy.new(values[0])
        raw_title = to_raw(video.title)
        raw_title = raw_title.replace('"', '')
        raw_title = raw_title.replace('/', '-')
        raw_title = raw_title.replace('\\', '-')
        raw_title = raw_title.replace('>', '')
        raw_title = raw_title.replace('<', '')
        raw_title = raw_title.replace('|', '-')
        raw_title = raw_title.replace('?', '')
        raw_title = raw_title.replace('*', '')
        raw_title = raw_title.replace(':', ' ')

        if values[1] == 'Video':
            best_video = video.getbest()
            best_video.download(raw_title + '.' + best_video.extension)
            if best_video.extension != 'mp4':
                os.system('ffmpeg.exe -y -i "'+raw_title + '.' + best_video.extension+'" "' + raw_title +'.mp4"')
                os.remove(video.title + '.' + best_video.extension)

        elif values[1] == 'Audio':
            audio = video.getbestaudio()
            audio.download(raw_title + '.' + audio.extension)
            if audio.extension != 'mp3':
                os.system('ffmpeg.exe -y -i "'+raw_title + '.' + audio.extension+'" "' + raw_title +'.mp3"')
                os.remove(raw_title + '.' + audio.extension)

        else:
            window['-OUTPUT-'].update("Unknown error, please retry")
            continue

        window['-OUTPUT-'].update("File successfully downloaded!")
    except:
        window['-OUTPUT-'].update("Error: invalid link, please retry")

window.close()


