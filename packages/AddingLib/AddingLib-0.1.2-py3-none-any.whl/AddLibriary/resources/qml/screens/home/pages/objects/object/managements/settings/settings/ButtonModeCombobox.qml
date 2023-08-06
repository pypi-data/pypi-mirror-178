import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    id: buttonModeCombobox

    visible: true
    atomTitle.title: tr.button_mode
    model: {
        if (__fp2_features__) return [tr.panic_button_enabled, tr.smart_button_enabled, tr.mute_fire_alarm_button]
        if (hub.firmware_version_dec >= 209100) return [tr.panic_button_enabled, tr.smart_button_enabled, tr.interconnect_delay_button_mode]
        return [tr.panic_button_enabled, tr.smart_button_enabled]
    }
    currentIndex: device.button_mode - 1
}
