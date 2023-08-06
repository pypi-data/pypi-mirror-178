import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    width: 24
    height: 8

    Custom.HandMouseArea {
        anchors.fill: parent
    }

    Rectangle {
        width: 24
        height: 2
        color: ui.colors.middle4
    }

    Rectangle {
        width: 24
        height: 2
        color: ui.colors.middle4
        anchors.bottom: parent.bottom
    }
}