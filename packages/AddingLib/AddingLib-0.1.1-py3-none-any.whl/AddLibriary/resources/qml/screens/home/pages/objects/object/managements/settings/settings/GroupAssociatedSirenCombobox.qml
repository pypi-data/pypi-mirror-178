import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    visible: hub.firmware_version_dec >= 206000 && hub.groups_enabled
    atomTitle.title: tr.group_associated_siren
    model: {
        var items = groups.group_names
        items.splice(0, 0, tr.not_assigned_siren)
        return items
    }
    currentIndex: groups.get_index_by_attr(device, "siren_associated_group_id") + 1
}
