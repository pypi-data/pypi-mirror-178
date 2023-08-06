import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


// Mini button with icon
Rectangle {
//  Icon of the button
    property alias source: iconItem.source
//  Mouse area of the button
    property alias containsMouse: buttonMiniMouseArea.containsMouse

//  On button clicked
    signal clicked

    width: 51
    height: 30

    radius: 15
    color: ui.ds3.figure.interactive

    DS3.Icon {
        id: iconItem

        anchors.centerIn: parent

        color: ui.ds3.figure.inverted
    }

    DS3.MouseArea {
        id: buttonMiniMouseArea

        onClicked: parent.clicked()
    }
}