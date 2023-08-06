import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
//  Color of the right circle
    property var circleColor: ui.ds3.figure.transparent
//  Main text
    property var mainText: "Color"
//  If selected
    property bool isSelected
//  Callback on clicked
    property var onSelected: () => {
        isSelected = !isSelected
    }

    implicitWidth: 36 + textItem.width + 16
    implicitHeight: 32

    radius: 16
    color: ui.ds3.figure.transparent
    border {
        width: 1

        color: isSelected ? ui.ds3.figure.interactive : ui.ds3.figure.transparent
    }

    Rectangle {
        width: 24
        height: 24

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 4
        }

        color: circleColor
        radius: 12
        border {
            width: 1

            color: isSelected ? ui.ds3.figure.interactive : ui.ds3.figure.transparent
        }
    }

    DS3.Text {
        id: textItem

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: 36
        }

        style: ui.ds3.text.body.MBold
        text: mainText
    }

    DS3.MouseArea {
        onClicked: {
            onSelected()
        }
    }
}
