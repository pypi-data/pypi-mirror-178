import QtQuick 2.12
import QtQuick.Controls 2.13


Item {
    id: atomConnection

    width: 120
    height: 14

//  Maximum strength
    property int maxStrength: 3
//  Current signal level
    property int strength: 0
    property int sideMargin: 24

    Row {
        width: parent.width
        height: 4

        anchors.centerIn: parent

        spacing: 4

        Repeater {
            model: maxStrength

            Rectangle {
                width: parent.width / maxStrength - 2
                height: 4

                color: ui.ds3.figure.interactive
                opacity: strength > index ? 1 : 0.3
            }
        }
    }

}
