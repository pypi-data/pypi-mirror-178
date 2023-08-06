import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            groupAssociatedCombobox.currentIndex,
            alarmVolumeDurationSlider.value,
            beepsButton.hubCapability,
            beepsButton.beepWADV2,
            beepsButton.beepWADNV2,
            beepsButton.beepOnArmDelay,
            beepsButton.beepOnDisarmDelay,
            beepsButton.beepOnExitDelayInNightMode,
            beepsButton.beepOnEntryDelayInNightMode,
            beepsButton.beepOnArmDisarm,
            beepsButton.beepOnDelay
        ]
        generateSettings: () => {
            var settings = {
                "name": {"name": deviceName.atomInput.text.trim()},
                "alarm_duration": alarmVolumeDurationSlider.value,
            }

            if (roomsCombobox.currentIndex >= 0) {
                settings["room_id"] = rooms.get_room(roomsCombobox.currentIndex).id
            }

            if (hub.firmware_version_dec >= 206000 && hub.groups_enabled) {
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

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.GroupAssociatedComboboxSirens { id: groupAssociatedCombobox }
            Settings.AlarmVolumeDurationSlider { id: alarmVolumeDurationSlider }
            Parts.SirenBeepsButtonNav {id: beepsButton }
        }
    }
}
