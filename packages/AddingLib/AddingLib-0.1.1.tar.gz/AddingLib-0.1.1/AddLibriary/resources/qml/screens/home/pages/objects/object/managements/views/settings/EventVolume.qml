import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    visible: (device.alarm_delay_beep || device.act_on_arming || device.chimes_enabled) && device.beep_on_delay_available
        && device.class_name != "wire_siren"
    atomTitle {
        title: tr.event_volume
        subtitle: ({
            1: tr.volume_max,
            18: tr.volume_mid,
            29: tr.volume_min
        }[device.beep_volume_level] || "")
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Volume-M.svg"
}
