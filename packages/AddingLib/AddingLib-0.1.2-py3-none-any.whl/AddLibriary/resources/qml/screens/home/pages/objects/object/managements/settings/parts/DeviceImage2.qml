import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/js/images.js" as Images

Item {
    width: parent.width
    height: 200

    property alias devImage: devImage

    Image {
        id: devImage

        width: 128
        height: 128

        anchors.centerIn: parent

        source: {
            if (device.obj_type == "28") {
                return Images.get_image(device.device_type != 2 ? "28-keypad-yavir" : "28-reader-yavir", "Large")
            }
            if (device.obj_type == "1d") {
                return Images.get_image(device.obj_type, "Large", device.input_type, device.custom_alarm)
            }
            return Images.get_image(device.obj_type, "Large", device.color, "0", device.subtype)
        }
    }
}