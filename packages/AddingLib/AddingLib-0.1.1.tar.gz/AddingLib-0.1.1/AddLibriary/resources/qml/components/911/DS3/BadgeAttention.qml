import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
    id: badgeAttention

//  Text of the badge
    property alias text: badgeItem.text

    width: badgeItem.width + 12
    height: badgeItem.height

    z: 1

    Rectangle {
        anchors.fill: parent

        color: ui.ds3.figure.attention
        radius: 4
    }

    Rectangle {
        height: badgeItem.height
        width: 4

        anchors {
            top: parent.top
            left: parent.left
        }

        color: ui.ds3.figure.attention
        radius: 4
    }

    DS3.Text {
        id: badgeItem

        anchors.centerIn: parent

        style: ui.ds3.text.special.BadgeRegular
        color: ui.ds3.figure.inverted
    }
}
