import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    model: [tr.negative_trip, tr.positive_trip]
    atomTitle.title: tr.connection_type
    currentIndex: device._get_int_connection_type(output_number - 1) - 1
    enabled: devEnable
}
