import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
//  Image source for the PlugImage
    property alias source: imageRect.source
//  Small icon component
    property alias smallIcon: iconComponent
//  ButtonMini component
    property alias buttonMini: buttonMini

    width: 136
    height: 136

    color: ui.ds3.bg.highest
    radius: width / 2

    DS3.Image {
        id: imageRect

        anchors.centerIn: parent

        width: 88
        height: 88
    }

    DS3.Image {
        id: iconComponent

        width: 40
        height: 40

        visible: iconComponent.source

        anchors {
            bottom: parent.bottom
            right: parent.right
        }
    }

    DS3.ButtonMini {
        id: buttonMini

        width: 51
        height: 30

        visible: buttonMini.source != ""

        anchors {
            bottom: parent.bottom
            right: parent.right
        }
    }
}