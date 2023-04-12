# encoding:utf-8

from PyQt6.QtWidgets import QMessageBox

icon_type = {
    "NoIcon": QMessageBox.Icon.NoIcon,
    "Critical": QMessageBox.Icon.Critical,
    "Information": QMessageBox.Icon.Information,
    "Question": QMessageBox.Icon.Question,
    "Warning": QMessageBox.Icon.Warning,
}

button_type = {
    "NoButton" : QMessageBox.StandardButton.NoButton,
    "Ok" : QMessageBox.StandardButton.Ok,
    "Save" : QMessageBox.StandardButton.Save,
    "SaveAll" : QMessageBox.StandardButton.SaveAll,
    "Open" : QMessageBox.StandardButton.Open,
    "Yes" : QMessageBox.StandardButton.Yes,
    "YesToAll" : QMessageBox.StandardButton.YesAll,
    "No" : QMessageBox.StandardButton.No,
    "NoToAll" : QMessageBox.StandardButton.NoAll,
    "Abort" : QMessageBox.StandardButton.Abort,
    "Retry" : QMessageBox.StandardButton.Retry,
    "Ignore" : QMessageBox.StandardButton.Ignore,
    "Close" : QMessageBox.StandardButton.Close,
    "Cancel" : QMessageBox.StandardButton.Cancel,
    "Discard" : QMessageBox.StandardButton.Discard,
    "Help" : QMessageBox.StandardButton.Help,
    "Apply" : QMessageBox.StandardButton.Apply,
    "Reset" : QMessageBox.StandardButton.Reset,
    "RestoreDefaults" : QMessageBox.StandardButton.RestoreDefaults,
    "FirstButton" : QMessageBox.StandardButton.FirstButton,
    "LastButton" : QMessageBox.StandardButton.LastButton,
    "YesAll" : QMessageBox.StandardButton.YesAll,
    "NoAll" : QMessageBox.StandardButton.NoAll,
    "Default" : QMessageBox.StandardButton.Default,
    "Escape" : QMessageBox.StandardButton.Escape,
    "FlagMask" : QMessageBox.StandardButton.FlagMask,
    "ButtonMask" : QMessageBox.StandardButton.ButtonMask
}

def showdialog(
    text: str,
    informative_text: str="",
    window_title: str="",
    detailed_text: str="",
    icon: str="NoIcon",
    buttons: list[str]= []
    ):
    """Print a popup with the given information
    
    Args:
        text (str): The main message to show
        informative_text (str): Additional information
        window_title (str): The title of the window
        detailed_text (str): A text printed in a messagebox at the bottom of the popup
        icon (str): The type of icon to show (can be : NoIcon, Critical, Information, Question, Warning)
            The default value is "NoIcon"
        buttons (list[str]): Define the buttons to show on the popup (can be :  "NoButton", "Ok", "Save",
            "SaveAll", "Open", "Yes", "YesToAll", "No", "NoToAll", "Abort", "Retry", "Ignore", "Close", 
            "Cancel", "Discard", "Help", "Apply", "Reset", "RestoreDefaults", "FirstButton" , "LastButton", 
            "YesAll", "NoAll", "Default", "Escape", "FlagMask", "ButtonMask")
    Return:
        The value of the button clicked
    
    """
    msg = QMessageBox()
    msg.setIcon(icon_type[icon])

    msg.setText(text)
    if informative_text != "":
        msg.setInformativeText(informative_text)
    if window_title != "":
        msg.setWindowTitle(window_title)
    if detailed_text != "":
        msg.setDetailedText(detailed_text)
    if len(buttons) > 0:
        btn_args = button_type[buttons.pop(0)]
        for btn in buttons:
            btn_args |= button_type[btn]
        msg.setStandardButtons(btn_args)

    #msg.buttonClicked.connect(msgbtn)
        
    return msg.exec()