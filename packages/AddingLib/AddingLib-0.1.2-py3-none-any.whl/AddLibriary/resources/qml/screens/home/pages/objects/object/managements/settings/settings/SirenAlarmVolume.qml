import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.siren_volume
    model: [tr.off, tr.volume_min, tr.volume_mid, tr.volume_max]
    currentIndex: device.siren_alarm_volume - 1
}
