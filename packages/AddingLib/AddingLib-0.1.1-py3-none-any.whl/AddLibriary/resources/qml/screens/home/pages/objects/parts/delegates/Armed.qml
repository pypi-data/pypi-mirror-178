import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"
import "qrc:/resources/qml/screens/home/pages/objects/parts"


Rectangle {
    width: header.width
    color: ui.colors.dark1
    height: 48

    property var header: objectsTable.headerItem

    Rectangle {
        width: parent.width
        height: 1
        color: ui.colors.black
        anchors.bottom: parent.bottom
    }

    ObjectMouseArea {}

    RowLayout {
        spacing: 0
        height: 48

        Item {
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[0] ? header.headerRow.children[0].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Image {
                sourceSize.width: 32
                sourceSize.height: 32
                source: "qrc:/resources/images/facilities/info/a.HubStatus-Convex.svg"
                anchors {
                    right: parent.right
                    rightMargin: 4
                    verticalCenter: parent.verticalCenter
                }

                Image {
                    sourceSize.width: 20
                    sourceSize.height: 20
                    anchors.centerIn: parent
                    source: {
                        if (!object) return ""
                        if (!object.security_state) return ""

                        var iconsPath = "qrc:/resources/images/facilities/status/"

                        // old
                        if (object.security_state == "ARMED") return iconsPath + "icon-a-hub-status-icon-armed.svg"
                        if (object.security_state == "DISARMED") return iconsPath + "icon-a-hub-status-icon-disarmed.svg"

                        // new
                        if (object.security_state == "NO_STATE_WITH_GROUPS_INFO") return ""  // iconsPath + "icon-a-hub-status-icon-disarmed_with_groups.svg"

                        if (object.security_state == "ARMED_NIGHT_MODE_ON") return iconsPath + "icon-a-hub-status-icon-armed.svg"
                        if (object.security_state == "ARMED_NIGHT_MODE_OFF") return iconsPath + "icon-a-hub-status-icon-armed.svg"
                        if (object.security_state == "DISARMED_NIGHT_MODE_ON") return iconsPath + "icon-a-hub-status-icon-night-mode.svg"
                        if (object.security_state == "DISARMED_NIGHT_MODE_OFF") return iconsPath + "icon-a-hub-status-icon-disarmed.svg"
                        if (object.security_state == "PARTIALLY_ARMED_NIGHT_MODE_ON") return iconsPath + "icon-a-hub-status-icon-night-mode.svg"
                        if (object.security_state == "PARTIALLY_ARMED_NIGHT_MODE_OFF") return iconsPath + "icon-a-hub-status-icon-partially-armed.svg"

                        return "qrc:/resources/images/events/logo.svg"
                    }
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[2] ? header.headerRow.children[2].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: number ? number : ui.empty
                color: ui.colors.light3
                width: parent.width - 16
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[4] ? header.headerRow.children[4].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: name ? name : ui.empty
                color: ui.colors.light1
                font.pixelSize: 16
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[6] ? header.headerRow.children[6].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: address ? address : ui.empty
                color: ui.colors.middle1
                font.pixelSize: 14
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 2
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[8] ? header.headerRow.children[8].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: hub_id ? hub_id : ui.empty
                color: ui.colors.light3
                width: parent.width - 16
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }
    }
}