import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
//  ButtonMini component
    property alias buttonMini: buttonMiniControl
//  Component atomTitle
    property alias atomTitle: atomTitle

    width: parent.width
    height: Math.max(buttonMiniControl.height + 16, atomTitle.height + 8)

    color: ui.ds3.bg.highest

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: parent.left
            right: buttonMiniControl.left
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }
    }


    DS3.ButtonMini {
        id: buttonMiniControl

        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }

        color: ui.ds3.figure.interactive
        opacity: enabled ? 1 : 0.3
    }
}