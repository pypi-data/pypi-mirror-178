import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: gbSensor.checked
    currentIndex: device.gb_sensitivity
    atomTitle.title: tr.glass_break_sensor_sensitivity
    model: [tr.low, tr.normal, tr.high]
}