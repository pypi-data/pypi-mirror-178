import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.wallswitch_mode
    model: [tr.bistable, tr.pulse]
    currentIndex: device.lockup_relay_mode - 1
}