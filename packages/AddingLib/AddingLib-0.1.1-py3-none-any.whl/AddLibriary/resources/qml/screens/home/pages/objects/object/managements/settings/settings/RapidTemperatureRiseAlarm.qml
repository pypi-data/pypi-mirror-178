import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.rapid_temperature_rise_alarm
    checked: device.temp_diff_enable
    visible: highTemperatureAlarm.checked
}
