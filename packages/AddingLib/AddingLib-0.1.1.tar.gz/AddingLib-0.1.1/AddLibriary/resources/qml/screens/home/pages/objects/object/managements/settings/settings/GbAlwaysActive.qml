import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch  {
    title: tr.glass_break_sensor_always_active
    checked: device.gb_always_active
    visible: gbSensor.checked
}
