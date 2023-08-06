import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSliderValue {
    visible: hub.firmware_version_dec >= 206000 && blocking.checked && deviceTypeCombobox.currentIndex == 0
    title: tr.time_to_block
    value: device.time_to_block
    from: 3
    to: 180
    suffix: tr.min
}
