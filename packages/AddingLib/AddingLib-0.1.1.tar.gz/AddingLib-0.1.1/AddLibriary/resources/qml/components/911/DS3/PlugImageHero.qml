import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    property alias source: icon.source

    width: parent.width
    height: 200

    color: ui.ds3.figure.transparent

    anchors.horizontalCenter: parent.horizontalCenter

    DS3.Icon {
        id: icon

        anchors.centerIn: parent
    }
}