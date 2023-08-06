import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/hub/popups/"
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
            label: tr.change_email
        }

        AjaxSettingsTextField {
            id: userEmailField
            miniText: tr.new_email_address
            field.validator: RegExpValidator { regExp: /^[0-9a-zA-Zа-яА-Я]+([\.+-_]?[0-9a-zA-Zа-яА-Я]+)*@[0-9a-zA-Zа-яА-Я]+([\.+-_]?[0-9a-zA-Zа-яА-Я]+)*(\.[0-9a-zA-Zа-яА-Я]{2,3})+$/ }

            width: popup.width - 64

            field.focus: true

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
                top: userEmailField.bottom
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
                var userEmail = userEmailField.field.text.trim()
                var userPassword = userPasswordField.field.text
                if (!userEmail || !userPassword) {
                    if (!userEmail) {
                        userEmailField.field.focus = false
                        userEmailField.field.valid = false
                    }
                    if (!userPassword) {
                        userPasswordField.field.focus = false
                        userPasswordField.field.valid = false
                    }

                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                client.change_user_email(userEmail, userPassword)
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