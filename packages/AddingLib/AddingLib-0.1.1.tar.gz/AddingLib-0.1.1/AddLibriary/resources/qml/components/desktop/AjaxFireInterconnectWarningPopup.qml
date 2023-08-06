import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"

AjaxPopup {
    id: popup
    objectName: "textPopup"
    width: 320
    height: 36 + rect.height + 12 + 48

    parent: ApplicationWindow.contentItem

    property string title: tr.warning
    property string text: tr.too_long_frame

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

        Keys.onPressed: {
            popup.close()
        }

        Column {
            anchors.fill: parent

            Item {
                width: parent.width
                height: 36
                Text {
                    text: title
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

        Rectangle {
            width: parent.width
            height: 48
            anchors.bottom: parent.bottom
            color: "transparent"

            Rectangle {
                height: 1
                width: parent.width
                opacity: 0.1
                color: ui.colors.light1
                anchors.top: parent.top
            }

            MouseArea {
                width: parent.width / 2
                height: 48
                anchors.left: parent.left
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                Rectangle {
                    height: parent.height
                    width: 1
                    opacity: 0.1
                    color: ui.colors.light1
                    anchors.right: parent.right
                }

                Text {
                    anchors.centerIn: parent
                    font.family: roboto.name
                    font.pixelSize: 12
                    color: ui.colors.light1
                    text: tr.cancel
                }

                onClicked: {
                    popup.close()
                }
            }

            MouseArea {
                width: parent.width / 2
                height: 48
                anchors.right: parent.right
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                Text {
                    anchors.centerIn: parent
                    font.family: roboto.name
                    font.pixelSize: 12
                    color: ui.colors.green1
                    text: tr.ok
                }

                onClicked: {
                    var settings = {
                        "fire_alarm": {
                            "trigger_on_all_sensors": true,
                        },
                        "jeweller": {
                            "detector_ping_interval_seconds": hub.fire_interconnected && hub.hub_type == "HUB_2_PLUS" ? 72 : 48,
                        },
                        "_params": {
                            "alt_action_success": true,
                        },
                    }

                    app.hub_management_module.apply_update(management, hub, settings)
                }
            }
        }
    }

    Connections {
        target: app

        onAltActionSuccess: {
            popup.close()
        }
    }
}