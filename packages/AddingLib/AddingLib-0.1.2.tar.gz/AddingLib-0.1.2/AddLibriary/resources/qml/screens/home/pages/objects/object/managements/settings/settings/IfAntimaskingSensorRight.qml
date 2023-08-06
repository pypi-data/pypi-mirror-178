import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.alert_with_siren_antimasking_right
    checked: device.siren_triggers.includes(4)
    visible: device.right_motion_antimasking
}