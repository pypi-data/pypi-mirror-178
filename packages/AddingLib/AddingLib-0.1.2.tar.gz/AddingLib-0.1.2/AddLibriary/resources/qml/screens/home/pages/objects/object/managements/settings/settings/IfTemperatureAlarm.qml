import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.if_temperature_threshold_exceeded
    checked: device.siren_triggers.includes(1)
    visible: highTemperatureAlarm.checked
}