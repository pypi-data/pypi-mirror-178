import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.DeviceSimple {
//  Is this device chosen
    property var isChosen: false
//  Gear control component
    property alias gearControl: gearControl
//  Main mouse area component
    property alias mouseArea: mouseArea
//  List of values whose containsMouse has to be in check with the component background
    property var colorCheck: []

//  On actionArrow control clicked
    signal actionArrowControlClicked
//  On gear control clicked
    signal gearControlClicked

    smallImage: true
    color: {
        if (isChosen) return ui.ds3.figure.inverted
        return [
            mouseArea,
            gearControl.buttonIconMouseArea,
            ...colorCheck
        ].some(el => el.containsMouse) ? ui.ds3.bg.high : ui.ds3.bg.highest
    }
    hasOnlineTextMessage: true
    Behavior on color {
        ColorAnimation { duration: 100 }
    }
    atomTitle.titleItem.color: ui.ds3.figure.base
    deviceImage.opacity: 1
    textColumn {
        anchors {
            right: gearControl.left
            rightMargin: 16
        }
        opacity: 1
    }

    DS3.ButtonIcon {
        id: actionArrow

        anchors {
            verticalCenter: textColumn.verticalCenter
            right: parent.right
            rightMargin: 16
        }

        source: "qrc:/resources/images/Athena/common_icons/ActionArrow.svg"
        color: ui.ds3.figure.nonessential
    }

    DS3.MouseArea {
        id: mouseArea

        onClicked: actionArrowControlClicked()
    }

    DS3.ButtonIcon {
        id: gearControl

        anchors {
            verticalCenter: textColumn.verticalCenter
            right: actionArrow.left
            rightMargin: 16
        }

        source: "qrc:/resources/images/Athena/common_icons/Settings-M.svg"
        color: ui.ds3.figure.interactive

        onClicked: gearControlClicked()
    }
}
