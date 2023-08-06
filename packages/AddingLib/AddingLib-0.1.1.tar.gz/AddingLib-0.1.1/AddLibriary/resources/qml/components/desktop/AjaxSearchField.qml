import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Controls.impl 2.2
import QtQuick.Templates 2.2 as T


TextField {
    id: topLevel
    text: ""
    property var placeHolderText: ""
    selectByMouse: true
    color: ui.colors.light1
    font.pixelSize: 12
    font.family: roboto.name
    font.weight: Font.Medium
    leftPadding: 10
    bottomPadding: 5
    rightPadding: 32
    width: 256
    height: 32
    property var flag: text

    PlaceholderText {
        id: placeholder
        x: topLevel.leftPadding
        y: topLevel.topPadding
        width: topLevel.width - (topLevel.leftPadding + topLevel.rightPadding)
        height: topLevel.height - (topLevel.topPadding + topLevel.bottomPadding)

        text: topLevel.placeHolderText
        font: topLevel.font
        opacity: 0.5
        color: ui.colors.light1
        verticalAlignment: topLevel.verticalAlignment
        visible: !topLevel.length && !topLevel.preeditText && (!topLevel.activeFocus || topLevel.horizontalAlignment !== Qt.AlignHCenter)
        elide: Text.ElideRight
    }

    background: Rectangle {
        implicitWidth: 256
        implicitHeight: 32
        color: topLevel.enabled ? "#616161" : "gray"
        radius: 3
        Image {
            visible: flag
            width: 22
            height: 22
            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 2
            }
            source: {
                if (flag) {
                    width = 22
                    height = 22
                    anchors.rightMargin = 7
                } else {
                    width = 32
                    height = 32
                    anchors.rightMargin = 2
                }

                return "qrc:/resources/images/icons/ic-clear.png"
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    text = ""
                }
            }
        }
    }
}