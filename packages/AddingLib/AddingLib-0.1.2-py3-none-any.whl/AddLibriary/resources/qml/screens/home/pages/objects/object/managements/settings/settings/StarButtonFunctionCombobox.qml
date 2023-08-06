import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: hub.firmware_version_dec >= 206000
    atomTitle.title: tr.function_button
    model: __fp2_features__ ? [tr.off, tr.send_panic_alarm, tr.mute_fire_alarm_button] : [tr.off, tr.send_panic_alarm, tr.silence_fire_alarm]
    currentIndex: device.star_button_function - 1
}