import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.extraContactType
    model: [tr.external_contact, tr.roller_shutter]
    visible: device.roller_shutter_available && externalContact.checked
    currentIndex: device.extra_contact_type - 1
}