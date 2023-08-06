import QtQuick 2.7
import QtQuick.Controls 2.1

Switch {
    id: topLevel

    property var color: ui.colors.green1
    property alias area: area

    MouseArea {
        id: area
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
    }

    indicator: Rectangle {
        implicitWidth: 40
        implicitHeight: 22
        x: topLevel.leftPadding
        y: parent.height / 2 - height / 2
        radius: 11
        color: "#575757"
        border.color: "transparent"

        Rectangle {
            x: topLevel.checked ? parent.width - width - 2: 2
            y: parent.height / 2 - height / 2
            width: 19
            height: 19
            radius: height / 2
            color: {
                return topLevel.enabled ? topLevel.color : "gray"
            }

        }
    }
}