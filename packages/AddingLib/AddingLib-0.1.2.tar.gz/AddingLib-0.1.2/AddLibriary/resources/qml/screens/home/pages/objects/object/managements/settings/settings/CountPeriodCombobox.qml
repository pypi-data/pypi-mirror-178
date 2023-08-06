import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.countPeriod
    model: [5, 10, 15, 20, 25, 30]
    visible: device.roller_shutter_available && device.roller_shutter_available && externalContact.checked && extraContactTypeCombobox.currentIndex == 1
    currentIndex: device.count_period / 5 - 1
}