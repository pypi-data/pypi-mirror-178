import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Item {
    id: topLevel
    property var index: -1
    property var text: "default"
    property var selected: index == header.currentState
    property var fontSize: 22
    property alias selectArea: selectArea
    property var sourceIcon: ""

    property alias fillRect: fillRect
    property alias imageItem: imageItem

    Rectangle {
        id: fillRect
        visible: topLevel.sourceIcon != ""
        color: selected ? ui.colors.dark4 : "transparent"
        anchors.fill: parent
    }

    Item {
        id: item
        width: parent.height
        height: parent.height

        Rectangle {
            width: 22
            height: 22
            radius: 11
            anchors.centerIn: parent
            color: selected ? ui.colors.green1 : ui.colors.middle1
            opacity: selected ? 1.0 : 0.3
            visible: topLevel.sourceIcon == ""
        }

        Image {
            id: imageItem
            visible: topLevel.sourceIcon != ""
            source: topLevel.sourceIcon
            sourceSize.width: 24
            sourceSize.height: 24
            anchors.centerIn: parent
        }
    }

    Custom.FontText {
        text: topLevel.text
        color: ui.colors.white
        font.pixelSize: topLevel.fontSize
        anchors {
            verticalCenter: parent.verticalCenter
            left: item.right
            leftMargin: 12
        }
    }

    Custom.HandMouseArea {
        id: selectArea
        anchors.fill: parent
    }
}