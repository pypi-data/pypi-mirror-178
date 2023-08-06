import QtQuick 2.12
import QtQuick.Controls 2.13

Row {
    id: repeaterRow

//  Amount of steps
    property int amount: 2
//  Index of current step. Starts at 0
    property int current: 0
    property int sideMargin: 24

    height: 4
    width: parent.width - sideMargin * 2

    spacing: 4

    Repeater {
        model: amount

        Rectangle {
            width: parent.width / amount - 4
            height: 4

            color: current >= index ? ui.ds3.figure.interactive : ui.ds3.special.hole
            radius: 4

            Behavior on color {
                ColorAnimation {
                    duration: 200
                }
            }
        }
    }
}
