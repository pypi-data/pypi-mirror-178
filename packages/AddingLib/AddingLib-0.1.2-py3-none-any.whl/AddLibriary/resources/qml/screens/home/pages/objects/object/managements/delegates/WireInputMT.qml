import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/images.js" as Images

CommonPart {
    imageSource: Images.get_image(
        device.obj_type,
        "Medium",
        device.input_type,
        device.custom_alarm_available_v2 ? device.custom_alarm_S2 : device.custom_alarm
    )
}