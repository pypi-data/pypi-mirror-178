import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Image source
    property alias source: leftImage.source
//  Main text
    property alias atomTitle: atomTitle

    implicitWidth: 375
    height: 68

    opacity: enabled ? 1 : 0.3
    color: ui.ds3.bg.highest

    DS3.Image {
        id: leftImage

        width: 40
        height: 40

        anchors {
            left: parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
        }
    }

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: leftImage.source != "" ? leftImage.right : parent.left
            leftMargin: 16
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 16
        }
    }
}
