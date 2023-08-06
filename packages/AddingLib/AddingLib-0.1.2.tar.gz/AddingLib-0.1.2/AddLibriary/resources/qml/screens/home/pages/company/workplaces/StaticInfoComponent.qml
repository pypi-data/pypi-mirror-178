import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups


Item {
    anchors.fill: parent

    ScrollView {
        id: scrollView
            clip: true
            width: parent.width - 20
            anchors {
                top: parent.top
                right: parent.right
                bottom: buttonsBlock.top
            }

            ScrollBar.vertical: Custom.ScrollBar {
                parent: scrollView
                anchors {
                    top: parent.top
                    right: parent.right
                    bottom: parent.bottom
                }

                policy: {
                    if (scrollView.contentHeight > scrollView.height) {
                        return ScrollBar.AlwaysOn
                    }
                    return ScrollBar.AlwaysOff
                }
            }

        ColumnLayout {
            spacing: 10
            width: parent.width
            anchors {
                top: parent.top
                right: parent.right
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 112
                Layout.maximumHeight: 112

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.UserImage {
                    id: userImage
                    width: 80
                    height: 80
                    fontSize: 28
                    imageSource: currentObject && currentObject[0] ? (Object.keys(currentObject[0].photos).length !== 0 ? currentObject[0].photos["128x128"] : "") : ui.empty
                    userName: currentObject && currentObject[0] ? currentObject[0].data.first_name + " " + currentObject[0].data.last_name : ui.empty
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }
                }

                Item {
                    width: 150
                    height: 48
                    anchors {
                        top: parent.top
                        topMargin: 12
                        right: parent.right
                        rightMargin: 16
                    }

                    visible: {
                        if (!currentObject || !currentObject[1]) return false
                        return currentObject[1].verificationStatus == "VERIFIED"
                    }

                    Custom.Button {
                        width: parent.width
                        text: tr.edit
                        transparent: true
                        color: ui.colors.green1
                        anchors.centerIn: parent

                        onClicked: {
                            application.debug("company -> company info -> workplaces -> edit workplace")
                            editMode = true
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.a911_employee_name
                    value: currentObject && currentObject[0] && currentObject[0].data ? currentObject[0].data.first_name + " " + currentObject[0].data.last_name : ui.empty
                    valueText.font.pixelSize: 18
                    valueText.rightPadding: 15
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 1
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.a911_login
                    value: currentObject && currentObject[0] && currentObject[0].data && currentObject[0].data.email ? currentObject[0].data.email : ui.empty
                    valueText.font.pixelSize: 16
                    valueText.rightPadding: 15
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 1
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.machine_id
                    value: currentObject && currentObject[1] && currentObject[1].machine_id ? currentObject[1].machine_id : ui.empty
                    valueText.font.pixelSize: 16
                    valueText.rightPadding: 15
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 1
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Rectangle {
                    height: 1
                    width: parent.width
                    anchors.bottom: parent.bottom
                    color: ui.colors.white
                    opacity: 0.1
                }

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.workplaces_911_popup
                    value: currentObject && currentObject[1] && currentObject[1].name ? currentObject[1].name : ui.empty
                    valueText.font.pixelSize: 16
                    valueText.rightPadding: 15
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 1
                }
            }

            Rectangle {
                color: "transparent"
                Layout.fillWidth: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80

                Custom.TextFieldStatic {
                    width: parent.width
                    key: tr.a911_status
                    valueText.font.pixelSize: 16
                    valueText.rightPadding: 15
                    valueText.leftPadding: definedStatus ? 16 : 0
                    distance: 12
                    anchors {
                        top: parent.top
                        topMargin: 12
                        left: parent.left
                    }
                    valueText.textFormat: Text.PlainText
                    valueText.elide: Text.ElideRight
                    valueText.maximumLineCount: 1

                    value: {
                        if (!currentObject || !currentObject[1]) return ui.empty
                        if (currentObject[1].connection_status == "ONLINE") return tr.online
                        if (currentObject[1].connection_status == "OFFLINE") return tr.offline
                        if (currentObject[1].connection_status == "LOGGED_OUT") return tr.logged_out_workplaces
                        return ui.empty
                    }

                    property var definedStatus: {
                        if (!currentObject || !currentObject[1]) return false
                        if (currentObject[1].connection_status == "ONLINE") return true
                        if (currentObject[1].connection_status == "OFFLINE") return true
                        if (currentObject[1].connection_status == "LOGGED_OUT") return true
                        return false
                    }

                    Rectangle {
                        width: 8
                        height: 8
                        radius: height / 2
                        anchors {
                            left: parent.left
                            verticalCenter: parent.valueText.verticalCenter
                        }

                        color: {
                            if (!currentObject || !currentObject[1]) return "transparent"
                            if (currentObject[1].connection_status == "ONLINE") return ui.colors.green1
                            if (currentObject[1].connection_status == "OFFLINE") return ui.colors.red1
                            if (currentObject[1].connection_status == "LOGGED_OUT") return ui.colors.light3
                            return "transparent"
                        }
                    }
                }
            }
        }
    }

    Item {
        id: buttonsBlock
        width: parent.width
        height: 72
        anchors.bottom: parent.bottom
        visible: true

        Item {
            visible: confirmWorkplaceButton.visible && !currentObject[1].machine_id
            anchors.fill: confirmWorkplaceButton

            Custom.HandMouseArea {
                onClicked: {
                    Popups.text_popup(tr.information, tr.without_machine_id)
                }
            }
        }

        Custom.Button {
            id: confirmWorkplaceButton
            width: parent.width - 32
            text: tr.add_workplace
            color: ui.colors.green1
            transparent: true
            anchors.centerIn: parent

            enabledCustom: currentObject && currentObject[1] && currentObject[1].machine_id

            visible: {
                if (!currentObject || !currentObject[1]) return false
                return currentObject[1].verificationStatus == "UNVERIFIED"
            }

            onClicked: {
                application.debug("company -> company info -> workplaces -> confirm workplace")

                Popups.create_workplace_popup(currentObject[1])
            }
        }

        Custom.Button {
            id: rejectWorkplaceButton
            width: parent.width - 32
            text: tr.cancel_aproved_workplace
            color: ui.colors.dark4
            textButton.color: ui.colors.white
            transparent: false
            anchors.centerIn: parent

            visible: {
                if (!currentObject || !currentObject[1]) return false
                return currentObject[1].verificationStatus == "VERIFIED"
            }

            onClicked: {
                application.debug("company -> company info -> workplaces -> reject workplace")

                var settings = {}
                settings["id"] = currentObject[1].id
                settings["verificationStatus"] = "UNVERIFIED"

                app.workplaces_module.set_workplace_verification_status(settings)
            }
        }
    }
}
