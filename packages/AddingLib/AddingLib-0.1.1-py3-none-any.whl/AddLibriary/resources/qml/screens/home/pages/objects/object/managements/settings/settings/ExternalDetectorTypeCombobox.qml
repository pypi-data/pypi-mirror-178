import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.external_detector_type
    model: [tr.bistable, tr.pulse]
    currentIndex: device.external_contact_alarm_mode - 1
}