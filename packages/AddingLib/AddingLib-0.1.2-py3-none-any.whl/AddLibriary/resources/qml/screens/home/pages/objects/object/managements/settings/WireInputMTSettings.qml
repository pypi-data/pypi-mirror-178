import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/" as Parts
import "qrc:/resources/qml/components/911/DS3" as DS3


Parts.DeviceSettings {
    Parts.CommonSettings {
        property var eventTypesWireMT: [
            'BURGLARY_ALARM','FIRE_ALARM','MEDICAL_ALARM',
            'PANIC_ALARM','GAS_ALARM','MALFUNCTION_ALARM',
            'LEAK_ALARM', 'SERVICE_EVENT'
        ]

        settingsForChangesChecker: [
            typeCombobox.currentIndex,
            alwaysActive.checked,
            partialArm.checked,
            applyTimeoutsToPerimeterField.checked,
            alarmDelaySeconds.value,
            armDelaySeconds.value,
            perimeterAlarmDelaySeconds.value,
            perimeterArmDelaySeconds.value,
            extContactModeCombobox.currentIndex,
            extContactAlarmModeCombobox.currentIndex,
            reactionTimeCombobox.currentIndex,
            inputResistanceCombobox.currentIndex,
            alarmTypeCombobox.currentIndex,
            ifAlarmSensor.checked,
            ifShortCircuit.checked
        ]
        generateSettings: () => {
            var settings = {
                "common_part": {
                    "name": {"name": deviceName.atomInput.text.trim()},
                },
                "input_type": typeCombobox.currentIndex + 1,
            }

            if (roomsCombobox.currentIndex >= 0) {
                var room = rooms.get_room(roomsCombobox.currentIndex)
                settings["common_part"]["room_id"] = room.id
            }

            if (typeCombobox.currentIndex == 0) {
                settings["alwaysActive"] = alwaysActive.checked
                settings["common_part"]["night_mode_arm"] = partialArm.checked
                settings["common_part"]["apply_delays_to_night_mode"] = applyTimeoutsToPerimeterField.checked

                settings["common_part"]["alarm_delay_seconds"] = alarmDelaySeconds.value
                settings["common_part"]["arm_delay_seconds"] = armDelaySeconds.value
                settings["common_part"]["perimeter_alarm_delay_seconds"] = perimeterAlarmDelaySeconds.value
                settings["common_part"]["perimeter_arm_delay_seconds"] = perimeterArmDelaySeconds.value

                settings["external_contact_mode"] = extContactModeCombobox.currentIndex + 2
                settings["external_contact_alarm_mode"] = extContactAlarmModeCombobox.currentIndex + 1
                settings["reaction_time"] = reactionTimeCombobox.currentIndex + 1
                settings["input_resistance"] = inputResistanceCombobox.currentIndex + 10 // min resistance value is 1.0 kOhm, it's refers to index 0

                if (device.custom_alarm_available_v2) {
                    settings["custom_alarm_S2"] = eventTypesWireMT[alarmTypeCombobox.currentIndex]
                } else {
                    settings["custom_alarm"] = alarmTypeCombobox.currentIndex + 1
                }

                settings["siren_triggers"] = []
                if (ifAlarmSensor.checked) {
                    settings["siren_triggers"].push(1)
                }
                if (ifShortCircuit.checked) {
                    settings["siren_triggers"].push(2)
                }

                if (hub.chimes_available) {
                    settings["chime_triggers"] = chimesItem.chimeTriggers
                    settings["chime_signal"] = chimesItem.chimeSignal
                }
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

                    currentIndex: device.input_type - 1
                }
                Settings.ExternalContactModeComboboxWireInput {
                    id: extContactModeCombobox

                    atomTitle.title: tr.device_work_mode
                }

                Column {
                    width: parent.width

                    visible: typeCombobox.currentIndex == 0
                    spacing: 1

                    Settings.AlarmTypeCombobox {
                        id: alarmTypeCombobox

                        visible: true
                        currentIndex: device.custom_alarm_available_v2 ? eventTypesWireMT.indexOf(device.custom_alarm_S2) : device.custom_alarm - 1
                        commentText: hub.firmware_version_dec >= 213000 ? tr.custom_event_descr : ""
                    }
                    Settings.ExternalDetectorTypeCombobox {
                        id: extContactAlarmModeCombobox

                        atomTitle.title: tr.operating_mode_wire_input
                    }
                    Settings.InputResistance {
                        id: inputResistanceCombobox

                        visible: extContactModeCombobox.currentIndex == 2 || extContactModeCombobox.currentIndex == 3
                        contentList.headerPositioning: ListView.OverlayHeader | ListView.InlineHeader
                        contentList.header: Rectangle {
                            id: header

                            width: visible ? parent.width - 2 : 0
                            height: visible ? textI.contentHeight + 12 : 0

                            color: ui.ds3.bg.highest
                            z: 10
                            visible: device.fact_resistance >= 1 && device.fact_resistance <= 7.5

                            DS3.Text {
                                id: textI

                                property var fact_res: `${tr.recommended_resistance_value} ${(device.fact_resistance).toFixed(1)} ${tr.resistance_value}`

                                width: parent.width - 24

                                anchors.horizontalCenter: parent.horizontalCenter
                                anchors.centerIn: parent

                                text: fact_res
                                style: ui.ds3.text.body.MRegular
                                hasElide: true
                                rightPadding: 30
                            }

                            DS3.MouseArea {
                                onEntered: {
                                    parent.color = ui.ds3.bg.high
                                }

                                onExited: {
                                    parent.color = ui.ds3.bg.highest
                                }

                                onClicked: {
                                    inputResistanceCombobox.currentIndex = inputResistanceCombobox.resistances.indexOf((device.fact_resistance).toFixed(1))
                                    inputResistanceCombobox.popup.close()
                                }
                            }
                        }
                    }
                    Settings.AlwaysActive { id: alwaysActive }
                    Settings.AlarmDelaySeconds { id: alarmDelaySeconds }
                    Settings.ArmDelaySeconds { id: armDelaySeconds }
                    Settings.PartialArm { id: partialArm }
                    Settings.ApplyTimeoutsToPerimeter { id: applyTimeoutsToPerimeterField }
                    Settings.PerimeterAlarmDelaySecondsNightMode { id: perimeterAlarmDelaySeconds }
                    Settings.PerimeterArmDelaySecondsNightMode { id: perimeterArmDelaySeconds }
                    Settings.ReactionTimeCombobox { id: reactionTimeCombobox }
                }
            }

            DS3.Spacing {
                height: ifAlarmSensor.visible || ifShortCircuit.visible ? 24 : 0
            }

            Settings.AlertWithSiren {
                visible: ifAlarmSensor.visible || ifShortCircuit.visible
            }

            DS3.SettingsContainer {
                Settings.IfAlarmSensor {
                    id: ifAlarmSensor

                    visible: typeCombobox.currentIndex == 0
                    checked: device.siren_triggers.includes("EXTRA_CONTACT_S2")
                }
                Settings.IfShortCircuitWireInputs {
                    id: ifShortCircuit

                    checked: device.siren_triggers.includes("SHORT_CIRCUIT")
                }
            }

            DS3.Spacing {
                height: chimesItem.visibilityCondition ? 24 : 0
            }

            DS3.SettingsContainer {
                Settings.Chimes {
                    id: chimesItem

                    visibilityCondition: typeCombobox.currentIndex == 0
                    isMainSensorChecked: false
                    isExternalContactChecked: typeCombobox.currentIndex == 0
                    isBistable: extContactAlarmModeCombobox.currentIndex == 0
                }
            }

            DS3.Comment {
                width: parent.width

                text: tr.chimes_device_settings_tip
                visible: chimesItem.visibilityCondition
            }

            DS3.Spacing {
                height: 24
            }

            DS3.SettingsContainer {
                Parts.BypassButtonNav {}
            }
        }
    }
}