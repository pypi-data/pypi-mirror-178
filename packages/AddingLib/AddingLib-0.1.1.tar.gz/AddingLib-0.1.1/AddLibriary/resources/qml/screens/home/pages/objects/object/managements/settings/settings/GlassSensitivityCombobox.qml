import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.sensitivity
    model: [tr.low, tr.normal, tr.high]
    currentIndex: device.sensitivity
}