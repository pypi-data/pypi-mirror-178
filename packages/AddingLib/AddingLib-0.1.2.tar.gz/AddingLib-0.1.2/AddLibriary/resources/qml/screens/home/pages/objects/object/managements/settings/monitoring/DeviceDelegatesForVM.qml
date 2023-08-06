import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/js/images.js" as Images

Rectangle {
    id: deleg

    width: 248
    height: 64

    opacity: device.online ? 1.0 : 0.3

    color: "transparent"

    Image {
        id: deviceImage

        width: 48
        height: 48
        source: {
            if (device.obj_type == "26") {
                return Images.get_image(device.wire_input_type != 2 ? "26-wired-intrusion" : "26-wired-tamper", "Small")
            }
            if (device.obj_type == "1d") {
                return Images.get_image(device.obj_type, "Small", device.input_type, device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm)
            }
            return Images.get_image(device.obj_type, "Small", device.color)
        }

        anchors {
            top: parent.top
            left: parent.left
        }
    }

    Text {
        id: deviceName

        text: device.name
        font.family: roboto.name
        font.pixelSize: 14
        color: ui.colors.light1
        anchors {
            top: parent.top
            topMargin: 2
            left: deviceImage.right
            leftMargin: 12
        }
    }

    Text {
        id: deviceIndex

        text: util.insert(tr.device_index_911, [device.device_index])
        font.family: roboto.name
        font.pixelSize: 12
        color: ui.colors.white
        opacity: 0.6
        anchors {
            top: deviceName.bottom
            left: deviceImage.right
            leftMargin: 12
        }
    }

    RowLayout {
        spacing: 0

        anchors {
            left: deviceImage.right
            bottom: parent.bottom
            bottomMargin: 3
        }

    }
}