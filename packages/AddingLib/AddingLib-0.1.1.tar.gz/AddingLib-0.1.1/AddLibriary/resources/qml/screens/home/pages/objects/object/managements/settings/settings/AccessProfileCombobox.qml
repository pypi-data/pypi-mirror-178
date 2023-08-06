import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: (hub.firmware_version_dec >= 206000)
    atomTitle.title: tr.access_profile
    model: [tr.using_keypad_password, tr.using_user_password, tr.using_keypad_or_user_password]
    currentIndex: {
        if (device.keypad_access_profile.includes(1) && device.keypad_access_profile.includes(2)) {
            return 2
        }
        if (device.keypad_access_profile.includes(2)) {
            return 1
        }
        if (device.keypad_access_profile.includes(1)) {
            return 0
        }
    }
}