import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/popups/user_settings"
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3" as DS3


AjaxPopup {
    id: popup
    property var settings: {"email": ""}
    objectName: "addEmployeePopup"
    width: 328
    height: columnItem.height + 88
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
        radius: 10

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
            id: columnItem
            width: parent.width - 56
            spacing: 8
            anchors {
                top: header.bottom
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
                Layout.minimumHeight: keyText.contentHeight + rolesScroll.height + 48
                Layout.maximumHeight: keyText.contentHeight + rolesScroll.height + 48
                Layout.fillWidth: true

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

                ScrollView {
                    clip: true
                    width: parent.width
                    anchors {
                        top: keyText.bottom
                        topMargin: 12
                        left: parent.left
                        bottom: parent.bottom
                    }

                    Roles {
                        id: rolesScroll
                        property var currentObject: null
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
                Layout.minimumHeight: 88
                Layout.maximumHeight: 88
                Layout.fillWidth: true

                Rectangle {
                    width: parent.width + 28
                    height: 1
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.Button {
                    width: parent.width
                    text: tr.add
                    color: ui.colors.green1
                    transparent: false
                    anchors.centerIn: parent
                    enabledCustom: emailField.valueText.control.text.length > 2
                                   && Array.from(rolesScroll.roles).length > 0

                    onClicked: {
                        settings["role"] = {"roles": Array.from(rolesScroll.roles)}
                        if (emailField.valueText.control.text == "") return
                        settings.email = emailField.valueText.control.text.trim()
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
