import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        settingsForChangesChecker: typeCombobox.currentIndex == 0 ? [
            typeCombobox.currentIndex,
            partialArm.checked,
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            applyTimeoutsToPerimeterField.checked,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            alwaysActive.checked,
            extContactModeCombobox.currentIndex,
            extContactAlarmModeCombobox.currentIndex,
            ifAlarmSensor.checked,
            ifShortCircuit.checked
        ] : [typeCombobox.currentIndex]

        generateSettings: () => {
            var settings = {
                "name": {"name": deviceName.atomInput.text.trim()},
                "wire_input_type": typeCombobox.currentIndex + 1,
            }

            if (roomsCombobox.currentIndex >= 0) {
                settings["room_id"] = rooms.get_room(roomsCombobox.currentIndex).id
            }

            if (typeCombobox.currentIndex == 0) {
                settings["night_mode_arm"] = partialArm.checked
                if (hub.firmware_version_dec >= 206000 && hub.firmware_version_dec < 211100) {
                    settings["alarm_delay_seconds"] = alarmDelaySeconds.value
                    settings["arm_delay_seconds"] = armDelaySeconds.value
                    settings["apply_delays_to_night_mode"] = applyTimeoutsToPerimeterField.checked
                }
                if (hub.firmware_version_dec >= 211100) {
                    settings["alarm_delay_seconds"] = alarmDelaySeconds.value
                    settings["arm_delay_seconds"] = armDelaySeconds.value
                    settings["perimeter_alarm_delay_seconds"] = perimeterAlarmDelaySeconds.value
                    settings["perimeter_arm_delay_seconds"] = perimeterArmDelaySeconds.value
                }
                if (hub.chimes_available) {
                    settings["chime_triggers"] = chimesItem.chimeTriggers
                    settings["chime_signal"] = chimesItem.chimeSignal
                }
                settings["external_contact_always_active"] = alwaysActive.checked
                settings["external_contact_mode"] = extContactModeCombobox.currentIndex + 2
                settings["external_contact_alarm_mode"] = extContactAlarmModeCombobox.currentIndex + 1

                settings["siren_triggers"] = []
                if (ifAlarmSensor.checked) {settings["siren_triggers"].push(1)}
                if (ifShortCircuit.checked) {settings["siren_triggers"].push(2)}
            }

            // Temporary solution for backward compatibility
            settings["_refactored"] = true

            return settings
        }

        Column {
            width: parent.width

            enabled: devEnable

            DS3.SettingsContainer {
                Settings.WireInputTypeCombobox {
                    id: typeCombobox
                }

                Column {
                    width: parent.width

                    visible: typeCombobox.currentIndex == 0
                    spacing: 1

                    Settings.AlarmDelaySeconds { id: alarmDelaySeconds }
                    Settings.ArmDelaySeconds { id: armDelaySeconds }
                    Settings.PartialArm { id: partialArm }
                    Settings.ApplyTimeoutsToPerimeter {
                        id: applyTimeoutsToPerimeterField

                        visible: hub.firmware_version_dec >= 206000 && hub.firmware_version_dec < 211100
                    }
                    Settings.PerimeterAlarmDelaySecondsNightMode { id: perimeterAlarmDelaySeconds }
                    Settings.PerimeterArmDelaySecondsNightMode { id: perimeterArmDelaySeconds }
                    Settings.ExternalContactModeComboboxWireInput { id: extContactModeCombobox }
                    Settings.ExternalDetectorTypeCombobox { id: extContactAlarmModeCombobox }
                    Settings.AlwaysActive { id: alwaysActive }
                }
            }

            DS3.Spacing {
                height: 24
            }

            Column {
                id: alertWithSirenSection

                width: parent.width

                visible: typeCombobox.currentIndex == 0

                Settings.AlertWithSiren {}

                DS3.SettingsContainer {
                    Settings.IfAlarmSensor {
                        id: ifAlarmSensor
                    }
                    Settings.IfShortCircuitWireInputs {
                        id: ifShortCircuit
                    }
                }

                DS3.Spacing {
                    height: 24
                }
            }

            Column {
                id: chimesSection

                width: parent.width

                visible: visibleChildren

                DS3.SettingsContainer {
                    Settings.Chimes {
                        id: chimesItem

                        visibilityCondition: typeCombobox.currentIndex == 0
                        isMainSensorChecked: false
                        isExternalContactChecked: extContactAlarmModeCombobox.currentIndex == 0
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
        }

        DS3.SettingsContainer {
            Parts.BypassButtonNav {}
        }
    }
}