import QtQuick 2.7
import QtQuick.Controls 2.2

Item {
    width: parent.width
    height: 48

    Text {
        id: deviceName
        text: device.name
        font.family: roboto.name
        font.pixelSize: 14
        color: ui.colors.white
        anchors {
            bottom: parent.bottom
            bottomMargin: 4
            horizontalCenter: parent.horizontalCenter
        }
    }
}