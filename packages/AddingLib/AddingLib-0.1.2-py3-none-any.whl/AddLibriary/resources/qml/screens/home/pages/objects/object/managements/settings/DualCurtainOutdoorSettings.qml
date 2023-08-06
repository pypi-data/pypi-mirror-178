import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    property var deviceViewName: null
    Parts.CommonSettings {
        settingsForChangesChecker: [
            partialArm.checked,
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            applyTimeoutsToPerimeterField.checked,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            lightIndication.checked,
            ifMotionSensorLeft.checked,
            ifAntimaskingSensorLeft.checked,
            ifMotionSensorRight.checked,
            ifAntimaskingSensorRight.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                    "night_mode_arm": partialArm.checked,
                    "indicator_light_mode": lightIndication.checked ? "STANDARD" : "DONT_BLINK_ON_ALARM",
                },
                "siren_triggers": [],
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

            if (ifMotionSensorLeft.checked) {
                settings["siren_triggers"].push(1)
            }
            if (ifAntimaskingSensorLeft.checked) {
                settings["siren_triggers"].push(3)
            }
            if (ifMotionSensorRight.checked) {
                settings["siren_triggers"].push(2)
            }
            if (ifAntimaskingSensorRight.checked) {
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
                Settings.AlarmDelaySeconds { id: alarmDelaySeconds }
                Settings.ArmDelaySeconds { id: armDelaySeconds }
                Settings.PartialArm { id: partialArm }
                Settings.ApplyTimeoutsToPerimeter { id: applyTimeoutsToPerimeterField }
                Settings.PerimeterAlarmDelaySecondsNightMode { id: perimeterAlarmDelaySeconds }
                Settings.PerimeterArmDelaySecondsNightMode { id: perimeterArmDelaySeconds }
                Settings.LightIndication { id: lightIndication }
            }

            DS3.Spacing {
                height: 24
            }

            DS3.TitleSection {
                text: tr.sensor_settings
                isCaps: true
                forceTextToLeft: true
                isBgTransparent: true
            }

            DS3.SettingsContainer {
                DS3.SettingsNavigationTitlePrimary {
                    title: tr.left_side

                    onEntered: {
                        setChild(
                            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/DcoSensorStep.qml",
                             {"isLeft": true}
                         )
                    }
                }

                DS3.SettingsNavigationTitlePrimary {
                    title: tr.right_side

                    onEntered: {
                        setChild(
                            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/DcoSensorStep.qml",
                             {"isLeft": false}
                         )
                    }
                }
            }

            DS3.Spacing {
                height: alertWithSiren.visible ? 24 : 0
            }

            Settings.AlertWithSiren {
                id: alertWithSiren

                visible: ifMotionSensorLeft.visible || ifAntimaskingSensorLeft.visible || ifMotionSensorRight.visible || ifAntimaskingSensorRight.visible
            }

            DS3.SettingsContainer {
                Settings.IfMotionSensorLeft { id: ifMotionSensorLeft }
                Settings.IfAntimaskingSensorLeft { id: ifAntimaskingSensorLeft }
                Settings.IfMotionSensorRight { id: ifMotionSensorRight }
                Settings.IfAntimaskingSensorRight { id: ifAntimaskingSensorRight }
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