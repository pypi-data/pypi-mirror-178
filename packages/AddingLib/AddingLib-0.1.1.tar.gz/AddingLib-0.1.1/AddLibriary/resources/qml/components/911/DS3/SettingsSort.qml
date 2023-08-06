import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: settingsSort

//  Use for changing title text item
    property alias titleItem: titleItem
//  Use for changing icon item
    property alias iconItem: iconItem

    width: parent.width || 180
    height: 32

    color: ui.ds3.bg.highest

    DS3.Text {
        id: titleItem

        anchors {
            left: parent.left
            leftMargin: 16
            right: iconItem.left
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }
    }

    DS3.Icon {
        id: iconItem

        anchors {
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }
    }
}