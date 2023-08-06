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
    height: 280
    closePolicy: Popup.CloseOnEscape

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
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 32
            radius: parent.radius
            title: tr.a911_restore_password
            anchors{
                top: parent.top
                topMargin: 32
            }

            closeArea.onClicked: {
                popup.close()
            }
        }

        Item {
            id: pages
            width: parent.width
            anchors {
                top: header.bottom
                topMargin: 32
                leftMargin: 32
                bottom: parent.bottom
            }

            Connections {
                target: app.restore_pass_module

                onForgotPasswordStepSuccess: {
                    if (step == 0) {
                        popup.tokenLength = info.length
                        listView.currentIndex = 1
                        widthAnim.to = 328
                        heightAnim.to = 568
                        widthAnim.start()
                        heightAnim.start()
                        return
                    }

                    if (step == 1) {
                        listView.currentIndex = 2
                        widthAnim.to = 328
                        heightAnim.to = 240
                        widthAnim.start()
                        heightAnim.start()
                        header.title = ""
                        return
                    }

                    if (step == 2) {
                        listView.currentIndex = 0
                        widthAnim.to = 552
                        heightAnim.to = 280
                        widthAnim.start()
                        heightAnim.start()
                        return
                    }
                }
            }

            ListView {
                width: parent.width
                height: parent.height
                id: listView
                model: objectsModel
                interactive: false
                currentIndex: 0
                anchors.fill: parent

                orientation: Qt.Horizontal
                snapMode: ListView.SnapOneItem
                highlightMoveDuration: popup.duration
                highlightMoveVelocity: -1
                highlightRangeMode: ListView.StrictlyEnforceRange
            }

            ObjectModel {
                id: objectsModel

                Item {
                    width: pages.width
                    height: pages.height

                    Item {
                        width: parent.width - 64
                        height: fieldInput.height
                        anchors {
                            top: parent.top
                            horizontalCenter: parent.horizontalCenter
                        }

                        Custom.TextFieldEdit {
                            id: fieldInput
                            width: parent.width
                            distance: 20
                            key: tr.phone_number_or_email
                            value: popup.email
                            valueText.control.maximumLength: 100

                            Connections {
                                target: app.restore_pass_module

                                onForgotPasswordErrors: {
                                    if (result["1"]) {
                                        fieldInput.valueText.valid = false
                                        fieldInput.valueText.error = result["1"].message
                                    }
                                    if (result["error"]) {
                                        fieldInput.valueText.valid = false
                                        fieldInput.valueText.error = result["error"].message
                                    }
                                }
                            }
                        }
                    }

                    Item {
                        width: 264
                        height: 48
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 32
                            horizontalCenter: parent.horizontalCenter
                        }

                        Custom.Button {
                            id: next
                            text: tr.next
                            width: parent.width
                            anchors.centerIn: parent
                            enabledCustom: fieldInput.valueText.control.text != ""

                            onClicked: {
                                next.forceActiveFocus()
                                popup.email = fieldInput.valueText.control.text.trim()
                                app.restore_pass_module.restore_password(popup.email)
                            }
                        }
                    }
                }

                Item {
                    width: pages.width
                    height: pages.height

                    Item {
                        id: smsField
                        width: parent.width - 64
                        height: 80
                        anchors {
                            horizontalCenter: parent.horizontalCenter
                        }

                        Custom.TextFieldEdit {
                            id: smsInput
                            width: parent.width
                            distance: 20
                            key: tr.code_from_sms
                            value: ""

                            Connections {
                                target: app.restore_pass_module

                                onForgotPasswordErrors: {
                                    if (result["2"]) {
                                        smsInput.valueText.valid = false
                                    }
                                    if (result["error"]) {
                                        smsInput.valueText.valid = false
                                    }
                                }
                            }
                        }
                    }

                    Item {
                        id: emailField
                        width: parent.width - 64
                        height: 80
                        anchors {
                            top: smsField.bottom
                            left: parent.left
                            leftMargin: 32
                            topMargin: 8
                        }

                        Custom.TextFieldEdit {
                            id: emailInput
                            width: parent.width
                            distance: 20
                            key: tr.code_from_email
                            value: ""

                            Connections {
                                target: app.restore_pass_module

                                onForgotPasswordErrors: {
                                    if (result["3"]) {
                                        emailInput.valueText.valid = false
                                    }
                                    if (result["error"]) {
                                        emailInput.valueText.valid = false
                                        emailInput.valueText.error = result["error"].message
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        id: line
                        width: parent.width - 32
                        height: 1
                        color: ui.colors.white
                        opacity: 0.1
                        anchors {
                            top: emailField.bottom
                            right: parent.right
                            topMargin: 16
                        }
                    }

                    Item {
                        id: passwordField
                        width: parent.width - 64
                        height: 80
                        anchors {
                            top: line.bottom
                            left: parent.left
                            leftMargin: 32
                            topMargin: 24
                        }

                        Custom.TextFieldEdit {
                            id: passwordInput
                            width: parent.width
                            distance: 20
                            key: tr.new_password
                            value: ""
                            valueText.control.echoMode: TextInput.Password
                        }
                    }

                    Item {
                        id: passwordField2
                        width: parent.width - 64
                        height: 80
                        anchors {
                            top: passwordField.bottom
                            left: parent.left
                            leftMargin: 32
                            topMargin: 8
                        }

                        Custom.TextFieldEdit {
                            id: passwordInput2
                            width: parent.width
                            distance: 20
                            key: tr.repeat_new_password
                            value: ""
                            valueText.control.echoMode: TextInput.Password
                        }
                    }

                    Item {
                        width: 264
                        height: 48
                        anchors {
                            bottom: parent.bottom
                            bottomMargin: 32
                            horizontalCenter: parent.horizontalCenter
                        }

                        Custom.Button {
                            id: next2
                            text: tr.save
                            width: parent.width
                            anchors.centerIn: parent

                            enabledCustom: {
                                smsInput.valueText.control.text.length == popup.tokenLength
                                && emailInput.valueText.control.text.length == popup.tokenLength
                                && passwordInput.valueText.control.text == passwordInput2.valueText.control.text
                                && passwordInput.valueText.control.text.trim()
                            }

                            onClicked: {
                                next2.forceActiveFocus()
                                app.restore_pass_module.restore_password_confirm(popup.email, smsInput.valueText.control.text,
                                emailInput.valueText.control.text, passwordInput.valueText.control.text)
                            }
                        }
                    }
                }

                Item {
                    width: pages.width
                    height: pages.height

                    Rectangle {
                        width: parent.width
                        height: parent.height
                        color: "transparent"

                        Image {
                            id: logo
                            source: "qrc:/resources/images/icons/logo-pants-white.svg"
                            anchors {
                                horizontalCenter: parent.horizontalCenter
                                top: parent.top
                            }
                        }

                        Text {
                            text: tr.a911_successfuly_changed_password
                            color: ui.colors.white
                            font.pixelSize: 16
                            anchors {
                                horizontalCenter: parent.horizontalCenter
                                top:logo.bottom
                                topMargin: 16
                            }
                        }
                    }
                }
            }
        }
    }
}
