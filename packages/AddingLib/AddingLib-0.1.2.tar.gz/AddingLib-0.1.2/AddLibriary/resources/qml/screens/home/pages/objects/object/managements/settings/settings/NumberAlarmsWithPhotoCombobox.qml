import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: !alwaysActive.checked
    atomTitle.title: tr.number_alarms_with_photo
    model: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, tr.all_photo]
    currentIndex: {
        if (device.number_alarms_with_photo == 0) return 10
        return device.number_alarms_with_photo - 1
    }
}