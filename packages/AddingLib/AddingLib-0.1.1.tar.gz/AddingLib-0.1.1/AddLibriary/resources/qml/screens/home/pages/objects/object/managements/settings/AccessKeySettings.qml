import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        roomsCombobox.visible: false

        settingsForChangesChecker: [
            userAssociatedCombobox.currentIndex,
            groupAssociatedCombobox.currentIndex
        ]

        generateSettings: () => {
            var settings = {
                "name": {"name": deviceName.atomInput.text.trim()},
            }

            if (hub.firmware_version_dec >= 206000) {
                if (hub.groups_enabled) {
                    var i = groupAssociatedCombobox.currentIndex
                    if (i == 0) {
                        settings["associated_group_id"] = "00000000"
                    } else {
                        var group = groups.get(groupAssociatedCombobox.currentIndex - 1)
                        if (group) {
                            settings["associated_group_id"] = group.group_id
                        }
                    }
                }
            }
            if (hub.firmware_version_dec >= 207000 || (hub.firmware_version_dec >= 206000 && hub.groups_enabled)) {
                var i = userAssociatedCombobox.currentIndex
                if (i == 0) {
                    settings["associated_user_id"] = "00000000"
                } else {
                    settings["associated_user_id"] = users.normalized_users.user_ids[userAssociatedCombobox.currentIndex - 1]
                }
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.GroupAssociatedCombobox {
                id: groupAssociatedCombobox
            }

            Settings.UserAssociated {
                id: userAssociatedCombobox
            }

            DS3.InputSingleLine {
                atomInput {
                    label: tr.accessKeyId
                    text: device.access_key_id
                    readOnly: true
                }
            }
        }
    }
}
