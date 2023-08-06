import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13
import QtQml.Models 2.14

import "qrc:/resources/qml/components/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


AjaxPopup {
    id: popup
    width: 328
    height: 352
    closePolicy: Popup.CloseOnEscape

    modal: true
    focus: true
    anchors.centerIn: parent

    property var title;
    property var additionalTitle: ""

    background: Rectangle {
        color: ui.colors.black
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
            height: 32
            radius: parent.radius
            title: popup.additionalTitle ? popup.additionalTitle : tr.a911_restore_password
            anchors {
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
                        valueText.control.validator: RegExpValidator { regExp : /[0-9]{6}/ }
                        Keys.onReturnPressed: {
                            if (next.enabledCustom) {
                                next.forceActiveFocus()
                                next.clicked()
                            }
                        }

                        Keys.onEnterPressed: {
                            if (next.enabledCustom) {
                                next.forceActiveFocus()
                                next.clicked()
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
                        valueText.control.validator: RegExpValidator { regExp : /[0-9]{6}/ }
                        Keys.onReturnPressed: {
                            if (next.enabledCustom) {
                                next.forceActiveFocus()
                                next.clicked()
                            }
                        }
        
                        Keys.onEnterPressed: {
                            if (next.enabledCustom) {
                                next.forceActiveFocus()
                                next.clicked()
                            }
                        }
                    }
                }
            }
        }
    }
    Item {
        width: 264
        height: 48
        anchors {
            bottom: {
                return parent.bottom
            }
            bottomMargin: 24
            horizontalCenter: parent.horizontalCenter
        }

        Custom.Button {
            id: next
            text: tr.next
            width: parent.width
            anchors.centerIn: parent
            enabledCustom: (smsInput.valueText.control.text.length === 6 &&
             emailInput.valueText.control.text.length === 6)

            onClicked: {
                app.restore_pass_module.confirm_secured_field_update(smsInput.valueText.control.text, emailInput.valueText.control.text)
            }
        }
    }
    Connections {
        target: app
        onActionSuccess: {
            app.get_current_user()
            notificationPopup(popup.title)
            popup.close()
        }
    }
    Connections {
        target: app.restore_pass_module
        onActionFailedConfirSecuredFieldUpdate: {
            emailInput.valueText.valid = false
            smsInput.valueText.valid = false
        }
    }
}
