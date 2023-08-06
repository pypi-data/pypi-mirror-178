import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.pulse_duration
    model: {
        var t = [...Array(256).keys()]
        t[0] = 0.5
        return t
    }
    currentIndex: device.pulse_length
    suffix: " " + tr.sec
}