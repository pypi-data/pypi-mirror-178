import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: settingsSwitch

//  Title of the settings
    property alias title: atomTitle.title
//  Subtitle of the settings
    property alias subtitle: atomTitle.subtitle
//  SubtitleIcon component
    property alias subtitleIcon: atomTitle.subtitleIcon
//  Whether switch is toggled
    property alias checked: control.checked
//  Callback on toggle action
    property var onSwitched: () => checked = !checked
//  Property which can change the active color of indicator
    property alias isDanger: control.isDanger
//  The alias for enabling or cancelling binding on the control component
    property alias cancelBinding: control.cancelBinding


    width: parent.width
    height: atomTitle.height + 22

    color: ui.ds3.bg.highest

    DS3.AtomTitle {
        id: atomTitle

        anchors {
            left: parent.left
            right: control.left
            margins: 16
            verticalCenter: parent.verticalCenter
        }
    }

    DS3.Switch {
        id: control

        anchors {
            right: parent.right
            margins: 16
            verticalCenter: parent.verticalCenter
        }

        onToggle: () => onSwitched()
    }
}