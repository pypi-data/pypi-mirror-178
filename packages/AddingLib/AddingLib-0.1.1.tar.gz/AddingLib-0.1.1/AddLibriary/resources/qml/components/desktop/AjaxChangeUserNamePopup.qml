import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/hub/popups/"
import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 360
    height: 180

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var nameField: null
    property var currentName: null

    Rectangle {
        width: 360
        height: 180
        color: "#252525"

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.username
        }

        AjaxSettingsTextField {
            id: userNameField

            miniText: ""
            field.text: currentName
            field.focus: true

            width: popup.width - 64

            Keys.onEnterPressed: {
                saveCancel.saveArea.clicked(true)
            }

            Keys.onReturnPressed: {
                saveCancel.saveArea.clicked(true)
            }

            field.onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            field.onTextChanged: {
                userNameField.field.text = util.validator(field.text, 24)
                return
            }

            anchors {
                top: closeItem.bottom
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }
        }

        AjaxSaveCancel {
            id: saveCancel
            anchors.bottom: parent.bottom

            cancelArea.onClicked: {
                popup.close()
            }

            saveArea.onClicked: {
                var userName = userNameField.field.text.trim()
                if (!userName) {
                    userNameField.field.focus = false
                    userNameField.field.valid = false
                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }
                nameField.field.text = userName
                popup.close()
            }
        }
    }
}