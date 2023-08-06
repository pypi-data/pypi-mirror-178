import QtQuick 2.12

import "qrc:/resources/qml/components/911/DS3/" as DS3


Item {
    width: 80
    height: 60

    property var navigationImageSource:null
    property var navigationText: null
    property bool isSelected: false

    DS3.Icon {
        id: navigationImage

        width: 24
        height: 24

        anchors {
            top: parent.top
            topMargin: 8
            horizontalCenter: parent.horizontalCenter
        }

        source: navigationImageSource
        color: isSelected ? ui.ds3.figure.interactive : ui.ds3.figure.secondary
    }

    DS3.Text {
        anchors {
            bottom: parent.bottom
            bottomMargin: 8
            horizontalCenter: parent.horizontalCenter
        }

        text: navigationText
        color: isSelected ? ui.ds3.figure.interactive : ui.ds3.figure.secondary
        style: ui.ds3.text.body.SRegular
    }
}
