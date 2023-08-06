import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS/" as DS


Rectangle {
    id: settingsSwitch

//  Text of the setting
    property alias text: textItem.text
//  State of the switch
    property alias checked: control.checked
//  Using rounded corner. If not there will be divider at the bottom
    property bool rounded: true
//  Weather toggle switch on click
    property bool autoToggle: true
//  Callback on switch toggled. Default is auto toggle
    property var onToggle: () => {
        checked = !checked
    }

    implicitWidth: parent.width
    implicitHeight: 16 + textItem.height

    opacity: enabled ? 1 : 0.3
    radius: rounded ? 8 : 0
    color: ui.backgrounds.highest

    DS.TextBodyLRegular {
        id: textItem

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 12
            right: control.left
            rightMargin: 8
        }
    }

    DS.Switch {
        id: control

        anchors {
            verticalCenter: parent.verticalCenter
            right: parent.right
            rightMargin: 12
        }

        onToggled: onToggle()
    }

    Rectangle {
        width: parent.width
        height: 1

        anchors.bottom: parent.bottom

        visible: !rounded
        color: ui.backgrounds.lowest
    }
}