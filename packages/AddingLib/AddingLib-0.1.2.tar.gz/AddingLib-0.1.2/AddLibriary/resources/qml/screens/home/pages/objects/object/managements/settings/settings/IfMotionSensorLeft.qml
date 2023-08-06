import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.alert_with_siren_motion_left
    checked: device.siren_triggers.includes(1)
    visible: device.left_motion_allowed
}