import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.high_temperature_alarm
    checked: device.temperature_alarm_enable
}