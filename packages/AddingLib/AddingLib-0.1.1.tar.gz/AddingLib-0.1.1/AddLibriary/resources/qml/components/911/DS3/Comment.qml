import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

Item {
//  Text of the comment
    property alias text: textField.text
//  Icon of the comment
    property alias icon: iconItem.source
//  Text color
    property var itemsColor: ui.ds3.figure.secondary
//  Style of the comment
    property alias style: textField.style

    width: parent.width || 300
    height: rowItem.height + 8

    opacity: enabled ? 1 : 0.3

    Row {
        id: rowItem

        width: parent.width
        height: textField.height

        anchors.verticalCenter: parent.verticalCenter

        spacing: 8

        DS3.Icon {
            id: iconItem

            anchors {
                top: parent.top
                topMargin: 1
            }

            color: itemsColor
        }

        DS3.Text {
            id: textField

            width: parent.width - iconItem.width

            anchors.verticalCenter: parent.verticalCenter

            style: ui.ds3.text.body.MRegular
            color: itemsColor
        }
    }
}