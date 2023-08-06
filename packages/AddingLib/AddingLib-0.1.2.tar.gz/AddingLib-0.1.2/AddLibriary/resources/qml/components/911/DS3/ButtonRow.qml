import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Button {
    id: buttonRow

//  If text of the button is red
    property var isDanger: false
//  If text of the button on left side
    property bool rowLeftAlign: false
//  Color of button background
    property var color: ui.ds3.bg.highest

    width: parent.width
    height: 48

    Component.onCompleted: {
        if (width != 0) {
            buttonText.width = width - leftPadding - rightPadding
        } else {
            width = Qt.binding(() => {return buttonText.width + leftPadding + rightPadding})
        }
    }

    leftPadding: 16
    rightPadding: 16

    background: Rectangle {
        anchors.fill: parent

        color: buttonRow.color
        opacity: !enabled ? 0.3 : (pressed ? 0.6 : 1)
    }
    contentItem: DS3.Text {
        id: buttonText

        width: buttonRow.width

        anchors.verticalCenter: parent.verticalCenter

        text: buttonRow.text
        style: ui.ds3.text.body.MBold
        color: isDanger ? ui.ds3.figure.attention : ui.ds3.figure.interactive
        opacity: background.opacity
        horizontalAlignment: rowLeftAlign ? Text.AlignLeft : Text.AlignHCenter
        hasElide: true
    }

    DS3.MouseArea {
        onPressed: mouse.accepted = false
    }
}
