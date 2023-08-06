import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    readonly property var scenarioAlarmTriggers: Object.keys(alarmSources).map(deviceId => alarmSources[deviceId])

    height: maxStepHeight

    title: tr.scenario_type_alarm
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
                text: scenario ? scenario.scenario_name : ""
                maxByteLength: 24
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    Column {
        id: multipleDevicesTriggers

        width: parent.width

        visible: amountOfTriggers > 1

        DS3.TitleSection {
            text: tr.scenario_trigger_link
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
        }

        DS3.SettingsContainer {
            id: scenarioTriggers

            width: parent.width

            property int selectedIndex: !!scenario
                ? ({
                    OR: 0,
                    AND: 1
                }[scenario.source_condition])
                : 0

            Repeater {
                model: [tr.scenario_trigger_one_alarm, tr.scenario_trigger_all]

                DS3.SettingsSingleSelection {
                    atomTitle.title: modelData
                    checked: index == scenarioTriggers.selectedIndex
                    switchChecked: () => scenarioTriggers.selectedIndex = index
                }
            }
        }

        DS3.Comment {
            width: parent.width

            text: tr.scenario_trigger_link_desc
        }

        DS3.Spacing {
            height: 24
        }

        Column {
            width: parent.width

            visible: scenarioTriggers.selectedIndex == 1 && selectedUiScenarioType != "TEMPERATURE"

            DS3.TitleSection {
                text: tr.scenario_time_setting
                isCaps: true
                isBgTransparent: true
                forceTextToLeft: true
            }

            DS3.SettingsContainer {
                width: parent.width

                DS3.InputTime {
                    id: inputTime

                    time: !!scenario ? scenario.time_before_action : 180
                }
            }

            DS3.Spacing {
                height: 24
            }
        }
    }

    Column {
        width: parent.width

        visible: isLSTwoGang

        DS3.TitleSection {
            text: tr.button_title_scenario
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
        }

        DS3.SettingsContainer {
            id: actionButton

            property var inScenarioKey: ["LIGHT_SWITCH_CHANNEL1", "LIGHT_SWITCH_CHANNEL2"]

            property var selectedButtons: {
                if (!scenario) return []
                let buttons = []
                if (scenario.targets.map((target) => target.in_scenario_key).includes("LIGHT_SWITCH_CHANNEL1")) buttons.push("LIGHT_SWITCH_CHANNEL1")
                if (scenario.targets.map((target) => target.in_scenario_key).includes("LIGHT_SWITCH_CHANNEL2")) buttons.push("LIGHT_SWITCH_CHANNEL2")
                return buttons
            }


            width: parent.width

            Repeater {
                id: actionButtonModel

                model: isLSTwoGang ? [device.button1_name, device.button2_name] : []

                DS3.SettingsMultiSelection {
                    atomTitle.title: modelData
                    checked: actionButton.selectedButtons.includes(actionButton.inScenarioKey[index])

                    switchChecked: () => {
                        checked = !checked
                        let scenario_key = actionButton.inScenarioKey[index]
                        if (checked) {
                            actionButton.selectedButtons.push(scenario_key)
                        }
                        else {
                            let index = actionButton.selectedButtons.indexOf(scenario_key)
                            if (index !== -1) {
                                actionButton.selectedButtons.splice(index, 1)
                            }
                        }
                        actionButton.selectedButtonsChanged()
                    }
                }
            }
        }

        DS3.Comment {
            width: parent.width

            text: selectedUiScenarioType == "TEMPERATURE" ? tr.by_temperature_lightswitch_device_button : tr.select_buttons_alarm_scenario
        }

        DS3.Spacing {
            height: 24
        }
    }

    DS3.SettingsContainer {
        DS3.CommentImportant {

            visible: isFastPHOD
            atomTitle.subtitle: tr.scenario_condition_armed_source
        }
    }

    DS3.Spacing {
        height: 24

        visible: isFastPHOD
    }

    DS3.TitleSection {
        text: tr.scenario_action
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
    }

    DS3.SettingsContainer {
        id: deviceAction

        property int selectedIndex: isImpulseType || isPHOD ? 0 : ({
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

            model: deviceActionModelStates // todo: check if `!util.check_is_type_exists(collected, "42")` is necessary

            DS3.SettingsSingleSelection {
                atomTitle.title: modelData
                checked: index == deviceAction.selectedIndex
                enabled: deviceActionModel.count > 1
                switchChecked: () => deviceAction.selectedIndex = index
            }
        }
    }

    DS3.Comment {
        width: parent.width

        visible: !isFastPHOD
        text: {
            if (isImpulseType) return tr.scenario_action_pulse_desc
            return isPHOD ? tr.device_action_alarm_scenario : tr.scenario_action_desc
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        visible: !!scenario

        DS3.ButtonRow {
            isDanger: true
            text: tr.delete

            onClicked: Popups.popupByPath(
            "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
            {
                title: tr.delete_scenario_schedule,
                text: tr.confirm_deletion,
                firstButtonCallback: () => { deleteScenario(scenario) },
                isFirstButtonRed: true,
                firstButtonText: tr.delete,
                secondButtonText: tr.cancel,
                isVertical: true,
            })
        }
    }

    DS3.Spacing {
        height: 24

        visible: !!scenario
    }

    footer: DS3.ButtonBar {
        enabled: !!nameInput.atomInput.text.trim() && (!actionButton.visible || actionButton.selectedButtons.length != 0)
        hasBackground: true
        button {
            text: tr.save_scenario
            onClicked: {
                var scenarioSettings = {}
                scenarioSettings["name"] = {"name": nameInput.atomInput.text.trim(), "alias": ""}
                scenarioSettings["source_condition"] = scenarioTriggers.selectedIndex + 1
                if (isImpulseType) {
                    scenarioSettings["target_action"] = 3
                } else if (isPHOD) {
                    scenarioSettings["target_action"] = 8  // MAKE_PHOTO
                    scenarioSettings["target_condition"] = ["ON_DEVICE_ARM"]
                } else {
                    if (deviceAction.selectedIndex == 0) {
                        scenarioSettings["target_action"] = 2
                    } else if (deviceAction.selectedIndex == 1) {
                        scenarioSettings["target_action"] = 1
                    } else if (deviceAction.selectedIndex == 2) {
                        scenarioSettings["target_action"] = 3
                    } else {
                        scenarioSettings["target_action"] = 1
                    }
                }

                if (scenarioTriggers.selectedIndex == 1) {
                    scenarioSettings["time_before_action"] = inputTime.time
                }

                if (selectedUiScenarioType == "TEMPERATURE") {
                    scenarioSettings["source_type"] = 5
                    scenarioSettings["threshold"] = {
                        "value": selectedValue,
                        "condition": conditionIndex,
                        "source_param": 2,
                    }
                }

                // To chose channel of LS
                let ls_channels = []
                if (isLightSwitch) {
                    ls_channels = isLSTwoGang ? actionButton.selectedButtons : ["LIGHT_SWITCH_CHANNEL1"]
                }

                saveScenarioByAlarm(scenario, scenarioSettings, scenarioAlarmTriggers, ls_channels)
            }
        }
    }
}