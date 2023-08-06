import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.accel_tilt
    model: ["5\xB0", "10\xB0", "15\xB0", "20\xB0", "25\xB0"]
    visible: tiltSensor.checked
    currentIndex: {
        if (device.accel_tilt < 6) {
            return parseInt(device.accel_tilt) - 1
        } else {
            return -1
        }
    }
}