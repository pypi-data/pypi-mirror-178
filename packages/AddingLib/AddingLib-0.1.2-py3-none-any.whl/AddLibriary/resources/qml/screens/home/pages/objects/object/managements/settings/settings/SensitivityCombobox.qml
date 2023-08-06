import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.sensitivity
    model: [tr.low, tr.normal, tr.high]
    visible: shockSensor.checked
    currentIndex: {
        if (device.sensitivity == 0) {
            return 0
        } else if (device.sensitivity == 4) {
            return 1
        } else if (device.sensitivity == 7) {
            return 2
        } else {
            return -1
        }
    }
}