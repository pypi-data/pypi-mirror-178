import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: inputTime

    property alias leftPicker: leftPicker
    property alias rightPicker: rightPicker

    width: parent.width
    height: Math.max(leftPicker.height, rightPicker.height)

    DS3.InputPicker {
        id: leftPicker

        anchors {
            left: parent.left
            right: parent.horizontalCenter
            rightMargin: 1
        }

        input.showCommentError: false
    }

    DS3.InputPicker {
        id: rightPicker

        anchors {
            left: parent.horizontalCenter
            right: parent.right
        }

        input.showCommentError: false
    }
}
