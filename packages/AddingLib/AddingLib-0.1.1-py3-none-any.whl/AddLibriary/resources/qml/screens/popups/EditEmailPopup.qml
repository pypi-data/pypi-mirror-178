import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    width: 328
    height: 400

    modal: true
    focus: true

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        id: body
        clip: true
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 98
            radius: parent.radius
            title: tr.change_email_button + "?"
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        Rectangle {
            width: parent.width
            height: 1
            color: ui.colors.dark4
            anchors.top: header.bottom
        }

        Item {
            id: passwordItem
            width: parent.width - 64
            height: 80
            anchors {
                top: header.bottom
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            Custom.TextFieldEdit {
                id: password
                distance: 20
                width: parent.width
                key: tr.password
                value: ""
                valueText.control.font.pixelSize: 16
                valueText.control.color: ui.colors.light3
                valueText.control.echoMode: TextInput.Password
                anchors {
                    top: parent.top
                }

                Keys.onReturnPressed: {
                    if (editEmail.enabledCustom) {
                        editEmail.forceActiveFocus()
                        editEmail.clicked()
                    }
                }

                Keys.onEnterPressed: {
                    if (editEmail.enabledCustom) {
                        editEmail.forceActiveFocus()
                        editEmail.clicked()
                    }
                }
            }
        }

        Item {
            id: newPhoneNumberItem
            width: parent.width - 64
            height: 80
            anchors {
                top: passwordItem.bottom
                topMargin: 24
                horizontalCenter: parent.horizontalCenter
            }

            Custom.TextFieldEdit {
                id: newEmail
                distance: 20
                width: parent.width
                key: tr.new_email_address
                value: ""
                valueText.control.font.pixelSize: 16
                valueText.control.color: ui.colors.light3
                valueText.control.maximumLength: 100
                anchors {
                    top: parent.top
                }
                Keys.onReturnPressed: {
                    if (editEmail.enabledCustom) {
                        editEmail.forceActiveFocus()
                        editEmail.clicked()
                    }
                }

                Keys.onEnterPressed: {
                    if (editEmail.enabledCustom) {
                        editEmail.forceActiveFocus()
                        editEmail.clicked()
                    }
                }
            }
        }

        Rectangle {
            width: parent.width - 32
            height: 1
            color: ui.colors.dark1
            anchors {
                bottom: parent.bottom
                bottomMargin: 72
                right: parent.right
            }
        }

        Item {
            width: parent.width - 64
            height: 40
            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: parent.bottom
                bottomMargin: 16
            }

            Custom.Button {
                id: editEmail
                text: tr.continue_android
                width: parent.width
                color: ui.colors.green1
                enabledCustom: password.valueText.control.text && newEmail.valueText.control.text
                anchors.centerIn: parent

                onClicked: {
                    var settings = {}
                    settings["password"] = password.valueText.control.text
                    settings["new_email"] = newEmail.valueText.control.text.trim()

                    popup.enabled = false
                    loading = true

                    app.restore_pass_module.update_email(settings)
                }
            }
        }

        Connections {
            target: app.restore_pass_module

            onUpdateUserEmailValidationError: {
                editEmail.loading = false
                popup.enabled = true

                if (result["1"]) {
                    password.valueText.valid = false
                    password.valueText.error = result["1"].message
                }

                if (result["3"]) {
                    newEmail.valueText.valid = false
                    newEmail.valueText.error = result["3"].message
                }
            }
        }

        Connections {
            target: app

            onActionSuccess: {
                editEmail.loading = false
                popup.enabled = true

                confirmEditedUserSettingsPopup(tr.your_email_has_been_changed, tr.verification_code)
                popup.close()
            }
        }
    }
}
