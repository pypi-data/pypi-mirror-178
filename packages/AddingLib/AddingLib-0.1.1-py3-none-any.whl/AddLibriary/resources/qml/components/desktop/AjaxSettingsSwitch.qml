import QtQuick 2.7
import QtQuick.Controls 2.2


Item {
    id: topLevel

    width: parent.width
    height: textLabel.contentHeight + 20
    opacity: enabled ? 1.0 : 0.5

    property string text: ""
    property bool checked: false
    property var color: ui.colors.green1
    property alias area: control.area
    property alias font: textLabel.font

    Item {
        width: parent.width - 80

        anchors.centerIn: parent

        Text {
            id: textLabel

            font.family: roboto.name
            font.pixelSize: 12
            color: ui.colors.light1
            text: topLevel.text
            wrapMode: Text.WordWrap
            width: parent.width - control.width

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
            }
        }

        AjaxSwitch {
            id: control

            checked: topLevel.checked
            color: topLevel.color
            width: 48

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
            }
        }

    }

}