import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            ifTemperatureAlarm.checked,
            ifRapidTemperatureRiseAlarm.checked,
            ifSmokeAlarm.checked,
            ifCOAlarm.checked,
        ]
        generateSettings: () => {
            var subtypeLower = device.subtype.toLowerCase()

            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                }
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }
            settings[subtypeLower] = {}
            settings[subtypeLower]["siren_triggers"] = ifTemperatureAlarm.checked ? [1] : []
            if (ifRapidTemperatureRiseAlarm.checked) {
                settings[subtypeLower]["siren_triggers"].push(2)
            }
            if (ifSmokeAlarm.checked) {
                settings[subtypeLower]["siren_triggers"].push(3)
            }
            if (ifCOAlarm.visible &&  ifCOAlarm.checked) {
                settings[subtypeLower]["siren_triggers"].push(4)
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }
        Column {
            width: parent.width

            enabled: devEnable

            Settings.AlertWithSiren {}

            DS3.SettingsContainer {
                Settings.IfTemperatureAlarm {
                    id: ifTemperatureAlarm

                    visible: true
                }
                Settings.IfRapidTemperatureRiseAlarm {
                    id: ifRapidTemperatureRiseAlarm

                    visible: true
                }
                Settings.IfSmokeAlarm {
                    id: ifSmokeAlarm

                }
                Settings.IfCOAlarm {
                    id: ifCOAlarm

                    visible: ["FIRE_PROTECT2_PLUS", "FIRE_PROTECT2_PLUS_SB"].includes(device.subtype)
                }
            }

            DS3.Spacing {
                height: 24
            }
        }

        DS3.SettingsContainer {
            Column {
                width: parent.width

                enabled: devEnable
                spacing: 1

                Parts.TestSignalLevelNav {}
                Parts.TestFireNav { id: testFireNav }
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}