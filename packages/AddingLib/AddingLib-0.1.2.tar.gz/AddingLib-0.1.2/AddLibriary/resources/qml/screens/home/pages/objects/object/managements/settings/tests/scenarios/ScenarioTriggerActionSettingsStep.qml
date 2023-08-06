import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups


DS3Popups.PopupStep {
    readonly property var inScenarioKey: ["LIGHT_SWITCH_CHANNEL1", "LIGHT_SWITCH_CHANNEL2"]
    readonly property var selectedDevicesHasImpulseType: Object.keys(selectedDevices).map(id => (
        selectedDevices[id].device.lockup_relay_mode == 2 && (
            !selectedDevices[id].device.hasOwnProperty("pulse_mode_contact_normal_available")
            || !!selectedDevices[id].device.pulse_mode_contact_normal_available
        )
    ))
    readonly property bool allSelectedDevicesHaveImpulseType: selectedDevicesHasImpulseType.every(d => d)
    readonly property bool anySelectedDevicesHasImpulseType: selectedDevicesHasImpulseType.some(d => d)
    readonly property var selectedTargetActions: Object.keys(selectedDevices).map(id => ({
        checked: ["00"],
        id: id,
        type: selectedDevices[id].device.obj_type,
        selected_buttons: selectedDevices[id].selected_buttons
    }))

    height: maxStepHeight

    title: tr.scenario_settings
    sidePadding: 24

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.InputSingleLine {
            id: nameInput

            atomInput {
                label: tr.name
                placeholderText: tr.scenario_name_placeholder
                maxByteLength: 24
                text: !!scenario ? scenario.scenario_name : ""
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.TitleSection {
        text: tr.scenario_action
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
    }

    DS3.SettingsContainer {
        id: targetDeviceAction

        property int selectedIndex: allSelectedDevicesHaveImpulseType ? 0 : ({
            ON: 0,
            2: 0,
            OFF: 1,
            1: 1,
            STATE_CHANGE: 2,
            CHANGE_STAGE: 2,
            3: 2,
        }[!!scenario ? scenario.target_action : 2])

        width: parent.width

        Repeater {
            id: deviceActionModel

            model: {
                if (allSelectedDevicesHaveImpulseType) return [tr.scenario_action_pulse]

                let states = [tr.scenario_action_ON, tr.scenario_action_OFF]

                if (hub.firmware_version_dec < 209102) return states

                states.push(tr.scenario_action_SWITCH)
                return states
            }

            DS3.SettingsSingleSelection {
                atomTitle.title: modelData
                checked: index == targetDeviceAction.selectedIndex
                enabled: deviceActionModel.count > 1
                switchChecked: () => targetDeviceAction.selectedIndex = index
            }
        }
    }

    DS3.Comment {
        width: parent.width

        text: allSelectedDevicesHaveImpulseType ? tr.scenario_action_pulse_desc : tr.scenario_action_desc
    }

    DS3.Spacing {
        height: 24
    }

    Column {
        width: parent.width

        DS3.SettingsContainer {
            width: parent.width

            DS3.CommentImportant {
                visible: targetDeviceAction.selectedIndex == 1 && anySelectedDevicesHasImpulseType

                atomTitle {
                    title: tr.information
                    subtitle: tr.smart_button_pulse_relay_warning
                }
                status: DS3.CommentImportant.Status.Attention
            }
        }

        DS3.Spacing {
            height: 24
        }
    }

    DS3.SettingsContainer {
        width: parent.width

        visible: !!scenario

        DS3.ButtonRow {
            isDanger: true
            text: tr.delete

            onClicked: deleteScenario(scenario)
        }
    }

    DS3.Spacing {
        height: 24

        visible: !!scenario
    }

    footer: DS3.ButtonBar {
        hasBackground: true
        enabled: !!nameInput.atomInput.text.trim()
        button {
            text: tr.save_scenario
            onClicked: {
                var scenarioSettings = {}
                scenarioSettings["name"] = {"name": nameInput.atomInput.text.trim(), "alias": ""}
                scenarioSettings["source_type"] = (
                    isButton && 3
                    || isLightSwitch && 4
                    || 5
                )
                let thresholds = []

                if (isButton) {
                    if (selectedTriggerType == 0) {
                        scenarioSettings["alarm_source"] = "21"
                    } else {
                        scenarioSettings["alarm_source"] = "22"
                    }
                } else if (isLightSwitch) {
                    if (selectedTriggerType == 0) {
                        scenarioSettings["alarm_source"] = selectedButtonIndex == 0 ? "3b" : "3d"
                    } else {
                        scenarioSettings["alarm_source"] = selectedButtonIndex == 0 ? "3c" : "3e"
                    }
                } else if (selectedUiScenarioType == "THRESHOLD") {
                    scenarioSettings["threshold"] = {
                        "value": selectedValue,
                        "condition": conditionIndex,
                        "source_param": selectedIndicatorIndex + 68,
                    }
                    thresholds = [{"device": device}]
                }

                if (allSelectedDevicesHaveImpulseType) {
                    scenarioSettings["target_action"] = 2
                } else {
                    if (targetDeviceAction.selectedIndex == 0) {
                        scenarioSettings["target_action"] = 2
                    } else if (targetDeviceAction.selectedIndex == 1) {
                        scenarioSettings["target_action"] = 1
                    } else if (targetDeviceAction.selectedIndex == 2) {
                        scenarioSettings["target_action"] = 3
                    } else {
                        scenarioSettings["target_action"] = 1
                    }
                }

                // To chose channel of LS
                let ls_channels = []
                if (isLightSwitch) {
                    let channel_name = inScenarioKey[selectedButtonIndex]
                    ls_channels.push(isLSTwoGang ? channel_name : "LIGHT_SWITCH_CHANNEL1")
                }

                saveTriggerScenario(scenario, scenarioSettings, selectedTargetActions, ls_channels, thresholds)
            }
        }
    }
}
