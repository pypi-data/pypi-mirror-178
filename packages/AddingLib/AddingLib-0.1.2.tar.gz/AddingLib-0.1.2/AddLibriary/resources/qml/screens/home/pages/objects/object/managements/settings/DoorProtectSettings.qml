import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: [
            mainSensor.checked,
            externalContact.checked,
            alwaysActive.checked,
            partialArm.checked,
            lightIndication.checked,
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            applyTimeoutsToPerimeterField.checked,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            ifMainSensor.checked,
            ifExternalSensor.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                    "night_mode_arm": partialArm.checked,
                    "indicator_light_mode": lightIndication.checked ? "STANDARD" : "DONT_BLINK_ON_ALARM",
                },
                "reed_contact_aware": mainSensor.checked,
                "extra_contact_aware": externalContact.checked,
                "always_active": alwaysActive.checked,
                "siren_triggers": ifMainSensor.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                settings["common_part"]["room_id"] = rooms.get_room(roomsCombobox.currentIndex).id
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
            if (ifExternalSensor.checked) {
                settings["siren_triggers"].push(2)
            }
            if (hub.chimes_available) {
                settings["chime_triggers"] = chimesItem.chimeTriggers
                settings["chime_signal"] = chimesItem.chimeSignal
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.AlarmDelaySeconds { id: alarmDelaySeconds }
                Settings.ArmDelaySeconds { id: armDelaySeconds }
                Settings.PartialArm { id: partialArm }
                Settings.ApplyTimeoutsToPerimeter { id: applyTimeoutsToPerimeterField }
                Settings.PerimeterAlarmDelaySecondsNightMode { id: perimeterAlarmDelaySeconds }
                Settings.PerimeterArmDelaySecondsNightMode { id: perimeterArmDelaySeconds }

                Settings.LightIndication {
                    id: lightIndication
                    visible: device.indicator_light_mode_available
                }
                Settings.MainSensor{ id: mainSensor }
                Settings.ExternalContact{ id: externalContact }
                Settings.AlwaysActive { id: alwaysActive }
            }

            DS3.Spacing {
                height: alertWithSiren.visible ? 24 : 0
            }

            Settings.AlertWithSiren {
                id: alertWithSiren

                visible: ifMainSensor.visible || ifExternalSensor.visible
            }

            DS3.SettingsContainer {
                Settings.IfMainSensor { id: ifMainSensor }
                Settings.IfExternalSensor { id: ifExternalSensor }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                enabled: devEnable

                Settings.Chimes { id: chimesItem }
            }

            DS3.Comment {
                width: parent.width

                text: tr.chimes_device_settings_tip
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