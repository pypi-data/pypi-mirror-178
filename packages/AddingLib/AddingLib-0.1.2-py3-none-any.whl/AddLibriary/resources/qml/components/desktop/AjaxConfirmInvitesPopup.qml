import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"

AjaxPopup {
    id: popup
    width: 320
    height: 36 + rect.height + 12 + 48

    property string text: ""
    property bool pro: false
    property string emails: ""
    property var management: null

    Rectangle {
        width: 320
        height: 130
        anchors.fill: parent
        color: "#393939"
        radius: 4
        border.width: 0.1
        border.color: "#1a1a1a"
        opacity: 0.999
        focus: true

        Column {
            anchors.fill: parent

            Item {
                width: parent.width
                height: 36
                Text {
                    text: tr.information
                    color: ui.colors.light1
                    font.family: roboto.name
                    font.pixelSize: 14
                    anchors.centerIn: parent
                }
            }

            Item {
                id: rect
                width: parent.width
                height: textLabel.contentHeight
                Text {
                    id: textLabel
                    width: parent.width - 10
                    wrapMode: Text.WordWrap
                    horizontalAlignment: Text.AlignHCenter
                    text: popup.text
                    color: ui.colors.light1
                    opacity: 0.7
                    font.family: roboto.name
                    font.pixelSize: 12
                    anchors.centerIn: parent
                }
            }
        }

        AjaxSaveCancel {
            anchors.bottom: parent.bottom
            saveText: tr.send

            cancelArea.onClicked: {
                popup.close()
            }

            saveArea.onClicked: {
                app.hub_management_module.invite_users(management.devices.hub, emails, pro)
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