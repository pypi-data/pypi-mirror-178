import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Column {
//  Icon element for source and size manipulations
    property alias icon: icon
//  Text element for text and color manipulations
    property alias textElement: textElement

    width: parent.width

    anchors.horizontalCenter: parent.horizontalCenter

    padding: 16

    DS3.Icon {
        id: icon

        width: 40
        height: 40

        anchors.horizontalCenter: parent.horizontalCenter
    }

    DS3.Spacing { height: 24 }

    DS3.Text {
        id: textElement

        width: parent.width - 24 * 2

        color: ui.ds3.figure.base
        style: ui.ds3.text.body.LRegular
        horizontalAlignment: Text.AlignHCenter
    }
}