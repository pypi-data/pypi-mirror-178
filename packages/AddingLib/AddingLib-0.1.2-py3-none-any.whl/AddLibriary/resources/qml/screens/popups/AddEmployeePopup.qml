import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    objectName: "addEmployeePopup"
    width: 328
    height: 400
    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true

    anchors.centerIn: parent

    onOpened: {
        emailField.valueText.control.forceActiveFocus()
    }

    background: Rectangle {
        color: "black"
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }

    contentItem: Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
        radius: 8

        Custom.PopupHeader {
            id: header
            width: parent.width
            height: 88
            radius: parent.radius
            title: tr.a911_add_empoyee
            anchors.top: parent.top

            closeArea.onClicked: {
                popup.close()
            }
        }

        ColumnLayout {
            width: parent.width - 56
            spacing: 8
            anchors {
                top: header.bottom
                topMargin: 24
                bottom: parent.bottom
                bottomMargin: 24
                horizontalCenter: parent.horizontalCenter
            }

            Rectangle {
                color: "transparent"
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80
                Layout.fillWidth: true

                Custom.TextFieldEdit {
                    id: emailField
                    width: parent.width
                    key: tr.a911_emploee_mail
                    value: ""
                    distance: 16
                    valueText.control.maximumLength: 100
                    valueText.color: ui.colors.dark1
                    anchors.centerIn: parent
                }
                Connections {
                    target: app.employee_module
                    onAddEmployeeValidationError: {
                        if (errors["2"]) {
                            emailField.valueText.valid = false
                            emailField.valueText.error = errors["2"].message
                        }
                    }
                }
            }

            Rectangle {
                id: roleRect
                color: "transparent"
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80
                Layout.fillWidth: true
                property var positionDelimiterError: borderCombobox.visible
                Custom.FontText {
                    id: keyText
                    text: tr.a911_role
                    width: parent.width
                    color: ui.colors.white
                    opacity: 0.5
                    font.pixelSize: 14
                    font.weight: Font.Light
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignLeft
                    anchors {
                        top: parent.top
                        topMargin: 8
                        left: parent.left
                    }
                }

                Custom.ComboBox {
                    id: roleField
                    property var userModel: uiRoles
                    property var serverModel: accessibleRoles
                    width: parent.width
                    model: userModel
                    currentIndex: -1
                    backgroundRectangle.color: ui.colors.dark1
                    anchors {
                        top: keyText.bottom
                        topMargin: 12
                        left: parent.left
                    }
                    Rectangle {
                        id: borderCombobox
                        anchors.fill: parent
                        visible: false
                        border {
                            color: ui.colors.red3
                            width: 1
                        }
                        color: "transparent"
                    }
                    popup.onOpened: {
                        borderCombobox.visible = false
                    }
                }
                Connections {
                    target: app.employee_module
                    onAddEmployeeValidationError: {
                        if (errors["1"]) {
                            errorText.text = errors["1"].message
                            borderCombobox.visible = true
                        }
                    }
                }
                Connections {
                    target: roleField
                    onFocusChanged: {
                        borderCombobox.visible = false
                    }
                }
                Custom.FontText {
                    id: errorText
                    width: parent.width
                    visible: borderCombobox.visible
                    color: ui.colors.red1
                    wrapMode: Text.WordWrap
                    font.pixelSize: 12
                    anchors {
                        top: roleField.bottom
                        left: parent.left
                    }
                }
                Rectangle {
                    width: parent.width
                    height: 1
                    color: ui.colors.white
                    opacity: 0.1
                    anchors {
                        top: roleRect.positionDelimiterError ? errorText.bottom : parent.bottom
                        topMargin: 8
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.fillHeight: true


            }

            Rectangle {
                color: "transparent"
                Layout.minimumHeight: 56
                Layout.maximumHeight: 56
                Layout.fillWidth: true

                Custom.Button {
                    width: parent.width
                    text: tr.continue_android
                    color: ui.colors.green1
                    transparent: false
                    anchors.centerIn: parent
                    enabledCustom: emailField.valueText.control.text.length > 3 && roleField.currentIndex != -1

                    onClicked: {
                        if (emailField.valueText.control.text == "" || roleField.currentIndex == -1) return

                        var settings = {}
                        settings["email"] = emailField.valueText.control.text.trim()
                        settings["role"] = roleField.serverModel[roleField.currentIndex]

                        app.employee_module.invite_employee(settings)
                    }
                }
            }
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }
    }
}
