import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.countTreshold
    model: [2, 3, 4, 5, 6, 7]
    visible: device.roller_shutter_available && externalContact.checked && extraContactTypeCombobox.currentIndex == 1
    currentIndex: device.count_threshold - 2
}