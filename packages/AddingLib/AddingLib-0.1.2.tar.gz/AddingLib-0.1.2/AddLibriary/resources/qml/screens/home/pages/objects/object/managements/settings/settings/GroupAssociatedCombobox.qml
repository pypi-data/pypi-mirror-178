import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: hub.firmware_version_dec >= 206000 && hub.groups_enabled
    atomTitle.title: tr.groupAssociated
    model: {
        var items = groups.group_names
        items.splice(0, 0, tr.not_assigned)
        return items
    }
    currentIndex: groups.get_index(device) + 1
}