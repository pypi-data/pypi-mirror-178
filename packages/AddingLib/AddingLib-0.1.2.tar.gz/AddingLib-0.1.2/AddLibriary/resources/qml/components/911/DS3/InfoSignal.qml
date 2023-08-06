import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Component atomTitle
    property alias atomTitle: atomTitle
//  Component leftIcon
    property alias leftIcon: leftIcon
//  Component atomConnection
    property alias atomConnection: atomConnection

    implicitWidth: parent.width
    height: Math.max(atomTitle.height, 68)

    color: ui.ds3.bg.highest

    DS3.Icon {
        id: leftIcon

        anchors {
            left: parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
        }

        color: ui.ds3.figure.base
        opacity: enabled ? 1 : 0.3
    }

    Column {
        id: textBlock

        width: parent.width

        anchors {
            left: leftIcon.source != '' ? leftIcon.right : parent.left
            leftMargin: 16
            right: parent.right
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }

        opacity: enabled ? 1 : 0.3

        DS3.AtomTitle {
            id: atomTitle

            width: parent.width

            isPrimary: false
            elide: Text.ElideRight
        }

        DS3.AtomConnection {
            id: atomConnection

            anchors.left: parent.left
        }
    }
}