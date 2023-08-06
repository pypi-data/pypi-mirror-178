import QtQuick 2.12

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            ifShortCircuit.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "siren_triggers": ifShortCircuit.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Settings.AlertWithSiren {}

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.IfShortCircuit { id:ifShortCircuit }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            Column {
                width: parent.width

                enabled: devEnable
                spacing: 1

                Parts.TestSignalLevelNav {}
                Parts.TestSignalLostNav {}
                Parts.ManualNav {}
                Parts.BypassButtonNav {}
            }
        }
    }
}
