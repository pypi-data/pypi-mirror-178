import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: device.blink_while_armed_and_max_volume_available
    model: [tr.off, tr.armed, tr.always_enable]
    atomTitle.title: tr.light_indication
    currentIndex: device.blink_while_armed - 1
}
