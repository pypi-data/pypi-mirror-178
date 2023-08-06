import QtQuick 2.12
import QtQuick.Controls 2.2


AjaxPopup {
    id: popup
    width: 360
    height: 223

    modal: true
    focus: true

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var data: null

    Rectangle {
        width: 360
        height: 223
        color: "#252525"

        border.width: 1
        border.color: "#1a1a1a"
        radius: 3

        AjaxPopupCloseHeader {
            id: closeItem
            label: tr.checking_code
        }

        AjaxSettingsTextField {
            id: smsCodeField
            miniText: tr.code_from_sms
            field.validator: RegExpValidator { regExp: /[0-9]{6}/ }
            width: popup.width - 64

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
            id: emailCodeField
            miniText: tr.code_from_email
            field.validator: RegExpValidator { regExp: /[0-9]{6}/ }
            width: popup.width - 64

            field.onActiveFocusChanged: {
                if (!valid) {
                    valid = true
                }
            }

            anchors {
                top: smsCodeField.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }
        }

        AjaxSaveCancel {
            anchors.bottom: parent.bottom

            cancelArea.onClicked: {
                popup.close()
            }

            saveArea.onClicked: {
                if (smsCodeField.field.length != 6 || emailCodeField.field.length != 6 ) {
                    if (smsCodeField.field.length != 6) {
                        smsCodeField.field.valid = false
                    }
                    if (emailCodeField.field.length != 6) {
                        emailCodeField.field.valid = false
                    }
                    return
                }

                client.user_confirm_edition(smsCodeField.field.text, emailCodeField.field.text)
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