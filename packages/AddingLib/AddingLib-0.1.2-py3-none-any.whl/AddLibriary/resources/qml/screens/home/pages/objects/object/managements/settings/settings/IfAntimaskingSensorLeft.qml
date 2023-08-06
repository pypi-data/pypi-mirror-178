import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.alert_with_siren_antimasking_left
    checked: device.siren_triggers.includes(3)
    visible: device.left_motion_antimasking
}