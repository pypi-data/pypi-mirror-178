import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

Rectangle {
    id: topLevel
    width: parent.width
    height: 48
    clip: true

    property var active: false
    property var iconSource: ""
    property var iconSourceDisabled: ""
    property var text: ""
    property var rightText: ">"
    property var selected: false

    color: topLevel.active ? "#3a3a3a" : "transparent"

    Rectangle {
        visible: parent.active
        width: 3
        height: 50
        color: ui.colors.green1
        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
        }
    }

    Item {
        visible: selected && !active
        anchors.fill: parent

        Rectangle {
            width: 12
            height: 12
            color: ui.colors.green1
            rotation: 45
            transformOrigin: Item.Center
            anchors {
                verticalCenter: parent.top
                horizontalCenter: parent.left
            }
        }

        Rectangle {
            width: 12
            height: 12
            color: ui.colors.green1
            rotation: 45
            transformOrigin: Item.Center
            anchors {
                verticalCenter: parent.bottom
                horizontalCenter: parent.left
            }
        }
    }

    Item {
        width: parent.width - 64
        height: 48

        anchors.centerIn: parent

        Image {
            id: icon
            width: 36
            height: 36

            source: topLevel.enabled ? topLevel.iconSource : topLevel.iconSourceDisabled

            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                leftMargin: 1
            }
        }

        Text {
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 12
            opacity: enabled ? 1 : 0.5
            text: topLevel.text

            anchors {
                verticalCenter: parent.verticalCenter
                left: icon.right
                leftMargin: 16
            }
        }

        Image {
            id: arrow
            width: 22
            height: 22
            rotation: active ? 0 : 180
            source: "qrc:/resources/images/desktop/icons/ic-back-arrow@2x.png"

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
            }

            opacity: topLevel.enabled ? 1.0 : 0.2
            visible: rightText
        }

        Text {
            color: ui.colors.light1
            font.family: roboto.name
            font.pixelSize: 12
            opacity: enabled ? 1 : 0.5
            text: topLevel.rightText

            visible: false

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
                rightMargin: 4
            }
        }
    }
}
