import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.indication
    model: [tr.off, tr.always_enable, tr.when_socket_enabled]
    currentIndex: [1, 2, 3].includes(device.indication_mode) ? device.indication_mode - 1 : -1
}