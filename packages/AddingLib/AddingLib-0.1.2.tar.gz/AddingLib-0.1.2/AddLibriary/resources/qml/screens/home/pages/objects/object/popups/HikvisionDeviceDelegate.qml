import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.0


Rectangle {
    radius: 10
    color: "#272727"
    opacity: 1

    property var device: null
    property var main: null

    Image {
        id: deviceImage
        opacity: 1.0
        width: 64
        height: 64
        source: {
            if (device.type == "device") return "qrc:/resources/images/desktop/delegates/dvr.png"
            return "qrc:/resources/images/desktop/delegates/Cameras/Cameras-96.png"
        }

        anchors {
            verticalCenter: parent.verticalCenter
            left: parent.left
            leftMargin: device.type == "device" ? 12 : 4
        }
    }

    Text {
        id: deviceName
        font.family: roboto.name
        font.pixelSize: 14
        font.letterSpacing: 1
        elide: Text.ElideRight
        color: ui.colors.light1
        opacity: 0.9
        width: parent.width - 64 - 24
        horizontalAlignment: Text.AlignLeft
        text: {
            if (device.type == "device") return device.deviceName
            return device.channelName
        }

        anchors {
            top: parent.top
            topMargin: 8
            left: deviceImage.right
            leftMargin: device.type == "device" ? 12 : 0
        }
    }

    Text {
        id: roomName
        opacity: 0.6
        font.family: roboto.name
        font.pixelSize: 12
        font.letterSpacing: 1
        elide: Text.ElideRight
        width: parent.width - 70
        color: ui.colors.white
        text: {
            if (device.type == "device") return device.deviceVersion
            return "# " + device.channelNo
        }

        anchors {
            top: deviceName.bottom
            topMargin: 2
            left: deviceImage.right
            leftMargin: device.type == "device" ? 12 : 0
        }
    }

    Text {
        id: serial
        opacity: 0.6
        font.family: roboto.name
        font.pixelSize: 12
        font.letterSpacing: 1
        elide: Text.ElideRight
        width: parent.width - 70
        color: ui.colors.white
        text: {
            if (main) return "Serial: " + device.deviceSerial
            return ""
        }

        anchors {
            bottom: parent.bottom
            bottomMargin: 6
            left: deviceImage.right
            leftMargin: device.type == "device" ? 12 : 0
        }
    }

    Image {
        width: 16
        height: 16
        source: {
            if (!device) return "qrc:/resources/images/views_icons_Athena2/ic-connect-green.png"
            return device.status == 0 ? "qrc:/resources/images/views_icons_Athena2/ic-connect-red.png" : "qrc:/resources/images/views_icons_Athena2/ic-connect-green.png"
        }
        anchors {
            right: parent.right
            rightMargin: 6
            bottom: parent.bottom
            bottomMargin: 6
        }
    }
}