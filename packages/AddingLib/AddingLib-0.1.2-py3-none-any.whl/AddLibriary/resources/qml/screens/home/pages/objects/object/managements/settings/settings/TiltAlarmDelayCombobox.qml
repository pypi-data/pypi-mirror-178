import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.tilt_alarm_delay
    model: ["1 " + tr.sec, "2 " + tr.sec, "5 " + tr.sec, "10 " + tr.sec, "30 " + tr.sec, "1 " + tr.min]
    visible: tiltSensor.checked
    currentIndex: device.tilt_alarm_delay - 1
}