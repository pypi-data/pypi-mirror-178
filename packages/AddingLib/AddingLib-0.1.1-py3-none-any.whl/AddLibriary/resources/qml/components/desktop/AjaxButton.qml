import QtQuick 2.7
import QtQuick.Controls 2.1

Button {
    id: topLevel
    width: contentItem.contentWidth + 32
    height: contentItem.contentHeight + 32

    property var color: enabled ? "#60e3ab" : ui.colors.middle3
    property alias buttonText: buttonText

    background: Rectangle {
        color: {
            return topLevel.down ? topLevel.color : "transparent"
        }
        border.color: {
            return topLevel.color
        }
        border.width: 2
    }

    contentItem: Text {
        id: buttonText

        text: topLevel.text
        color: ui.colors.light1
        font.family: roboto.name
        font.weight: Font.Medium
        font.pixelSize: 14
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
        onPressed: {
            mouse.accepted = false
        }
    }
}