import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: typeCombobox.currentIndex == 0
    atomTitle.title: tr.external_contact_mode
    model: [tr.normally_open, tr.normally_closed, tr.eol, tr.eol_no]
    currentIndex: device.external_contact_mode - 2
}