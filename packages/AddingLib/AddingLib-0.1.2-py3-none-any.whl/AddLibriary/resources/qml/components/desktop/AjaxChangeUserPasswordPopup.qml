import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/js/popups.js" as Popups

AjaxPopup {
    id: popup
    width: 360
    height: 268

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    Rectangle {
        width: 360
        height: 268
        color: "#252525"

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.change_password
        }

        AjaxSettingsTextField {
            id: oldPasswordField
            miniText: tr.old_password
            width: popup.width - 64
            password: true

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
            id: newPasswordField
            miniText: tr.new_password
            password: true
            width: popup.width - 64

            field.onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            Keys.onEnterPressed: {
                saveCancel.saveArea.clicked(true)
            }

            Keys.onReturnPressed: {
                saveCancel.saveArea.clicked(true)
            }

            anchors {
                top: oldPasswordField.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }
        }

        AjaxSettingsTextField {
            id: reNewPasswordField
            miniText: tr.repeat_new_password
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
                top: newPasswordField.bottom
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
                var oldPassword = oldPasswordField.field.text
                var newPassword = newPasswordField.field.text
                var reNewPassword = reNewPasswordField.field.text
                if (!oldPassword || !newPassword || !reNewPassword) {
                    if (!oldPassword) {
                        oldPasswordField.field.focus = false
                        oldPasswordField.field.valid = false
                    }
                    if (!newPassword) {
                        newPasswordField.field.focus = false
                        newPasswordField.field.valid = false
                    }
                    if (!reNewPassword) {
                        reNewPasswordField.field.focus = false
                        reNewPasswordField.field.valid = false
                    }

                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                if (newPassword != reNewPassword) {
                    newPasswordField.field.focus = false
                    newPasswordField.field.valid = false
                    reNewPasswordField.field.focus = false
                    reNewPasswordField.field.valid = false

                    Popups.text_popup(tr.error, tr.passwords_doesnt_match)
                    return
                }

                client.change_user_password(oldPassword, newPassword)
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