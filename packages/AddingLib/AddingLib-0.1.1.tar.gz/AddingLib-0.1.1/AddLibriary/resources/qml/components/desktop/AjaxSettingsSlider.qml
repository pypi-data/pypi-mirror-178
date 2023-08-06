import QtQuick 2.7
import QtQuick.Controls 2.2


Item {
    id: topLevel
    width: parent.width
    height: textLabel.contentHeight + 12
    opacity: enabled ? 1.0 : 0.5

    property string text: ""
    property alias from: control.from
    property alias to: control.to
    property alias stepSize: control.stepSize
    property alias value: control.value
    property alias handle: control.handle

    Item {
        width: parent.width - 64
        anchors.centerIn: parent

        Text {
            id: textLabel
            font.family: roboto.name
            font.pixelSize: 12
            color: ui.colors.light1
            text: topLevel.text
            wrapMode: Text.WordWrap
            width: parent.width - control.width - 12

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 8
            }
        }

        AjaxSlider {
            id: control
            width: 128
            from: topLevel.from
            to: topLevel.to
            stepSize: topLevel.stepSize
            value: topLevel.value
            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
            }
        }
    }
}