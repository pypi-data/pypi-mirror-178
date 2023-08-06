import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: hub.firmware_version_dec >= 206000 && blocking.checked
    atomTitle.title: tr.time_to_block
    model: [3, 5, 10, 20, 30, 60, 90, 180]
    currentIndex: {
        var timeToBlockIndex = model.indexOf(device.time_to_block)
        return timeToBlockIndex == -1 ? 0 : timeToBlockIndex
    }
}
