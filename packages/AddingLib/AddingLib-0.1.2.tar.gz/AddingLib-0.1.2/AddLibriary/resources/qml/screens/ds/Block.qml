import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
    default property alias data: content.data
    property alias title: textItem.text

    width: parent.width
    height: content.height + 40 + textItem.height

    visible: searchField.atomInput.text ? title.toLowerCase().includes(searchField.atomInput.text.toLowerCase()) : true

    DS3.Text {
        id: textItem

        style: ui.ds3.text.title.LBold
    }

    Rectangle {
        anchors {
            bottom: parent.bottom
            top: textItem.bottom
        }

        width: parent.width

        color: ui.ds3.figure.transparent
        border {
            color: ui.ds3.figure.interactive
            width: 3
        }
        radius: 10

        Column {
            id: content

            width: parent.width - 40

            anchors.centerIn: parent

            spacing: 10
        }
    }
}
