import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    visible: device.gb_allowed
    atomTitle {
        title: tr.glass_shutter_protection_sensitivity
        subtitle: {
            return [0, 1, 2].includes(device.motion_sensitivity) ? {
                0: tr.device_settings_sensitivity_array_0,
                1: tr.normal,
                2: tr.device_settings_sensitivity_array_2
            }[device.motion_sensitivity] : tr.na
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Sensitivity-M.svg"
}