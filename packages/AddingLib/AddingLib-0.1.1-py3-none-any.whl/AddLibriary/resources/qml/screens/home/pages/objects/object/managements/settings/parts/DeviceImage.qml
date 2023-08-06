import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/js/images.js" as Images

Item {
    width: parent.width
    height: 152

    property alias devImage: devImage

    Image {
        id: devImage

        width: 96
        height: 96
        anchors.centerIn: parent
        source: {
            if (device.obj_type == "28") {
                return Images.get_image(device.device_type != 2 ? "28-keypad-yavir" : "28-reader-yavir", "Medium")
            }
            if (device.obj_type == "1d") {
                return Images.get_image(device.obj_type, "Medium", device.input_type, device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm)
            }
            return Images.get_image(device.obj_type, "Medium", device.color, "TAMPER_ALARM", device.subtype)
        }
    }
}