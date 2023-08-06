import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Text of the button
    property alias buttonText: button.text
//  Whether background exists
    property bool hasBackground: false
//  Whether comment is visible
    property alias hasComment: comment.visible
//  Text of the comment
    property alias commentText: comment.text
//  Icon of the comment
    property alias commentIcon: comment.icon
//  Color of the comment
    property alias commentColor: comment.itemsColor
//  Whether you need to change button
    property alias button: button
//  If has stepper
    property alias hasStepper: stepper.visible
//  Amounts of steps (use if button has stepper)
    property alias stepAmount: stepper.amount
//  Current step (use if button has stepper)
    property alias currentStep: stepper.current
//  Is rounded on the bottom
    property var isRoundBottom: false
// top margin for when the element is being rounded on the bottom
    property var roundingMargin: 8
//  Source to left icon
    property alias iconSource: button.buttonIconSource
//  If button is outline
    property alias isOutline: button.isOutline
//  buttons column that can hold any number of buttons
    property alias buttons: buttons.children

    width: parent.width
    height: 32 + (comment.visible ? 28 : 0) + (stepper.visible ? 12 : 0) + buttons.height
    color: hasBackground ? ui.ds3.bg.high : ui.ds3.figure.transparent

    DS3.Stepper {
        id: stepper

        anchors {
            top: parent.top
            topMargin: 8
            horizontalCenter: parent.horizontalCenter
        }

        visible: false
    }

    DS3.Comment {
        id: comment

        anchors {
            top: hasStepper ? stepper.bottom : parent.top
            topMargin: 8
            left: parent.left
            leftMargin: 24
            right: parent.right
            rightMargin: 24
        }

        visible: false
    }

    Column {
        id: buttons

        Component.onCompleted: {
            for(let i = 0; i < children.length; i++) {
                children[i].width = Qt.binding(() => buttons.width)
            }
        }

        spacing: 8

        anchors {
            top: {
                if (comment.visible) return comment.bottom
                if (stepper.visible) return stepper.bottom
                return parent.top
            }
            left: parent.left
            right: parent.right
            leftMargin: 24
            rightMargin: 24
            bottomMargin: 24
            topMargin: comment.visible ? 0 : 8
        }

        DS3.ButtonContained {
            id: button
        }
    }
}
