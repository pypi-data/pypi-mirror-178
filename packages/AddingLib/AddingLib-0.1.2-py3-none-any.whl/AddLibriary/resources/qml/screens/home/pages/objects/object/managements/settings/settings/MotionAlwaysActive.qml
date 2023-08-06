import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.motion_sensor_always_active
    checked: device.motion_always_active
    visible: motionSensor.checked
}