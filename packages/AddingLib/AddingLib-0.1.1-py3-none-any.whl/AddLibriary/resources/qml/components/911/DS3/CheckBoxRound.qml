import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


// Regular button
Button {
    id: checkBoxRound

//  the view of button (if outline, then background is transparent)
    property var isOutline: false

    /* -------------------------------------------- */
    /* desktop tests */
    property var accessibleAreaName: ""
    /* -------------------------------------------- */

    width: 40
    height: 40

    background: Rectangle {
        anchors.fill: parent

        radius: height
        color: isOutline ? ui.ds3.figure.transparent : ui.ds3.figure.interactive
        opacity: !enabled ? 0.3 : (pressed ? 0.6 : 1)
        border.color: isOutline ? ui.ds3.figure.nonessential : ui.ds3.figure.interactive
    }

    contentItem: Item {}

    DS3.Text {
        id: buttonText

        anchors.centerIn: parent

        text: checkBoxRound.text
        style: ui.ds3.text.body.MBold
        color: isOutline ? ui.ds3.figure.base : ui.ds3.bg.highest
        opacity: background.opacity
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        hasElide: true
    }

    DS3.MouseArea {
        onPressed: mouse.accepted = false
    }

    /* -------------------------------------------- */
    /* desktop tests */
    Accessible.name: checkBoxRound.accessibleAreaName
    Accessible.description: "<button enabled=" + Accessible.checkable + ">" + checkBoxRound.text + "</button>"
    Accessible.role: Accessible.Button
    Accessible.checkable: visible && enabled
    Accessible.onPressAction: {
        if (!Accessible.checkable) return
        checkBoxRound.clicked(true)
    }
    /* -------------------------------------------- */
}