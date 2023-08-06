import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"


AjaxPopup {
    id: popup
    width: 528
    height: 320
    closePolicy: Popup.CloseOnEscape
    modal: true
    focus: true
    anchors.centerIn: parent
    property alias text: warningMessage.text
    property var remove: ""

    background: Rectangle {
        color: ui.colors.black
        opacity: 0.6
        width: application.width
        height: application.height
        x: 0 - parent.x
        y: 0 - parent.y
    }
    contentItem:  Rectangle {
        id: body
        clip: true
        color:  ui.colors.dark3
        radius: 8
        anchors.fill: parent

        Item {
            height: logoImage.height + warningMessage.height + 16
            width: parent.width - 152
            anchors {
                top: parent.top
                right: parent.right
                topMargin: 88
                rightMargin: 86
            }

            Image {
                id: logoImage
                sourceSize.width: 67
                sourceSize.height: 28
                source: "qrc:/resources/images/desktop/logo/logo-pants-white.svg"
                anchors.horizontalCenter: parent.horizontalCenter
            }

            Custom.FontText {
                id: warningMessage
                text: tr.delete
                width: parent.width
                color: ui.colors.light3
                font.pixelSize: 16
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                anchors {
                    top: logoImage.bottom
                    topMargin: 16
                }
            }
        }
        Rectangle {
            width: parent.width - 32
            height: 1
            color: ui.colors.dark1
            anchors {
                bottom: body.bottom
                bottomMargin: 80
                rightMargin: 16
                right: body.right
            }
        }

        Rectangle {
            width: parent.width - 64
            height: 40
            color: "transparent"
            anchors {
                bottom: parent.bottom
                bottomMargin: 23
                horizontalCenter: parent.horizontalCenter
            }

            Custom.Button {
                id: cancel
                width: 224
                transparent: true
                text: tr.cancel
                color: ui.colors.light4
                onClicked: {
                    popup.close()
                }
            }

            Custom.Button {
                width: 224
                anchors {
                    left: cancel.right
                    leftMargin: 24
                }
                transparent: true
                text: remove === "SCHEDULE" ? tr.to_trash_911 : tr.delete
                color: ui.colors.red1

                onClicked: {
                    if (remove === "BINDING") {
                        app.company_module.delete_hub_company_binding(currentObject)
                        connectionsList.connectionsData.ownCurrentIndex = -1
                    }
                    else if (remove === "SCHEDULE")
                        app.company_module.schedule_channel_911_removal(currentObject)
                    else if (remove === "REMOVE") {
                        app.company_module.remove_channel_911(currentObject)
                        connectionsList.connectionsData.ownCurrentIndex = -1
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

        onActionFailed: {
            popup.close()
        }
    }
}