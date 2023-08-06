import QtQuick 2.12
import QtQuick.Controls 2.13


Rectangle {
    id: copyItem
    property var backgroundColor: ui.colors.dark3

    property int sideSizeRect: 10
    property var copyText: ""
    property int toolBarSize: 500
    property var copy: function() {
        util.set_clipboard_text(copyItem.copyText)
    }
    color: "transparent"
    width: 18
    height: 18
    anchors.right: parent.right
    anchors.rightMargin: 16
    anchors.verticalCenter: parent.verticalCenter
    anchors.verticalCenterOffset: -1
    visible: true // mouse.containsMouse || copyArea.containsMouse

    Rectangle {
        id: greenRect
        width: copyItem.sideSizeRect
        height: copyItem.sideSizeRect
        color: "transparent"
        anchors.centerIn: parent
        radius: 3
        border {
            color: ui.colors.green1
            width: 1
        }

        Rectangle {
            width: copyItem.sideSizeRect
            height: copyItem.sideSizeRect
            border {
                color: parent.border.color
                width: 1
            }
            radius: parent.radius
            color: copyItem.backgroundColor
            anchors.centerIn: parent
            anchors.verticalCenterOffset: 3
            anchors.horizontalCenterOffset: -3
        }
    }

    HandMouseArea {
        id: copyArea
        anchors.fill: parent
        hoverEnabled: true
        onEntered: greenRect.border.color = ui.colors.green2
        onExited: greenRect.border.color = ui.colors.green1

        ToolTip {
            id: tooltip
            parent: parent

            contentItem: Text {
                text: tr.copied
                font.family: roboto.name
                font.pixelSize: 12
                color: ui.colors.light1
            }

            background: Rectangle {
                color: ui.colors.dark4
                radius: 4
                border {
                    width: 1
                    color: ui.colors.green1
                }
            }
        }

        onClicked: {
            copy()
            tooltip.show("", copyItem.toolBarSize)
        }
    }
}