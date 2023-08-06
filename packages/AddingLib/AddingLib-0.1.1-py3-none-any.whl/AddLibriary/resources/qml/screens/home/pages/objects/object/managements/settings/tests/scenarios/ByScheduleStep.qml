import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    property var scenario: null

    height: maxStepHeight

    title: tr.scenario_type_schedule
    sidePadding: 24

    DS3.Spacing {
        height: 24
    }

    Column {
        width: parent.width

        visible: isLSTwoWay && hub.device_type_counter(["44"], ["LIGHT_SWITCH_TWO_WAY"]) > 1

        DS3.SettingsContainer {
            DS3.CommentImportant {
                atomTitle {
                    title: tr.note_two_way_switches_title
                    subtitle: tr.note_two_way_switches_descr
                }
            }
        }

        DS3.Spacing {
            height: 24
        }
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.InputSingleLine {
            id: nameInput

            atomInput {
                label: tr.name
                placeholderText: tr.scenario_name_placeholder
                text: !!scenario ? scenario.scenario_name : ""
                maxByteLength: 24
            }
        }
    }

    DS3.Spacing {
        height: 24
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

                model: !!device.button1_name && !!device.button2_name ? [device.button1_name, device.button2_name] : []

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

            text: tr.select_buttons_schedule_scenario
        }

        DS3.Spacing {
            height: 24
        }
    }

    DS3.TitleSection {
        text: tr.scenario_action
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
    }

    DS3.SettingsContainer {
        id: deviceAction

        property int selectedIndex: isImpulseType ? 0 : ({
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

            model: deviceActionModelStates

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

        visible: deviceActionModel.count > 1 || !isFastPHOD
        text: isImpulseType ? tr.scenario_action_pulse_desc : tr.scenario_action_desc
    }

    DS3.Spacing {
        height: 24
    }

    DS3.TitleSection {
        text: tr.schedule_scenario_execution_time
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.InputPickerDouble {
            id: timePickerSecond

            leftPicker {
                model: util.generate_hours(settings.is_ampm_time_format)
                input {
                    atomInput {
                        label: tr.hours
                        required: true
                        text: {
                            if (!scenario) return ""
                            let scenatio_hours = scenario.schedule.hours.toString().padStart(2, "0")
                            if (settings.is_ampm_time_format) {
                                return scenatio_hours >= 12 ? `${scenatio_hours - 12} pm` : `${scenatio_hours} am`
                            } else {
                                return `${scenario.schedule.hours.toString().padStart(2, "0")}`
                            }
                        }
                    }
                }
            }

            rightPicker {
                model: util.generate_minutes()
                input {
                    atomInput {
                        label: tr.minutes
                        required: true
                        text: !!scenario
                            ? `${scenario.schedule.minutes.toString().padStart(2, "0")}`
                            : ""
                    }
                }
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    Column {
        id: noTimezoneSelected

        width: parent.width

        visible: !hub.hub_timezone

        DS3.SettingsContainer {
            width: parent.width

            DS3.CommentImportant {
                atomTitle {
                    title: tr.scenario_important_note
                    subtitle: util.insert(tr.schedule_scenario_time_zone_warning, ["", "", "", hub.name])
                }
            }
        }

        DS3.Spacing {
            height: 24
        }
    }

    DS3.TitleSection {
        text: tr.repeat
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
    }

    DS3.SettingsContainer {
        width: parent.width

        DS3.DatePicker {
            id: datePicker

            checkedDays: !!scenario ? scenario.schedule.weekdays : [0,1,2,3,4,5,6]
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

            onClicked: deleteScenario(scenario)
        }
    }

    DS3.Spacing {
        height: 24

        visible: !!scenario
    }

    footer: DS3.ButtonBar {
        enabled: {
            if (isLSTwoGang) {
                return actionButton.selectedButtons.length && !!nameInput.atomInput.text.trim()
            }
            return !!nameInput.atomInput.text.trim()
        }
        hasBackground: true
        button {
            text: tr.save_scenario
            onClicked: {
                var scenarioSettings = {}

                if (!timePickerSecond.leftPicker.input.checkValid() || !timePickerSecond.rightPicker.input.checkValid()) {
                    Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
                    return
                }

                scenarioSettings["name"] = {"name": nameInput.atomInput.text.trim(), "alias": ""}

                scenarioSettings["schedules"] = []
                let hours_int = parseInt(timePickerSecond.leftPicker.input.atomInput.text.split(" ")[0])
                if (settings.is_ampm_time_format && timePickerSecond.leftPicker.input.atomInput.text.includes("pm")) hours_int += 12
                scenarioSettings["schedules"].push({
                    "hours": hours_int,
                    "minutes": parseInt(timePickerSecond.rightPicker.input.atomInput.text),
                    "enabled": true,
                    "week_days": datePicker.checkedDays.map( a => 2 ** a)
                })

                if (isImpulseType) {
                    scenarioSettings["target_action"] = 2
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

                // To chose channel of LS
                let ls_channels = []
                if (isLightSwitch) {
                    ls_channels = isLSTwoGang ? actionButton.selectedButtons : ["LIGHT_SWITCH_CHANNEL1"]
                }

                saveScenarioBySchedule(scenario, scenarioSettings, ls_channels)
            }
        }
    }
}
