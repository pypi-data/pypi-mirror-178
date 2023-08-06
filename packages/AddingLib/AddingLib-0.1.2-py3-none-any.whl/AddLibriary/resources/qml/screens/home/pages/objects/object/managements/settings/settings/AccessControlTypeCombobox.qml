import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: hub.firmware_version_dec >= 208100
    atomTitle.title: tr.access_contol_type
    model: [tr.wired_keypad, tr.wired_key_reader]
    currentIndex: device.device_type - 1
}