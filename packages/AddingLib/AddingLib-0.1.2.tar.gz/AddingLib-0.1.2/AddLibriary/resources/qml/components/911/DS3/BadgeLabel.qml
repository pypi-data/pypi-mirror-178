import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Text of the badge
    property alias text: badgeItem.text
//  Is the badge outline
    property bool isOutline: false
//  The color that is being used while outlined
    property var outlineColor: ui.ds3.figure.secondary

    width: badgeItem.width + 12
    height: badgeItem.height

    z: 1

    color: isOutline ? ui.ds3.figure.transparent : ui.ds3.figure.interactive
    border {
        color: outlineColor
        width: isOutline ? 1 : 0
    }
    radius: 4

    DS3.Text {
        id: badgeItem

        anchors.centerIn: parent

        style: ui.ds3.text.special.BadgeRegular
        color: isOutline ? border.color : ui.ds3.figure.inverted
    }
}
