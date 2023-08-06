import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.alarm_indication_off
    checked: device.indicator_light_mode == "STANDARD"
    visible: device.indicator_light_mode_available
}
