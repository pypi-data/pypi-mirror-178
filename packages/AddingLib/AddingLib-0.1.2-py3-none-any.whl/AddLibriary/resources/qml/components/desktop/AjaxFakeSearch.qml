import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Controls.impl 2.2
import QtQuick.Templates 2.2 as T


Item {
    id: fakeSearch
    width: 256
    height: 32

    property var icon: ""
    property var currentText: ""
    property var defaultText: ""

    property alias field: topLevel
    property alias mouseArea: mouseArea

    TextField {
        id: topLevel
        text: fakeSearch.currentText
        selectByMouse: true
        color: ui.colors.light1
        font.pixelSize: 13
        readOnly: true
        font.family: roboto.name
        font.weight: Font.Medium
        font.letterSpacing: 1
        leftPadding: 10
        bottomPadding: 5
        rightPadding: 32
        width: parent.width - 64
        height: parent.height
        anchors.centerIn: parent

        PlaceholderText {
            id: placeholder
            x: topLevel.leftPadding
            y: topLevel.topPadding
            width: topLevel.width - (topLevel.leftPadding + topLevel.rightPadding)
            height: topLevel.height - (topLevel.topPadding + topLevel.bottomPadding)
            visible: !topLevel.length && !topLevel.preeditText && (!topLevel.activeFocus || topLevel.horizontalAlignment !== Qt.AlignHCenter)

            text: fakeSearch.defaultText
            font: topLevel.font
            opacity: 0.5
            color: ui.colors.light1
            verticalAlignment: topLevel.verticalAlignment
            elide: Text.ElideRight
        }

        background: Rectangle {
            implicitWidth: topLevel.width
            implicitHeight: topLevel.height
            color: topLevel.enabled ? "#616161" : "gray"
            radius: 3

            Image {
                sourceSize.width: 24
                sourceSize.height: 24
                visible: true
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: parent.right
                    rightMargin: 6
                }

                source: fakeSearch.icon
            }
        }
    }

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor
    }
}
