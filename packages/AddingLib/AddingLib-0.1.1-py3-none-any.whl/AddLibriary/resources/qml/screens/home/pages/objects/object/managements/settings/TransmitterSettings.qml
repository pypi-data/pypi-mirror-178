import QtQuick 2.12

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: {
            let values = [
                alarmDelaySeconds.value,
                armDelaySeconds.value,
                partialArm.checked,
                extPowerSupplyCombobox.currentIndex,
                externalContactStateCombobox.currentIndex,
                typeExternalContactCombobox.currentIndex,
                alarmTypeCombobox.currentIndex,
                tamperStateModeCombobox.currentIndex,
                moveSwitch.checked,
                alwaysActive.checked,
                ifAlarm.checked,
            ]

            if (partialArm.checked) values.push(
                applyTimeoutsToPerimeterField.checked,
                perimeterAlarmDelaySeconds.value,
                perimeterArmDelaySeconds.value,
            )

            if (moveSwitch.checked) values.push(ifAccelAlarm.checked)

            return values
        }
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                    "night_mode_arm": partialArm.checked,
                },
                "external_contact_state_mode": parseInt(externalContactStateCombobox.currentIndex) + 1,
                "external_contact_alarm_mode": parseInt(typeExternalContactCombobox.currentIndex) + 1,
                "external_device_tamper_state_mode": parseInt(tamperStateModeCombobox.currentIndex) + 1,
                "external_contact_always_active": alwaysActive.checked,
                "accelerometer_aware": moveSwitch.checked,
                "custom_alarm_type": alarmTypeCombobox.currentIndex < 5 ? alarmTypeCombobox.currentIndex + 1 : alarmTypeCombobox.currentIndex + 2,
                "external_device_power_supply_mode": parseInt(extPowerSupplyCombobox.currentIndex) + 1,
                "siren_triggers": ifAlarm.checked ? [1] : [],
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

            if (ifAccelAlarm.checked) {
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
                Settings.ExtPowerSupplyCombobox { id: extPowerSupplyCombobox }
                Settings.ExternalContactModeCombobox { id: externalContactStateCombobox }
                Settings.ExternalDetectorTypeCombobox { id: typeExternalContactCombobox }
                Settings.AlarmTypeCombobox { id: alarmTypeCombobox }
                Settings.TamperStateModeCombobox { id: tamperStateModeCombobox }
                Settings.MoveSwitch { id: moveSwitch }
                Settings.AlwaysActive { id: alwaysActive }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.TitleSection {
                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
                text: tr.alert_with_a_siren
            }

            DS3.SettingsContainer {
                Settings.IfAlarm { id: ifAlarm }
                Settings.IfAccelAlarm { id: ifAccelAlarm }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Settings.Chimes {
                    id: chimesItem

                    isMainSensorChecked: false
                    isExternalContactChecked: typeExternalContactCombobox.currentIndex == 0
                }
            }

            DS3.Comment {
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
                Parts.TestSignalLostNav {}
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}