import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    visible: {
        if (!hub) return false
        var common_visibility = hub.firmware_version_dec >= 211100 && device.perimeter_arm_delay_seconds && device.night_mode_arm
        if (device.obj_type == "1d") { // wireInputMT
           return common_visibility && device.input_type == 1 // sensor only
        }
        if (device.obj_type == "26") { // wireInput
           return common_visibility && !device.input_is_tamper // sensor only
        }
        return common_visibility
    }
    atomTitle {
        title: tr.delay_when_leaving_in_night_mode_sec
        subtitle: device.perimeter_arm_delay_seconds
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/DelayWhenLeavingNightMode-M.svg"
}