import PIL
import PySimpleGUI as sg
from PIL import Image
import os
from io import BytesIO
import requests
from threading import Thread



# Define the layout of the GUI


#server_url = 'http://127.0.0.1:5000/api/v3?type=img'
server_url = "http://192.168.29.73:5000/api/v3?type=img"


def makeRequest(url,files):
    r = requests.post(url, files={'file': open(files, 'rb')})
    print(r.text)

sg.theme('DarkAmber')


layout = [
    [
        sg.Text("Upload an Image: "),
        sg.Input(key='-FILE-'),
        sg.FileBrowse(),
        sg.Button("Load Image")
    ],
    [sg.Image(key='-IMG-')],
    [sg.Text(key='-TXT-')]
]


# Create the window
window = sg.Window('IntelliDoc by Anand and Amogh', layout)
window.SetIcon()
while True:

    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Load Image':
        filename = values['-FILE-']
        text = None
        try:
            if os.path.exists(filename):
                img = Image.open(filename)
                img.thumbnail(size=(500,500))
                bin = BytesIO()
                img.save(bin,format='PNG')
                window["-IMG-"].update(data=bin.getvalue())
                window["-TXT-"].update("Connecting to Server...")
                result = Thread(target=makeRequest,args=(server_url,filename))
                result.start()



        except AttributeError:
            sg.popup_error("Please upload a file.")
        except PIL.UnidentifiedImageError:
            sg.popup_error("Select Image")

# Close the window
window.close()




