import QtQuick 2.12
import QtQuick.Controls 2.13


Item {
//  Amount of steps
    property int amount: 2
//  Index of current step. Starts at 0
    property int current: 0

    width: parent.width
    height: 4

    Row {
        width: parent.width

        Repeater {
            model: amount

            Rectangle {
                width: parent.width / amount
                height: 4

                color: current > index ? ui.ds3.figure.interactive : ui.ds3.special.hole

                Behavior on color {
                    ColorAnimation {
                        duration: 1000
                    }
                }
            }
        }
    }
}
