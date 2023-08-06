import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS" as DS


// Button with icon inside it
Rectangle {
    id: buttonRound

//  style must be passes as `ui.controls.{style}`
    property var style
//  length of the side of button (24 for S(default), 32 for M)
    property var side: 24

//  Button is clicked
    signal clicked

    width: side
    height: side

    color: style.color
    radius: width

    DS.Icon {
        anchors.centerIn: parent

        source: style.imageSource
    }

    DS.MouseArea {
        onClicked: buttonRound.clicked()
    }
}
