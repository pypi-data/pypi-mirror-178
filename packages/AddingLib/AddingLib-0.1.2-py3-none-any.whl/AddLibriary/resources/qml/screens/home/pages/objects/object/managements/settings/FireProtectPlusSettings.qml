import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            highTemperatureAlarm.checked,
            rapidTemperatureRiseAlarm.checked,
            alarmCoEnabled.checked,
            ifTemperatureAlarm.checked,
            ifRapidTemperatureRiseAlarm.checked,
            ifSmokeAlarm.checked,
            ifCOAlarm.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "high_temperature_alarms_enabled": highTemperatureAlarm.checked,
                "temperature_diff_detection_enabled": rapidTemperatureRiseAlarm.visible && rapidTemperatureRiseAlarm.checked,
                "co_alarms_enabled": alarmCoEnabled.checked,
                "siren_triggers": ifTemperatureAlarm.visible && ifTemperatureAlarm.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (ifRapidTemperatureRiseAlarm.visible && ifRapidTemperatureRiseAlarm.checked) {
                settings["siren_triggers"].push(2)
            }
            if (ifSmokeAlarm.checked) {
                settings["siren_triggers"].push(3)
            }
            if (ifCOAlarm.checked) {
                settings["siren_triggers"].push(4)
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }
        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.HighTemperatureAlarm {id: highTemperatureAlarm}
                Settings.RapidTemperatureRiseAlarm { id: rapidTemperatureRiseAlarm }
                Settings.AlarmCoEnabled { id: alarmCoEnabled}
            }

            DS3.Spacing {
                height: 24
            }

            Settings.AlertWithSiren {}

            DS3.SettingsContainer {
                Settings.IfTemperatureAlarm { id: ifTemperatureAlarm }
                Settings.IfRapidTemperatureRiseAlarm { id: ifRapidTemperatureRiseAlarm }
                Settings.IfSmokeAlarm { id: ifSmokeAlarm }
                Settings.IfCOAlarm { id: ifCOAlarm }
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