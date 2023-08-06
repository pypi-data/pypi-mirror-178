import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
//  ButtonMini component
    property alias switchControl: switchControl
//  Switch status
    property var switchChecked
//  Component atomTitle
    property alias atomTitle: atomTitle

//  Signal on the even of the switch being switched
    signal switched

    width: parent.width
    height: Math.max(switchControl.height + 16, atomTitle.height + 8)

    color: ui.ds3.bg.highest

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: parent.left
            right: switchControl.left
            rightMargin: 16
            verticalCenter: parent.verticalCenter
        }
    }

    DS3.Switch {
        id: switchControl

        anchors {
            right: parent.right
            verticalCenter: parent.verticalCenter
        }
        checked: switchChecked || false
        opacity: enabled ? 1 : 0.3

        onToggle: () => switched()
    }
}