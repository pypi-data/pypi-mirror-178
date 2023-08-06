import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
//  Main text
    property alias textItem: textItem
//  Caps text variant
    property bool isCaps: false

    width: parent.width
    height: textItem.height + 8

    DS3.Text {
        id: textItem

        anchors {
            left: parent.left
            verticalCenter: parent.verticalCenter
            right: parent.right
        }

        style: isCaps ? ui.ds3.text.special.SectionCaps : ui.ds3.text.body.MRegular
        color: ui.ds3.figure.secondary
        opacity: enabled ? 1 : 0.3
    }
}
