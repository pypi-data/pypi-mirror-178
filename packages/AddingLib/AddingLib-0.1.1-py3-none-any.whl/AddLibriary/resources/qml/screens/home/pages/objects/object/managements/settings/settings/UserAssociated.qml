import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsPickerTitleSecondary {
    property bool isAssociatedUserRecentlyDeleted: users.normalized_users.user_ids.indexOf(device.associated_user_id) == -1
        && device.associated_user_id != '00000000'

    visible: hub.firmware_version_dec >= 207000 || (hub.firmware_version_dec >= 206000 && hub.groups_enabled)
    atomTitle.title: tr.userAssociated
    model: {
        var items = users.normalized_users.names
        if (isAssociatedUserRecentlyDeleted) {
            items.splice(0, 0, tr.user_was_deleted)
            return items
        }
        items.splice(0, 0, tr.not_assigned_user)
        return items
    }
    currentIndex: users.normalized_users.user_ids.indexOf(device.associated_user_id) + 1
}