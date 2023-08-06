import QtQuick 2.7
import QtQuick.Controls 2.2


Item {
    id: topLevel
    width: parent.width
    height: inner.height + 24
    opacity: enabled ? 1.0 : 0.5

    property string text: ""
    property string descriptionText: ""
    property alias from: control.from
    property alias to: control.to
    property alias stepSize: control.stepSize
    property alias value: control.value
    property alias handle: control.handle

    Item {
        id: inner
        width: parent.width - 64
        anchors.centerIn: parent
        height: textLabel.contentHeight + control.height + descriptionLabel.contentHeight + 16

        Text {
            id: textLabel
            font.family: roboto.name
            font.pixelSize: 12
            color: ui.colors.light1
            text: topLevel.text
            width: parent.width - 128
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter

            anchors {
                top: parent.top
                horizontalCenter: parent.horizontalCenter
            }
        }

        AjaxSlider {
            id: control
            width: parent.width - 64
            from: topLevel.from
            to: topLevel.to
            stepSize: topLevel.stepSize
            value: topLevel.value
            anchors {
                top: textLabel.bottom
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            Text {
                text: control.value
                font.family: roboto.name
                font.pixelSize: 12
                color: ui.colors.green1

                anchors {
                    bottom: control.handle.top
                    bottomMargin: 4
                    horizontalCenter: control.handle.horizontalCenter
                }
            }

            Text {
                text: control.from
                font.family: roboto.name
                font.pixelSize: 12
                color: ui.colors.light1
                opacity: 0.7

                anchors {
                    left: control.left
                    leftMargin: -16
                }
            }

            Text {
                text: control.to
                font.family: roboto.name
                font.pixelSize: 12
                color: ui.colors.light1
                opacity: 0.7

                anchors {
                    right: control.right
                    rightMargin: -16
                }
            }
        }

        Text {
            id: descriptionLabel
            font.family: roboto.name
            font.pixelSize: 11
            color: ui.colors.light1
            opacity: 0.8
            text: topLevel.descriptionText
            width: parent.width - 128
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter

            anchors {
                top: control.bottom
                horizontalCenter: parent.horizontalCenter
            }
        }
    }
}