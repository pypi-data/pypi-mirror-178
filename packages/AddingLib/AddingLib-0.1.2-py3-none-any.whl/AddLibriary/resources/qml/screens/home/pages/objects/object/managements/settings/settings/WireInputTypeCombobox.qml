import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.wire_input_type
    model: [tr.wire_input_type_sensor, tr.wire_input_type_tamper]
    currentIndex: device.wire_input_type - 1
}