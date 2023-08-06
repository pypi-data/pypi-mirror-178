import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: {
            let values = [
                groupAssociatedCombobox.currentIndex,
                deviceTypeCombobox.currentIndex,
            ]
            if (deviceTypeCombobox.currentIndex == 0) {
                values.push(accessProfileCombobox.currentIndex)
                if (blocking.checked) values.push(blockTimeSlider.value)
            }
            return values
        }
        generateSettings: () => {
            var settings = {
                "name": {"name": deviceName.atomInput.text.trim()},
                "device_type": deviceTypeCombobox.currentIndex + 1,
            }

            if (roomsCombobox.currentIndex >= 0) {
                settings["room_id"] = rooms.get_room(roomsCombobox.currentIndex).id
            }

            if (hub.firmware_version_dec >= 206000) {
                if (hub.groups_enabled) {
                    if (groupAssociatedCombobox.currentIndex == 0) {
                        settings["associated_group_id"] = "00000000"
                    } else {
                        var group = groups.get(groupAssociatedCombobox.currentIndex - 1)
                        if (group) {
                            settings["associated_group_id"] = group.group_id
                        }
                    }
                }
                if (deviceTypeCombobox.currentIndex == 0) {
                    if (accessProfileCombobox.currentIndex == 2) {
                        settings["access_profiles"] = [1, 2]
                    } else if (accessProfileCombobox.currentIndex == 1) {
                        settings["access_profiles"] = [2]
                    } else if (accessProfileCombobox.currentIndex == 0) {
                        settings["access_profiles"] = [1]
                    }
                }
            }

            if (deviceTypeCombobox.currentIndex == 0) {
                settings["blocking_enabled"] = blocking.checked
                settings["time_to_block_on_multiple_password_failures_minutes"] = blockTimeSlider.value
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.GroupAssociatedCombobox { id: groupAssociatedCombobox }
            Settings.AccessControlTypeCombobox { id: deviceTypeCombobox }
            Settings.AccessProfileCombobox {
                id: accessProfileCombobox

                visible: deviceTypeCombobox.currentIndex == 0 && hub.firmware_version_dec >= 206000
            }
            Settings.Password {
                id: password

                visible: deviceTypeCombobox.currentIndex == 0
            }
            Settings.DuressPassword {
                id: duress_password

                visible: deviceTypeCombobox.currentIndex == 0
            }
            Settings.Blocking {
                id: blocking

                visible: deviceTypeCombobox.currentIndex == 0
            }
            Settings.BlockTimeSlider { id: blockTimeSlider }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            Parts.BypassButtonNav {}
        }
    }
}