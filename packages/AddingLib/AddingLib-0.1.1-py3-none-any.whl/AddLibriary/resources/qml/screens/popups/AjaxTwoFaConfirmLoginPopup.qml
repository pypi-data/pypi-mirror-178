import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/desktop/popups.js" as Popups

AjaxPopup {
    id: popup

    width: 360
    height: background.height

    modal: true
    focus: true

    property var loginData: null

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    Rectangle {
        id: background

        width: 360
        height: closeItem.height + 24 + confirmLoginField.height + 3 + errorText.height + 8 + enterTotpText.height + 12 + forgotPassword.height + 24 + saveCancelArea.height
        color: ui.colors.dark3

        radius: 8

        Custom.PopupHeader {
            id: closeItem

            width: parent.width
            height: 64
            radius: parent.radius
            title: tr.desktop_2fa_confirm_login

            anchors.right: parent.right

            closeArea.onClicked: {
                popup.close()
            }
        }

        AjaxTextField {
            id: confirmLoginField

            width: popup.width - 64
            placeHolderText: "XXX XXX"
            focus: true

            maximumLength: 7

            anchors {
                top: closeItem.bottom
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }

            validator: RegExpValidator { regExp: /[0-9]{3} ?[0-9]{3}/ }
            inputMethodHints: Qt.ImhDigitsOnly

            onTextChanged: {
                util.confirm_login_dash_insert(confirmLoginField.text, cursorPosition)
            }

            Connections {
                target: util

                onDashInsertResult: {
                    confirmLoginField.text = new_text
                    confirmLoginField.cursorPosition = position
                }
            }

            Keys.onPressed: {
                if (event.key == Qt.Key_Enter || event.key == Qt.Key_Return) {
                    nextButton.clicked(true)
                    return
                }
            }

            onActiveFocusChanged: {
                if (errorText.text) {
                    errorText.text = ""
                }
            }
        }

        Text {
            id: errorText

            width: popup.width - 64
            height: contentHeight
            text: ""
            color: ui.colors.red1
            font.family: roboto.name
            font.pixelSize: 14
            wrapMode: Text.WordWrap

            anchors {
                top: confirmLoginField.bottom
                topMargin: 3
                horizontalCenter: parent.horizontalCenter
            }
        }

        Text {
            id: enterTotpText

            width: popup.width - 64
            height: contentHeight

            text: tr.desktop_2fa_enter_totp
            color: ui.colors.light1
            opacity: 0.5
            font.family: roboto.name
            font.pixelSize: 12
            wrapMode: Text.WordWrap
            verticalAlignment: Text.AlignVCenter

            anchors {
                top: errorText.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }
        }

        Text {
            id: forgotPassword

            width: parent.width - 64
            height: contentHeight

            text: tr.сant_receive_code_via_authentication_app
            color: ui.colors.green1
            font.family: roboto.name
            font.pixelSize: 12
            wrapMode: Text.Wrap
            verticalAlignment: Text.AlignVCenter

            anchors {
                top: enterTotpText.bottom
                topMargin: 12
                left: parent.left
                leftMargin: 32
//                horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                hoverEnabled: true

                onEntered: {
                    forgotPassword.opacity = 1
                }

                onExited: {
                    forgotPassword.opacity = 0.8
                }

                onClicked: {
                    application.toForgotPassword(loginData.email)
                    popup.close()
                }
            }
        }

        Item {
            id: saveCancelArea

            width: parent.width - 64
            height: 72

            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
            }

            Custom.Button {
                id: cancelButton

                width: 140
                height: 40
                color: ui.colors.light3
                transparent: true

                text: tr.cancel

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                onClicked:{
                    popup.close()
                }
            }

            Custom.Button {
                id: nextButton

                width: 140
                height: 40
                transparent: true

                text: tr.next

                anchors {
                    left: cancelButton.right
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }

                onClicked:{
                    if (!confirmLoginField.text.length) {
                        confirmLoginField.valid = false
                        return
                    }
                    else {
                        app.login_module.login(loginData.email, loginData.password, confirmLoginField.text.replace(" ", ""))
                    }
                    application.waitPopup()
                }
            }

        }
    }

    Connections {
        target: app.login_module

        onProLoginSuccess: {
            popup.close()
        }

        onLoginSuccess: {
            popup.close()
        }

        onLogoutSignal: {
            popup.close()
        }

        onConfirmTotpFailed: {
            errorText.text = tr.desktop_2fa_wrong_code
            confirmLoginField.valid = false
            confirmLoginField.focus = false
            confirmLoginField.text = ""
        }
    }
}