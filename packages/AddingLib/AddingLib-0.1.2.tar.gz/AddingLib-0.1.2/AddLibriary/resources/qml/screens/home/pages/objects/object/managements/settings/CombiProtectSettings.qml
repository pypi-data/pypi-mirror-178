import QtQuick 2.12

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3

Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            lightIndication.checked,
            partialArm.checked,
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            applyTimeoutsToPerimeterField.checked,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            motionSensor.checked,
            motionSensitivityCombobox.currentIndex,
            motionAlwaysActive.checked,
            gbSensor.checked,
            gbSensitivityCombobox.currentIndex,
            gbAlwaysActive.checked,
            ifMotionSensor.checked,
            ifGbSensor.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                    "night_mode_arm": partialArm.checked,
                    "indicator_light_mode": lightIndication.checked ? "STANDARD" : "DONT_BLINK_ON_ALARM",
                },
                "motion_sensor_aware": motionSensor.checked,
                "motion_sensitivity": motionSensitivityCombobox.currentIndex,
                "motion_sensor_always_active": motionAlwaysActive.checked,
                "glass_break_sensor_aware": gbSensor.checked,
                "glass_break_sensitivity": gbSensitivityCombobox.currentIndex,
                "glass_break_sensor_always_active": gbAlwaysActive.checked,
                "siren_triggers": ifMotionSensor.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (hub.is_arm_alarm_delays_available) {
                settings["common_part"]["alarm_delay_seconds"] = alarmDelaySeconds.value
                settings["common_part"]["arm_delay_seconds"] = armDelaySeconds.value
            }

            if (hub.firmware_version_dec >= 206000 && hub.firmware_version_dec < 211100) {
                settings["common_part"]["apply_delays_to_night_mode"] = applyTimeoutsToPerimeterField.checked
            }

            if (hub.firmware_version_dec >= 211100) {
                settings["common_part"]["perimeter_alarm_delay_seconds"] = perimeterAlarmDelaySeconds.value
                settings["common_part"]["perimeter_arm_delay_seconds"] = perimeterArmDelaySeconds.value
            }

            if (ifGbSensor.checked) {
                settings["siren_triggers"].push(2)
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        DS3.SettingsContainer {
            enabled: devEnable

            Settings.AlarmDelaySeconds { id: alarmDelaySeconds }
            Settings.ArmDelaySeconds { id: armDelaySeconds }
            Settings.PartialArm { id: partialArm }
            Settings.ApplyTimeoutsToPerimeter { id: applyTimeoutsToPerimeterField }
            Settings.PerimeterAlarmDelaySecondsNightMode { id: perimeterAlarmDelaySeconds }
            Settings.PerimeterArmDelaySecondsNightMode { id: perimeterArmDelaySeconds }
            Settings.LightIndication { id: lightIndication }
            Settings.MotionSensor { id: motionSensor }
            Settings.MotionSensitivityCombobox {
                id: motionSensitivityCombobox

                currentIndex: device.motion_sensitivity
                visible: hub.online && device.online && motionSensor.checked
            }
            Settings.MotionAlwaysActive { id: motionAlwaysActive }
            Settings.GbSensor { id: gbSensor }
            Settings.GbSensitivityCombobox { id: gbSensitivityCombobox }
            Settings.GbAlwaysActive { id: gbAlwaysActive }
        }

        DS3.Spacing {
            height: 24
        }
        Column {
            width: parent.width

            visible: motionSensor.checked || gbSensor.checked

            Settings.AlertWithSiren {}
            DS3.SettingsContainer {
                id: ifMotionGBSensorsContainer

                enabled: devEnable

                Settings.IfMotionSensor {
                    id: ifMotionSensor

                    visible: motionSensor.checked
                }
                Settings.IfGbSensor { id: ifGbSensor }
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
                Parts.TestZoneNav {}
                Parts.TestSignalLostNav {}
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}