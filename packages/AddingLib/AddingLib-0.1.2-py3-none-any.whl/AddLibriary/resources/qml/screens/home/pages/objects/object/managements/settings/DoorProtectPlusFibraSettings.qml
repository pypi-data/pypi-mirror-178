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
            shockSensor.checked,
            sensitivityCombobox.currentIndex,
            simpleImpact.checked,
            tiltSensor.checked,
            accelTiltCombobox.currentIndex,
            tiltAlarmDelayCombobox.currentIndex,
            alwaysActive.checked,
            partialArm.checked,
            indicatorLightMode.checked,
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            applyTimeoutsToPerimeterField.checked,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            ifExternalSensor.checked,
            ifTiltSensor.checked,
            ifShockSensor.checked,
            extraContactTypeCombobox.currentIndex,
            countPeriodCombobox.currentText,
            countTresholdCombobox.currentText,
            ifRSSensor.checked,
            ifMainSensor.checked,
            ifRSLostSensor.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                    "night_mode_arm": partialArm.checked,
                    "indicator_light_mode": indicatorLightMode.checked + 1,
                },
                "reed_contact_aware": mainSensor.checked,
                "extra_contact_aware": externalContact.checked,
                "shock_sensor_aware": shockSensor.checked,
                "ignore_simple_impact": simpleImpact.checked,
                "accelerometer_aware": tiltSensor.checked,
                "accelerometer_tilt_degrees": parseInt(accelTiltCombobox.currentIndex) + 1,
                "accelerometer_tilt_alarm_delay_seconds": parseInt(tiltAlarmDelayCombobox.currentIndex) + 1,
                "always_active": alwaysActive.checked,
                "siren_triggers": ifMainSensor.checked ? [1] : [],
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (sensitivityCombobox.currentIndex == 2) {
                settings["shock_sensor_sensitivity"] = parseInt(7)
            } else if (sensitivityCombobox.currentIndex == 1) {
                settings["shock_sensor_sensitivity"] = parseInt(4)
            } else {
                settings["shock_sensor_sensitivity"] = parseInt(0)
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

            if (ifExternalSensor.checked) {
                settings["siren_triggers"].push(2)
            }
            if (ifTiltSensor.checked) {
                settings["siren_triggers"].push(3)
            }
            if (ifShockSensor.checked) {
                settings["siren_triggers"].push(4)
            }

            if (device.roller_shutter_available) {
                settings["extra_contact_type"] = parseInt(extraContactTypeCombobox.currentIndex) + 1
                settings["roller_shutter_settings"] = {
                    "count_period": parseInt(countPeriodCombobox.currentText),
                    "count_threshold": parseInt(countTresholdCombobox.currentText),
                }

                if (ifRSSensor.checked) {
                    settings["siren_triggers"].push(5)
                }
                if (ifRSLostSensor.checked) {
                    settings["siren_triggers"].push(6)
                }
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

                Settings.IndicatorLightMode { id: indicatorLightMode }
                Settings.MainSensor{ id: mainSensor }
                Settings.ExternalContact{ id: externalContact }
                Settings.AlwaysActive { id: alwaysActive }
                Settings.ExtraContactTypeCombobox { id: extraContactTypeCombobox }
                Settings.CountPeriodCombobox { id: countPeriodCombobox }
                Settings.CountTresholdCombobox { id: countTresholdCombobox }
                Settings.ShockSensor { id: shockSensor }
                Settings.SensitivityCombobox { id: sensitivityCombobox }
                Settings.SimpleImpact { id: simpleImpact }
                Settings.TiltSensor { id: tiltSensor }
                Settings.AccelTiltCombobox { id: accelTiltCombobox }
                Settings.TiltAlarmDelayCombobox { id: tiltAlarmDelayCombobox }
            }


            DS3.Spacing {
                height: alertWithSiren.visible ? 24 : 0
            }

            Settings.AlertWithSiren {
                id: alertWithSiren

                visible: (
                    ifMainSensor.visible || ifExternalSensor.visible ||
                    ifRSSensor.visible || ifRSLostSensor.visible ||
                    ifShockSensor.visible || ifTiltSensor.visible)
            }

            DS3.SettingsContainer {
                Settings.IfMainSensor { id: ifMainSensor }
                Settings.IfExternalSensor {
                    id: ifExternalSensor

                    visible: devEnable && externalContact.checked && extraContactTypeCombobox.currentIndex != 1
                }
                Settings.IfRSSensor { id: ifRSSensor }
                Settings.IfRSLostSensor { id: ifRSLostSensor }
                Settings.IfShockSensor { id: ifShockSensor }
                Settings.IfTiltSensor { id: ifTiltSensor }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Settings.Chimes {
                    id: chimesItem

                    isExternalContactChecked: externalContact.checked && extraContactTypeCombobox.currentIndex != 1
                }
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

                Parts.TestSignalLevelNav {
                    title: tr.fibra_signal_strength_test
                    icon: "qrc:resources/images/Athena/settings_icons/FibraSettings-L.svg"
                }
                Parts.TestZoneNav {}
            }
            Parts.ManualNav {}
            Parts.BypassButtonNav {}
        }
    }
}