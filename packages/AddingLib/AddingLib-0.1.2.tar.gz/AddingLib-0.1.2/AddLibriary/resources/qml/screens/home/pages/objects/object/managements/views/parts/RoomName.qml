import QtQuick 2.7
import QtQuick.Controls 2.2

Item {
    width: parent.width
    height: 16

    Text {
        id: roomName
        text: device.room_name
        font.family: roboto.name
        font.pixelSize: 12
        color: ui.colors.white
        opacity: 0.5
        anchors {
            centerIn: parent
        }
    }
}