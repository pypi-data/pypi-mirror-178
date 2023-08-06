import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            pulseDuration.currentIndex,
            batteryChargeTracking.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "pulse_length": pulseDuration.currentIndex,
                "battery_charge_tracking": batteryChargeTracking.checked,
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.PulseDuration { id: pulseDuration }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.BatteryChargeTracking { id: batteryChargeTracking }
        }

        DS3.Comment {
            width: parent.width

            text: tr.battery_charge_tracking_info
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            Parts.TestSignalLevelNav {}
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}