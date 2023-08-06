import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Popup {
    id: sheetAction

    default property alias data: content.data
    property alias title: content.title

    width: 300
    height: content.height

    padding: 0
    y: parent.height - 8
    bottomMargin: 24
    topMargin: 24

    background: Rectangle {
        color: ui.ds3.bg.base
        radius: 12

        DropShadow {
            anchors.fill: back
            verticalOffset: 1
            radius: parent.radius
            samples: 30
            color: ui.backgrounds.overlay
            source: back
        }

        Rectangle {
            id: back

            anchors.fill: parent

            color: ui.ds3.bg.base
            radius: 10
        }
    }

    DS3.SettingsContainer {
        id: content

        width: parent.width
    }
}