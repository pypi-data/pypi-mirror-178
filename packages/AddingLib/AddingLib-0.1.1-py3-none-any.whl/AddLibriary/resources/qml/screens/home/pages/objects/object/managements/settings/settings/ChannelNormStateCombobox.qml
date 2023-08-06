import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.contact_state
    model: [tr.normally_open, tr.normally_closed]
    currentIndex: {
        if ([1, 2].includes(device.channel_normal_state)) {
            return device.channel_normal_state - 1
        }
        return - 1
    }
}