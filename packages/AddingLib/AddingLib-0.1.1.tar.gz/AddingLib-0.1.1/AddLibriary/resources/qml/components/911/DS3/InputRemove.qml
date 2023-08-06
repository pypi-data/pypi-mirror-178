import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InputSingleLine {
    signal remove

    inputsColumn.anchors {
        right: rightIconWrapper.left
        rightMargin: 0
    }

    Item {
        id: rightIconWrapper

        width: 56
        height: parent.height

        anchors {
            right: parent.right
            bottom: parent.bottom
            top: parent.top
        }

        Rectangle {
            id: minusCircle

            width: 24
            height: 24

            anchors.centerIn: parent

            color: inputMouseArea.containsMouse ? ui.ds3.figure.attention : ui.ds3.figure.nonessential
            radius: width / 2

            Behavior on color {
                ColorAnimation {
                    duration: 100
                }
            }
        }

        Rectangle {
            id: minusFilled

            height: 2
            width: 12

            anchors.centerIn: parent

            color: ui.ds3.figure.inverted
        }

        DS3.MouseArea {
            id: inputMouseArea

            hoverEnabled: true

            onClicked: remove()
        }
    }
}