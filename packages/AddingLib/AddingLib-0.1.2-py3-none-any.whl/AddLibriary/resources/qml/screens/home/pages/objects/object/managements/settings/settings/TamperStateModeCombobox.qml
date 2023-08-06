import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.tamper_mode
    model: [tr.normally_open, tr.normally_closed]
    currentIndex: device.external_device_tamper_state_mode - 1
}