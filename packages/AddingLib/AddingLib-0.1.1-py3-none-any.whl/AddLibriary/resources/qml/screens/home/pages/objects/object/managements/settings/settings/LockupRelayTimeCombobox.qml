import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    scrollToChosenWhenOpened: true
    atomTitle.title: tr.pulse_duration
    model: Array.apply(null, Array(255)).map(function (_, i) { return i + 1 })
    currentIndex: device.lockup_relay_time - 1
}
