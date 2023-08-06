import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: inputTime

    property alias leftPicker: leftPicker
    property alias middlePicker: middlePicker
    property alias rightPicker: rightPicker

    width: parent.width
    height: {
        console.log(Math.max(leftPicker.height,  middlePicker.height, rightPicker.height))
        return Math.max(leftPicker.height,  middlePicker.height, rightPicker.height)
    }

    DS3.InputPicker {
        id: leftPicker

        width: parent.width / 3 - 1

        anchors.left: parent.left

        input.showCommentError: false
    }

    DS3.InputPicker {
        id: middlePicker

        anchors {
            left: leftPicker.right
            leftMargin: 1
            right: rightPicker.left
            rightMargin: 1
        }

        input.showCommentError: false
    }

    DS3.InputPicker {
        id: rightPicker

        width: parent.width / 3 - 1

        anchors.right: parent.right

        input.showCommentError: false
    }
}
