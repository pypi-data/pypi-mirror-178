import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            applyTimeoutsToPerimeterField.checked,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            partialArm.checked,
            motionSensitivityCombobox.currentIndex,
            alwaysActive.checked,
            indicatorLightMode.checked,
            ifMotionSensor.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                    "night_mode_arm": partialArm.checked,
                    "indicator_light_mode": indicatorLightMode.checked + 1,
                },
                "sensitivity": motionSensitivityCombobox.currentIndex,
                "always_active": alwaysActive.checked,
                "siren_triggers": ifMotionSensor.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (hub.is_arm_alarm_delays_available) {
                settings["common_part"]["alarm_delay_seconds"] =alarmDelaySeconds.value
                settings["common_part"]["arm_delay_seconds"] = armDelaySeconds.value
            }

            if (hub.firmware_version_dec >= 206000 && hub.firmware_version_dec < 211100) {
                settings["common_part"]["apply_delays_to_night_mode"] = applyTimeoutsToPerimeterField.checked
            }

            if (hub.firmware_version_dec >= 211100) {
                settings["common_part"]["perimeter_alarm_delay_seconds"] = perimeterAlarmDelaySeconds.value
                settings["common_part"]["perimeter_arm_delay_seconds"] = perimeterArmDelaySeconds.value
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        DS3.SettingsContainer {
            Settings.AlarmDelaySeconds { id: alarmDelaySeconds }
            Settings.ArmDelaySeconds { id: armDelaySeconds }
            Settings.PartialArm { id: partialArm }
            Settings.ApplyTimeoutsToPerimeter { id: applyTimeoutsToPerimeterField }
            Settings.PerimeterAlarmDelaySecondsNightMode { id: perimeterAlarmDelaySeconds }
            Settings.PerimeterArmDelaySecondsNightMode { id: perimeterArmDelaySeconds }

            Settings.IndicatorLightMode { id: indicatorLightMode }
            Settings.MotionSensitivityCombobox { id: motionSensitivityCombobox }
            Settings.AlwaysActive { id: alwaysActive }
        }

        DS3.Spacing {
            height: 24
        }

        Settings.AlertWithSiren {}

        DS3.SettingsContainer {
            Settings.IfMotionSensor { id: ifMotionSensor }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            Parts.TestSignalLevelNav {}
            Parts.TestZoneNav {}
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}