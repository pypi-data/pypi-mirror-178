import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: device.false_press_filter_available
    atomTitle.title: tr.falsePressFilter
    model: [tr.off, tr.long_press, tr.double_press]
    currentIndex: device.false_press_filter - 1
}