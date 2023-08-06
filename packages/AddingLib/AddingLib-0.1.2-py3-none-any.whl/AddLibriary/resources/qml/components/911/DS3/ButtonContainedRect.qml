import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


ButtonRect {
    id: buttonContainedRect

    generalOpacity: enabled ? 1 : 0.3

    background: Rectangle {
        id: background

        anchors.fill: parent

        radius: 8
        color: pressed ? ui.ds3.bg.lowest : buttonContainedRect.color
    }
}