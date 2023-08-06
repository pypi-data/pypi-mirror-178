import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
    title: tr.get_notified_if_moved_lq
    checked: device.is_acceleration_aware
}
