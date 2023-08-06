import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: control
    width: typeText.contentWidth + 32
    height: 40

    property var text: ""
    property var selected: false

    property alias typeArea: typeArea
    property alias color: typeText.color
    property alias tabColor: tabItem.color

    Rectangle {
        id: tabItem
        width: parent.width
        height: parent.height
        radius: height / 2
        color: control.selected ? ui.colors.black : ui.colors.dark4

        Custom.FontText {
            id: typeText
            text: control.text
            color: control.selected ? ui.colors.middle1 : ui.colors.middle3
            font.pixelSize: 14
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            anchors.centerIn: parent
        }

        Custom.HandMouseArea {
            id: typeArea
        }
    }
}