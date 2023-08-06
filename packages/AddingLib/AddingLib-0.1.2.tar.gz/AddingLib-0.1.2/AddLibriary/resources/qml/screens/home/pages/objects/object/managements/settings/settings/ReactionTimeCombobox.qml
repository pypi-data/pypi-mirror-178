import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.reaction_time_kind
    model: ["20 " + tr.time_value_ms, "100 " + tr.time_value_ms, "1 " + tr.sec]
    currentIndex: device.reaction_time - 1
}