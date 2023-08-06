import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3


Item {
//  Property changed the help text
    property alias textItem: textItem

    height: 32
    width: mainRow.width

    Row {
        id: mainRow

        anchors.horizontalCenter: parent.horizontalCenter

        spacing: 8

        DS3.Spinner {
            anchors.verticalCenter: parent.verticalCenter
        }

        DS3.Text {
            id: textItem

            anchors.verticalCenter: parent.verticalCenter
            visible: textItem.text
            style: ui.ds3.text.body.LRegular
        }
    }
}