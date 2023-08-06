import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.if_quick_temperature_rise_detected
    checked: device.siren_triggers.includes(2)
    visible: rapidTemperatureRiseAlarm.checked && highTemperatureAlarm.checked
}