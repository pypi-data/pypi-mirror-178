import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    model: {
        return device.mute_available ?
        [tr.volume_silent, tr.volume_min, tr.volume_mid, tr.volume_max] :
        [tr.volume_min, tr.volume_mid, tr.volume_max]
    }
    atomTitle.title: tr.siren_volume
    currentIndex: {
        var curIdx = 2
        if (device.volume == 32) {
            curIdx = -1
        } else if (device.volume == 29) {
            curIdx = 0
        } else if (device.volume == 18) {
            curIdx = 1
        }  else if (device.volume == 1) {
            curIdx = 2
        }
        return device.mute_available ? curIdx + 1 : curIdx
    }
}
