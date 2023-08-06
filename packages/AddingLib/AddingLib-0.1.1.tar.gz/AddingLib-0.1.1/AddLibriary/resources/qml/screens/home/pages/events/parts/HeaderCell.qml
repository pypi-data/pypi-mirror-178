import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: headerCell
    clip: true
    Layout.minimumWidth: children[0].contentWidth + 32
    Layout.fillHeight: true
    Layout.fillWidth: true
    Layout.preferredWidth: 1

    property var text: ""

    Custom.FontText {
        text: parent.text
        color: ui.colors.middle1
        font.pixelSize: 12
        anchors {
            left: parent.left
            leftMargin: 12
            verticalCenter: parent.verticalCenter
        }
    }
}