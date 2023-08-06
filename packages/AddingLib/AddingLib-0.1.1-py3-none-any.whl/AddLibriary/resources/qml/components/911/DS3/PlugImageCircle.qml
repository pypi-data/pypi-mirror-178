import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
//  Source of the icon
    property alias icon: icon.source
//  Color of the icon
    property alias iconColor: icon.color

    width: 136
    height: 136

    Rectangle {
        width: 128
        height: 128

        anchors.centerIn: parent

        color: ui.ds3.bg.highest
        radius: 64

        DS3.Icon {
            id: icon

            anchors.centerIn: parent
        }
    }
}
