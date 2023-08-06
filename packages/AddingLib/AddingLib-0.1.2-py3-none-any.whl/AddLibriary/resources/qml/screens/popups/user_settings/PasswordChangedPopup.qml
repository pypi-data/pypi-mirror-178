import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtQml.Models 2.14

import "qrc:/resources/qml/components/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "passwordChangePopup"
    width: 328
    height: 488
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    modal: true
    focus: true
    anchors.centerIn: parent

    property var tokenLength: 6
    property var duration: 200
    property var email: ""

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    PropertyAnimation {
        id: widthAnim
        target: popup
        duration: popup.duration
        property: "width"
    }

    PropertyAnimation {
        id: heightAnim
        target: popup
        duration: popup.duration
        property: "height"
    }

    contentItem: Rectangle {
        id: body
        clip: true
        color: ui.colors.dark3
        radius: 10
        anchors.fill: parent

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 80
            radius: parent.radius
            title: tr.change_password
            anchors{
                top: parent.top
            }

            closeArea.onClicked: {
                popup.close()
            }
        }
        
        Item {
            id: infoText

            width: parent.width - 64
            height: visible ? 40 : 0
            visible: false

            anchors {
                top: header.bottom
                horizontalCenter: parent.horizontalCenter
            }

            Custom.FontText {
                text: tr.a911_password_requirements
                width: 240
                color: ui.colors.middle4
                anchors.centerIn: parent
                wrapMode: Text.WordWrap
            }
        }

        Item {
            id: oldPasswordItem

            width: parent.width - 64
            height: 96

            anchors {
                top: infoText.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }

            Custom.TextFieldEdit {
                id: oldPassword

                distance: 20
                width: parent.width
    
                valueText.control.font.pixelSize: 16
                valueText.control.color: ui.colors.light3
                valueText.control.echoMode: TextInput.Password
                key: tr.old_password
                value: ""

                anchors {
                    top: parent.top
                }

                Keys.onReturnPressed: {
                    if (editPasswordButton.enabledCustom) {
                        editPasswordButton.forceActiveFocus()
                        editPasswordButton.clicked()
                    }
                }

                Keys.onEnterPressed: {
                    if (editPasswordButton.enabledCustom) {
                        editPasswordButton.forceActiveFocus()
                        editPasswordButton.clicked()
                    }
                }
            }
        }

        Item {
            id: newPasswordItem

            width: parent.width - 64
            height: 96

            anchors {
                top: oldPasswordItem.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }

            Custom.TextFieldEdit {
                id: newPassword

                distance: 20
                width: parent.width
                valueText.control.font.pixelSize: 16
                valueText.control.color: ui.colors.light3
                valueText.control.echoMode: TextInput.Password
                key: tr.new_password
                value: ""

                anchors {
                    top: parent.top
                }

                Keys.onReturnPressed: {
                    if (editPasswordButton.enabledCustom) {
                        editPasswordButton.forceActiveFocus()
                        editPasswordButton.clicked()
                    }
                }

                Keys.onEnterPressed: {
                    if (editPasswordButton.enabledCustom) {
                        editPasswordButton.forceActiveFocus()
                        editPasswordButton.clicked()
                    }
                }

                valueText.control.onFocusChanged: {
                    if (focus) {
                        newPassword.valueText.valid = true
                        repeatPassword.valueText.valid = true
                    }
                }
            }
        }

        Item {
            id: repeatPasswordItem

            width: parent.width - 64
            height: 96

            anchors {
                top: newPasswordItem.bottom
                topMargin: 8
                horizontalCenter: parent.horizontalCenter
            }

            Custom.TextFieldEdit {
                id: repeatPassword
                distance: 20
                width: parent.width
                valueText.control.font.pixelSize: 16
                valueText.control.color: ui.colors.light3
                valueText.control.echoMode: TextInput.Password
                key: tr.a911_confirm_password
                value: ""

                anchors {
                    top: parent.top
                }

                Keys.onReturnPressed: {
                    if (editPasswordButton.enabledCustom) {
                        editPasswordButton.forceActiveFocus()
                        editPasswordButton.clicked()
                    }
                }

                Keys.onEnterPressed: {
                    if (editPasswordButton.enabledCustom) {
                        editPasswordButton.forceActiveFocus()
                        editPasswordButton.clicked()
                    }
                }

                valueText.control.onFocusChanged: {
                    if (focus) {
                        newPassword.valueText.valid = true
                        repeatPassword.valueText.valid = true
                    }
                }
            }
        }

        Item {
            width: parent.width
            height: 88

            anchors {
                bottom: parent.bottom
            }

            Rectangle {
                width: parent.width - 32
                height: 1
                color: ui.colors.dark1

                anchors {
                    top: parent.top
                    right: parent.right
                }
            }

            Custom.Button {
                id: editPasswordButton
                width: parent.width - 64
                text: tr.continue_android

                transparent: false
                color: ui.colors.green1
                enabledCustom: oldPassword.valueText.control.text.trim() && newPassword.valueText.control.text.trim() && repeatPassword.valueText.control.text.trim()

                anchors.centerIn: parent

                onClicked: {
                    var settings = {}
                    if (newPassword.valueText.control.text != repeatPassword.valueText.control.text) {
                        newPassword.valueText.valid = false
                        repeatPassword.valueText.valid = false
                        repeatPassword.valueText.error = tr.passwords_doesnt_match
                        return
                    }
                    settings["old_password"] = oldPassword.valueText.control.text
                    settings["phone_number"] = appUser.data.user_info.phone
                    settings["new_password"] = newPassword.valueText.control.text
                    settings["repeat_password"] = repeatPassword.valueText.control.text

                    popup.enabled = false
                    loading = true

                    app.restore_pass_module.update_user_password(settings)
                }
            }
        }

        Connections {
            target: app.restore_pass_module

            onUpdateUserPasswordValidationError: {
                // TODO change localize texts, mayve add popup in the future

                editPasswordButton.loading = false
                popup.enabled = true

                if (newPassword.valueText.control.text === repeatPassword.valueText.control.text) {
                    newPassword.valueText.valid = true
                    repeatPassword.valueText.valid = true
                }

                if (result["1"]) {
                    oldPassword.valueText.valid = false
                    oldPassword.valueText.error = result["1"].message
                }

                if (result === "systems.ajax.a911.constraints.InvalidPasswordWhileUpdateSecuredField") {
                    oldPassword.valueText.valid = false
                }
            }
        }

        Connections {
            target: app

            onActionSuccess: {
                editPasswordButton.loading = false
                popup.enabled = true

                confirmEditedUserSettingsPopup(tr.a911_successfuly_changed_password, tr.change_password)
                popup.close()
            }
        }
    }
}
