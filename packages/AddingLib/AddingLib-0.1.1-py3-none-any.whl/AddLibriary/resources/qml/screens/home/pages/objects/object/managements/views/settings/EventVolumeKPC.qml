import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.InfoTitle {
    visible: (device.alarm_delay_beep || device.act_on_arming || device.chimes_enabled) && device.beep_on_delay_available
    atomTitle {
        title: tr.event_volume
        subtitle: ({
            0: tr.volume_min,
            1: tr.volume_mid,
            2: tr.volume_max
        }[device.siren_events_volume])
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Volume-M.svg"
}