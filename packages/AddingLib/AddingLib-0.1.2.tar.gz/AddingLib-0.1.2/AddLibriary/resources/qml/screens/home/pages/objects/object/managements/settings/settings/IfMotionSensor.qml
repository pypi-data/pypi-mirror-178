import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.if_motion_detected
    checked: device.siren_triggers.includes(1)
}