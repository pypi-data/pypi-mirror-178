import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    atomTitle.title: tr.room
    model: rooms.room_names
    currentIndex: {
        if (device.room_id == undefined || device.room_id_bound == undefined) return 0
        if (device.obj_type == "2e") return 0
        return rooms.get_index(device)
    }
}