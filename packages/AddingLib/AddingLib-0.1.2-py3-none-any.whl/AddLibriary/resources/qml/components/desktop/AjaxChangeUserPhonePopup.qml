import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/popups.js" as Popups


AjaxPopup {
    id: popup
    width: 360
    height: 223

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    Rectangle {
        width: 360
        height: 223
        color: "#252525"

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.change_phone_number
        }

        AjaxSettingsTextField {
            id: newPhoneField
            miniText: tr.new_phone_number
            field.validator: RegExpValidator { regExp: /^[\+]?[0-9]{7,19}$/ }
            field.placeholderText: "+"

            width: popup.width - 64

            field.focus: true

            field.onTextChanged: {
                var t = field.text;
                if (t && !t.includes("+")) {
                    field.text = "+" + t
                }
            }

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

            anchors {
                top: closeItem.bottom
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }
        }

        AjaxSettingsTextField {
            id: userPasswordField
            miniText: tr.password
            password: true
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

            anchors {
                top: newPhoneField.bottom
                topMargin: 8
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
                var newPhone = newPhoneField.field.text
                var userPassword = userPasswordField.field.text
                if (!newPhone || newPhone == "+" || !userPassword) {
                    if (!newPhone || newPhone == "+") {
                        newPhoneField.field.focus = false
                        newPhoneField.field.valid = false
                    }
                    if (!userPassword) {
                        userPasswordField.field.focus = false
                        userPasswordField.field.valid = false
                    }

                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                client.change_user_phone(newPhone, userPassword)
            }
        }
    }

    Connections {
        target: client

        onChangeUserDataSuccess: {
            popup.close()
        }
    }
}