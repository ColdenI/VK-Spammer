from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QThread
from PyQt5 import QtGui
import datetime
import vk_api
from ApiManager import APIManager
import sys, time, random
import CWR

#

users = []
messageText = []
victimID = []
TextMessageInfo = "<html>"

saveToken = []
saveID = []

isAutoSend = False
AutoSendFrom = 0
AutoSendTo = 100

SPtoken = None



app = QtWidgets.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon('des/ico.ico'))
ui = uic.loadUi("des/design.ui")
ui.setWindowIcon(QtGui.QIcon('des/ico.ico'))
Loger = CWR.CWRFile("data/log.txt")
SaveTokenData = CWR.CWRItem('data/tdata.cfg')
SaveIDData = CWR.CWRItem('data/idata.cfg')
SaveSettings = CWR.CWRItem('data/sdata.cfg')

class AThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):

        while True:
            global TextMessageInfo

            if isAutoSend and victimID != None:
                time.sleep(random.randint(AutoSendFrom, AutoSendTo) / 1000)

                for i in range(len(users)):
                    time.sleep(random.randint(AutoSendFrom, AutoSendTo) / 10000)
                    for ii in victimID:
                        sendMessageText(i, ii, messageText[random.randint(0, len(messageText) - 1)], False)

class AThread1(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            for i in users:
                ret = i.isMessage()
                if ret != None:
                    for ni in victimID:
                        if ret[1] != ni:
                            wrireLog("MESSAGE: for <" + i.token + "> from: " + str(ret[1]) + " text: " + str(ret[0]), "#c3c611")
                        else:
                            wrireLog("MESSAGE: for <" + i.token + "> from: " + str(ret[1]) + " text: " + str(ret[0]), "#267cfe")



def main():
    print("started\n\n")
    wrireLog("Program start\n", "#205a07")

    thread = AThread()
    thread.start()
    thread1 = AThread1()
    thread1.start()

    ui_connect()
    ui.show()
    app.exec()


    print("\n\nfinished")

def addID(id):
    global victimID
    victimID.append(int(id))
    wrireLog("ID has been successfully added", "#44cf1a")
    ui_update()
def Badd_ID():
    try:
        if ui.lineEdit_2.text() != "":
            addID(int(ui.lineEdit_2.text()))
        else:
            wrireLog("! id is not valid!".upper() + " enter the ID", "#d30000")
    except ValueError:
        wrireLog("! id is invalid!".upper() + " enter the ID", "#d30000")

    ui_update()
def Bremove_id():
    if ui.listWidget_3.currentRow() != -1:
        victimID.remove(victimID[ui.listWidget_3.currentRow()])
        wrireLog("ID has been successfully deleted", "#44cf1a")
    else:
        wrireLog("! id was not found!".upper() + " select a ID", "#d30000")
    ui_update()

def Badd_Message():
    if ui.lineEdit_3.text() != "":
        addMessage(ui.lineEdit_3.text())
    else:
        wrireLog("! Message text is not valid!".upper() + " enter the token", "#d30000")
        ui_update()
def addMessage(text):
    if text != "":
        messageText.append(text)
        wrireLog("Message text has been successfully added", "#44cf1a")
        ui_update()
    else:
        wrireLog("! message text is not valid!".upper() + " enter the text", "#d30000")
        ui_update()
def Bremove_message():
    if ui.listWidget_2.currentRow() != -1:
        messageText.remove(messageText[ui.listWidget_2.currentRow()])
        wrireLog("Message text has been successfully deleted", "#44cf1a")
    else:
        wrireLog("! Message text was not found!".upper() + " select a text message", "#d30000")
    ui_update()

def addToken(token):
    if token != "":
        try:
            users.append(APIManager(str(token)))
            wrireLog("Token has been successfully added", "#44cf1a")
            #users[0].SendTextMessage(554354587, str(token))
            ui_update()
        except vk_api.exceptions.ApiError:
            wrireLog("!!! TOKEN is not valid!".upper() + " check the token", "#d30000")
            ui_update()
    else:
        wrireLog("! TOKEN is not valid!".upper() + " enter the token", "#d30000")
        ui_update()
def Badd_token():
    if ui.lineEdit.text() != "":
        addToken(ui.lineEdit.text())
    else:
        wrireLog("! TOKEN is not valid!".upper() + " enter the token", "#d30000")
        ui_update()
def Bremove_token():
    if ui.listWidget.currentRow() != -1:
        users.remove(users[ui.listWidget.currentRow()])
        wrireLog("Token has been successfully deleted", "#44cf1a")
    else:
        wrireLog("! TOKEN was not found!".upper() + " select a token", "#d30000")
    ui_update()

def sendMessageText(index, id, msg, isUiUpdate = True):
    if len(messageText) > 0:
        try:
            users[index].SendTextMessage(id, msg)
        except vk_api.exceptions.ApiError:
            wrireLog("! invalid user id!".upper() + " check the user ID", "#d30000")
            if isUiUpdate:
                ui_update()
    else:
        wrireLog("! invalid message text!".upper() + " add a message text", "#d30000")
        if isUiUpdate:
            ui_update()


def BsendMessage():
    ind_token = ui.listWidget.currentRow()
    ind_id = ui.listWidget_3.currentRow()
    ind_msg = ui.listWidget_2.currentRow()

    if ind_id != -1:
        if ind_msg != -1:
            if ind_token != -1:
                sendMessageText(ind_token, victimID[ind_id], messageText[ind_msg])
            else:
                wrireLog("! Token was not found!".upper() + " select a token", "#d30000")
        else:
            wrireLog("! Message text was not found!".upper() + " select a message text", "#d30000")
    else:
        wrireLog("! ID was not found!".upper() + " select a ID", "#d30000")

    ui_update()

def BsetAuto():
    global isAutoSend, AutoSendTo, AutoSendFrom
    if ui.checkBox.checkState() == 2:
        isAutoSend = True
    else:
        isAutoSend = False

    ui.spinBox_2.setMinimum(ui.spinBox.value() + 1)

    AutoSendFrom = int(ui.spinBox.value())
    AutoSendTo = int(ui.spinBox_2.value())

    wrireLog("Auto send message - " + str(isAutoSend) + "  from " + str(AutoSendFrom) + "  to " + str(AutoSendTo), "#55aa7f")

    ui_update()

def Bclear_input_token():
    ui.lineEdit.setText("")
def Bclear_input_id():
    ui.lineEdit_2.setText("")
def Bclear_input_message():
    ui.lineEdit_3.setText("")

def loadData():
    saveID.clear()
    saveToken.clear()

    try:
        for i in SaveIDData.getItems():
            saveID.append(str(i) + " - " + str(SaveIDData.getItem(i)))

        for i in SaveTokenData.getItems():
            saveToken.append(str(i) + " - " + str(SaveTokenData.getItem(i)))

    except FileNotFoundError:
        wrireLog(" !! DATA CANNOT BE READ! - first create a save", "#d30000")


    ui_update()

def saveIDData(id, name):
    SaveIDData.addItem(id, name)
def saveTokenData(token, name):
    SaveTokenData.addItem(token, name)

def BsaveID():
    try:
        saveIDData(int(ui.lineEdit_8.text()), ui.lineEdit_4.text())
        ui.lineEdit_8.setText("")
        ui.lineEdit_4.setText("")
        loadData()
    except ValueError:
        ui.lineEdit_8.setText("")
        ui.lineEdit_4.setText("")
        wrireLog("! id is invalid!".upper() + " enter the ID", "#d30000")
        ui_update()
def BsaveToken():
    saveTokenData(ui.lineEdit_5.text(), ui.lineEdit_7.text())
    ui.lineEdit_5.setText("")
    ui.lineEdit_7.setText("")
    loadData()

def BopensaveToken():
    ui.lineEdit_6.setText(str(saveToken[ui.listWidget_4.currentRow()]).split(" - ")[0])
def BopensaveID():
    ui.lineEdit_6.setText(str(saveID[ui.listWidget_5.currentRow()]).split(" - ")[0])

def BsaveRamoveToken():
    try:
        if ui.listWidget_4.currentRow() != -1:
            if SaveTokenData.containsItem(str(saveToken[ui.listWidget_4.currentRow()]).split(" - ")[0]):
                SaveTokenData.removeItem(str(saveToken[ui.listWidget_4.currentRow()]).split(" - ")[0])
                #saveToken.remove(saveToken[ui.listWidget_4.currentRow()])
                loadData()
    except Exception as e:
        print(e)
def BsaveRamoveID():
    try:
        if ui.listWidget_5.currentRow() != -1:
            if SaveIDData.containsItem(str(saveID[ui.listWidget_5.currentRow()]).split(" - ")[0]):
                SaveIDData.removeItem(str(saveID[ui.listWidget_5.currentRow()]).split(" - ")[0])
                #saveToken.remove(saveToken[ui.listWidget_4.currentRow()])
                loadData()
    except Exception as e:
        print(e)

def getDataProfile():
    try:
        global SPtoken
        SPtoken = APIManager(ui.lineEdit_13.text())
        _data = SPtoken.GetProfileInfo()

        ui.label_16.setText(str(_data.get('id')))
        ui.label_17.setText(str(_data.get('home_town', "None")))
        ui.label_18.setText(str(_data.get('status', "None")))
        ui.label_19.setText(str(_data.get('first_name', "None")))
        ui.label_23.setText(str(_data.get('last_name', "None")))
        ui.label_24.setText(str(_data.get('bdate', "None")))
        ui.label_25.setText(str(_data.get('bdate_visibility', "None")))
        try:
            ui.label_28.setText(str(_data['city']['title']))
        except Exception as ex:
            ui.label_28.setText("error")
        try:
            ui.label_30.setText(str(_data['country']['title']))
        except Exception as ex:
            ui.label_30.setText("error")
        ui.label_32.setText(str(_data.get('relation', "None")))
        ui.label_35.setText(str(_data.get('screen_name', "None")))
        ui.label_37.setText(str(_data.get('sex', "None")))


        ui.lineEdit_11.setText(str(_data.get('home_town', "None")))
        ui.lineEdit_10.setText(str(_data.get('status', "None")))
        ui.lineEdit_9.setText(str(_data.get('first_name', "None")))
        ui.lineEdit_14.setText(str(_data.get('last_name', "None")))
        ui.lineEdit_15.setText(str(_data.get('bdate', "None")))
        ui.lineEdit_16.setText(str(_data.get('bdate_visibility', "None")))
        ui.lineEdit_19.setText(str(_data.get('relation', "None")))
        ui.lineEdit_21.setText(str(_data.get('sex', "None")))

        for i in (ui.pushButton_17, ui.pushButton_16, ui.pushButton_21, ui.pushButton_28, ui.pushButton_22, ui.pushButton_23, ui.pushButton_18, ui.pushButton_26):
            i.setEnabled(True)

        #SPtoken.SetProfileInfo_status("5467")

    except vk_api.exceptions.ApiError:
        wrireLog("!!! TOKEN is not valid!".upper() + " check the token", "#d30000")
        ui_update()

def setDataProfileStatus():
    try:
        SPtoken.SetProfileInfo_status(ui.lineEdit_10.text())
    except vk_api.exceptions.ApiError:
        wrireLog("!!! invalid parameter!".upper() + " check the parameter", "#d30000")
        ui_update()
def setDataProfileFirstName():
    try:
        SPtoken.SetProfileInfo_first_name(ui.lineEdit_9.text())
    except vk_api.exceptions.ApiError:
        wrireLog("!!! invalid parameter!".upper() + " check the parameter", "#d30000")
        ui_update()
def setDataProfileLastName():
    try:
        SPtoken.SetProfileInfo_last_name(ui.lineEdit_14.text())
    except vk_api.exceptions.ApiError:
        wrireLog("!!! invalid parameter!".upper() + " check the parameter", "#d30000")
        ui_update()
def setDataProfileSex():
    try:
        SPtoken.SetProfileInfo_sex(ui.lineEdit_21.text())
    except vk_api.exceptions.ApiError:
        wrireLog("!!! invalid parameter!".upper() + " check the parameter", "#d30000")
        ui_update()
def setDataProfileBDate():
    try:
        SPtoken.SetProfileInfo_bdate(ui.lineEdit_15.text())
    except vk_api.exceptions.ApiError:
        wrireLog("!!! invalid parameter!".upper() + " check the parameter", "#d30000")
        ui_update()
def setDataProfileBDateV():
    try:
        SPtoken.SetProfileInfo_bdate_visibility(ui.lineEdit_16.text())
    except vk_api.exceptions.ApiError:
        wrireLog("!!! invalid parameter!".upper() + " check the parameter", "#d30000")
        ui_update()
def setDataProfileHometown():
    try:
        SPtoken.SetProfileInfo_home_town(ui.lineEdit_11.text())
    except vk_api.exceptions.ApiError:
        wrireLog("!!! invalid parameter!".upper() + " check the parameter", "#d30000")
        ui_update()
def setDataProfileRelation():
    try:
        SPtoken.SetProfileInfo_relation(ui.lineEdit_19.text())
    except vk_api.exceptions.ApiError:
        wrireLog("!!! invalid parameter!".upper() + " check the parameter", "#d30000")
        ui_update()

def ui_update():
    ui.infoText.setText(TextMessageInfo)

    ui.listWidget.clear()
    for i in users:
        ui.listWidget.addItem(i.token)

    ui.listWidget_2.clear()
    for i in messageText:
        ui.listWidget_2.addItem(i)

    ui.listWidget_3.clear()
    for i in victimID:
        ui.listWidget_3.addItem(str(i))

    ui.listWidget_4.clear()
    for i in saveToken:
        ui.listWidget_4.addItem(str(i))

    ui.listWidget_5.clear()
    for i in saveID:
        ui.listWidget_5.addItem(str(i))






def ui_connect():
    ui.pushButton_4.clicked.connect(ui_update)
    ui.pushButton.clicked.connect(Badd_ID)
    ui.pushButton_2.clicked.connect(Badd_Message)
    ui.ButtonAddToken.clicked.connect(Badd_token)
    ui.pushButton_5.clicked.connect(Bremove_token)
    ui.pushButton_3.clicked.connect(BsendMessage)
    ui.checkBox.clicked.connect(BsetAuto)
    ui.spinBox.valueChanged.connect(BsetAuto)
    ui.spinBox_2.valueChanged.connect(BsetAuto)
    ui.pushButton_6.clicked.connect(Bremove_message)
    ui.pushButton_7.clicked.connect(Bremove_id)

    ui.pushButton_8.clicked.connect(Bclear_input_token)
    ui.pushButton_9.clicked.connect(Bclear_input_id)
    ui.pushButton_10.clicked.connect(Bclear_input_message)

    ui.pushButton_13.clicked.connect(loadData)
    ui.pushButton_12.clicked.connect(BsaveToken)
    ui.pushButton_11.clicked.connect(BsaveID)

    ui.listWidget_4.itemSelectionChanged.connect(BopensaveToken)
    ui.listWidget_5.itemSelectionChanged.connect(BopensaveID)

    ui.pushButton_14.clicked.connect(BsaveRamoveToken)
    ui.pushButton_15.clicked.connect(BsaveRamoveID)

    ui.pushButton_20.clicked.connect(getDataProfile)

    ui.pushButton_17.clicked.connect(setDataProfileStatus)
    ui.pushButton_16.clicked.connect(setDataProfileFirstName)
    ui.pushButton_21.clicked.connect(setDataProfileLastName)
    ui.pushButton_28.clicked.connect(setDataProfileSex)
    ui.pushButton_22.clicked.connect(setDataProfileBDate)
    ui.pushButton_23.clicked.connect(setDataProfileBDateV)
    ui.pushButton_18.clicked.connect(setDataProfileHometown)
    ui.pushButton_26.clicked.connect(setDataProfileRelation)


def wrireLog(text, color = "#000000"):
    global TextMessageInfo
    now = datetime.datetime.now()
    text = str(now).split(".")[0] + "   -   " + text
    TextMessageInfo = '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-size:8.25pt; color:' + color + ';">' + text + '</span></p>' + TextMessageInfo
    Loger.append("\n" + text)

if __name__ == '__main__':
    main()