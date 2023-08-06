import QtQuick 2.7
import QtQuick.Controls 2.1

Switch {
    id: topLevel

    property var color: ui.colors.green1
    property alias area: area
    property var background_color: "#404040"

    MouseArea {
        id: area
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onClicked: {
            topLevel.focus = true
        }
    }

    indicator: Rectangle {
        implicitWidth: 48
        implicitHeight: 26
        x: topLevel.leftPadding
        y: parent.height / 2 - height / 2
        radius: 13
        color: background_color
        border.color: "transparent"

        Rectangle {
            x: topLevel.checked ? parent.width - width - 2: 2
            y: parent.height / 2 - height / 2
            width: 22
            height: 22
            radius: height / 2
            color: {
                if (!enabled) opacity = 0.5
                if (enabled) opacity = 1.0
                return topLevel.checked ? topLevel.color : "#9e9e9e"
            }

        }
    }
}