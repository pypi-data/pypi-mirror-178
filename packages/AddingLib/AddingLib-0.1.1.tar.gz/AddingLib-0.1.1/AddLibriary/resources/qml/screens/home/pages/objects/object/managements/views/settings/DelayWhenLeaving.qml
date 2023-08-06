import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    visible: {
        if (!hub) return false
        var common_visibility = hub.firmware_version_dec >= 206000  && device.arm_delay_seconds
        if (device.obj_type == "1d") { // wireInputMT
           return common_visibility && device.input_type == 1 // sensor only
        }
        if (device.obj_type == "26") { // wireInput
           return common_visibility && !device.input_is_tamper // sensor only
        }
        return common_visibility
    }
    atomTitle {
        title: tr.delay_when_leaving_sec
        subtitle: device.arm_delay
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/DelayWhenLeaving-M.svg"
}