import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3

// Athena 4.6

Rectangle {
    id: badgeRegular
//  Text of the badge
    property alias text: badgeItem.text
//  Switch the badge color to red if necessary
    property  alias color: badgeRegular.color

    width: badgeItem.width + 12
    height: badgeItem.height

    visible: !!text
    z: 1
    color: ui.ds3.figure.interactive
    radius: height/2

    DS3.Text {
        id: badgeItem

        anchors.centerIn: parent

        style: ui.ds3.text.button.SBold
        color: ui.ds3.figure.inverted
    }
}
