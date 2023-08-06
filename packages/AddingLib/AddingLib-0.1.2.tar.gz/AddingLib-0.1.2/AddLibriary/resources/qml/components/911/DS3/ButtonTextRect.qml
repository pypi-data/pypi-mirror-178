import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.ButtonRect {
    id: buttonContainedRect

    generalOpacity: {
        if (pressed) return 0.6
        if (!enabled) return 0.3
        return 1
    }

    background: Rectangle {
        id: background

        anchors.fill: parent

        color: ui.ds3.figure.transparent
    }
}



