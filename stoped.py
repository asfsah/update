import PySimpleGUI as sg

# ウィンドウのレイアウト
layout = [
    [sg.Text('Account suspended.', font=('Helvetica', 20, 'bold'), background_color='#222', text_color='white', size=(30, 2), justification='center')],
    [sg.Multiline('This account has already been deleted by the administrator. Only the administrator knows the cause of the deletion. Please re-read the Terms of Use and wait to purchase again.', font=('Helvetica', 12), background_color='#222', text_color='white', size=(30, 5), disabled=True, border_width=0, justification='center')],
    [sg.Button('Close', button_color=('white', 'red'))]
]

# ウィンドウの作成
window = sg.Window('My Window', layout, background_color='#222', finalize=True, element_justification='center', size=(512, 512))

# ウィンドウの表示
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Close':
        break

# ウィンドウの終了
window.close()
