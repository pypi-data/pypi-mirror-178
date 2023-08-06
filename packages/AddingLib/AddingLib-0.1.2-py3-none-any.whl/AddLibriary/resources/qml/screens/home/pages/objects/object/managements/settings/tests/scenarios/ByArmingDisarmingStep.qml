import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupStep {
    property bool scenarioAlreadyExists: !!device.arming_actions.length

    property var reactionsModel: {
        if (!device) return []
        if (isImpulseType) {
            return [tr.scenario_action_pulse, tr.no_change]
        }
        return [tr.scenario_action_ON, tr.scenario_action_OFF, tr.no_change]
    }

    height: maxStepHeight

    title: tr.scenario_type_reaction
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

    Column {
        width: parent.width

        visible: isLSTwoGang

        DS3.TitleSection {
            text: tr.left_button_lightswitch_title
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: leftButtonSwitch

                width: parent.width

                title: !!device.button1_name ? device.button1_name : ""
                checked: [
                    "TURN_ON_ON_ARMING",
                    "TURN_OFF_ON_ARMING",
                    "TURN_ON_ON_DISARMING",
                    "TURN_OFF_ON_DISARMING"
                ].some(action => device.arming_actions.includes(action))
            }
        }
    }

    DS3.Spacing {
        height: leftButtonSwitch.checked && isLSTwoGang ? 24 : 0
    }

    DS3.TitleSection {
        text: tr.scenario_reaction_when_arming
        isCaps: true
        isBgTransparent: true
        forceTextToLeft: true
        visible: leftButtonSwitch.checked || !isLSTwoGang
    }

    DS3.SettingsContainer {
        id: whenArming

        property string selected: {
            if (isImpulseType) {
                if (device.arming_actions.includes("ARM_SWITCH_ON") || device.arming_actions.includes("TURN_ON_ON_ARMING")) {
                    return reactionsModel[0]
                }
                if (device.arming_actions.includes("ARM_SWITCH_OFF") || device.arming_actions.includes("TURN_OFF_ON_ARMING")) {
                    return reactionsModel[1]
                }
                return reactionsModel[reactionsModel.length - 1]
            } else {
                if (device.arming_actions.includes("ARM_SWITCH_ON") || device.arming_actions.includes("TURN_ON_ON_ARMING")) {
                    return reactionsModel[0]
                }
                if (device.arming_actions.includes("ARM_SWITCH_OFF") || device.arming_actions.includes("TURN_OFF_ON_ARMING")) {
                    return reactionsModel[1]
                }
                return reactionsModel[reactionsModel.length - 1]
            }
        }

        width: parent.width

        visible: leftButtonSwitch.checked || !isLSTwoGang

        Repeater {
            model: reactionsModel

            DS3.SettingsSingleSelection {
                atomTitle.title: modelData
                checked: modelData == whenArming.selected
                switchChecked: () => whenArming.selected = modelData
            }
        }
    }

    Column {
        width: parent.width

        visible: leftButtonSwitch.checked || !isLSTwoGang

        DS3.Spacing {
            height: 24
        }

        DS3.TitleSection {
            text: tr.scenario_reaction_when_disarming
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
        }

        DS3.SettingsContainer {
            id: whenDisarming

            property string selected: {
                if (isImpulseType) {
                    if (device.arming_actions.includes("DISARM_SWITCH_ON") || device.arming_actions.includes("TURN_ON_ON_DISARMING")) {
                        return reactionsModel[0]
                    }
                    if (device.arming_actions.includes("DISARM_SWITCH_OFF") || device.arming_actions.includes("TURN_OFF_ON_DISARMING")) {
                        return reactionsModel[1]
                    }
                    return reactionsModel[reactionsModel.length - 1]
                } else {
                    if (device.arming_actions.includes("DISARM_SWITCH_ON") || device.arming_actions.includes("TURN_ON_ON_DISARMING")) {
                        return reactionsModel[0]
                    }
                    if (device.arming_actions.includes("DISARM_SWITCH_OFF") || device.arming_actions.includes("TURN_OFF_ON_DISARMING")) {
                        return reactionsModel[1]
                    }
                    return reactionsModel[reactionsModel.length - 1]
                }
            }

            width: parent.width

            Repeater {
                model: reactionsModel

                DS3.SettingsSingleSelection {
                    atomTitle.title: modelData
                    checked: modelData == whenDisarming.selected
                    switchChecked: () => whenDisarming.selected = modelData
                }
            }
        }
    }

    DS3.Spacing {
        height: nightModeReaction.visible ? 24 : 0
    }

    Column {
        id: nightModeReaction

        width: parent.width

        visible: (leftButtonSwitch.checked || !isLSTwoGang) && (whenDisarming.selected != tr.no_change || whenArming.selected != tr.no_change)

        DS3.TitleSection {
            text: tr.perimeter
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: nightModeReactionSwitch

                title: tr.react_on_perimetral_arming_disarming

                checked: isLSTwoGang ?
                    device.arming_actions.includes("REACT_ON_NIGHT_MODE") :
                    device.perimeter_protection_group
            }
        }

        DS3.Comment {
            width: parent.width

            text: tr.react_night_mode_descr
        }
    }

    DS3.Spacing {
        height: isLSTwoGang ? 24 : 0
    }

    Column {
        width: parent.width

        visible: isLSTwoGang

        DS3.TitleSection {
            text: tr.right_button_lightswitch_title
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: rightButtonSwitch

                width: parent.width

                title: !!device.button2_name ? device.button2_name : ""
                checked: [
                    "TURN_ON_ON_ARMING",
                    "TURN_OFF_ON_ARMING",
                    "TURN_ON_ON_DISARMING",
                    "TURN_OFF_ON_DISARMING"
                ].some(action => device.arming_actions_channel2.includes(action))
            }
        }

        DS3.Spacing {
            height: rightButtonSwitch.checked ? 24 : 0
        }

        DS3.TitleSection {
            text: tr.scenario_reaction_when_arming
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
            visible: rightButtonSwitch.checked
        }

        DS3.SettingsContainer {
            id: whenArmingRightButton

            property string selected: {
                if (!!device.arming_actions_channel2 && device.arming_actions_channel2.includes("TURN_ON_ON_ARMING")) {
                    return reactionsModel[0]
                }
                if (!!device.arming_actions_channel2 && device.arming_actions_channel2.includes("TURN_OFF_ON_ARMING")) {
                    return reactionsModel[1]
                }
                return reactionsModel[reactionsModel.length - 1]
            }

            width: parent.width

            visible: rightButtonSwitch.checked

            Repeater {
                model: reactionsModel

                DS3.SettingsSingleSelection {
                    atomTitle.title: modelData
                    checked: modelData == whenArmingRightButton.selected
                    switchChecked: () => whenArmingRightButton.selected = modelData
                }
            }
        }

        DS3.Spacing {
            height: rightButtonSwitch.checked ? 24 : 0
        }

        DS3.TitleSection {
            text: tr.scenario_reaction_when_disarming
            isCaps: true
            isBgTransparent: true
            forceTextToLeft: true
            visible: rightButtonSwitch.checked
        }

        DS3.SettingsContainer {
            id: whenDisarmingRightButton

            property string selected: {
                if (!!device.arming_actions_channel2 && device.arming_actions_channel2.includes("TURN_ON_ON_DISARMING")) {
                    return reactionsModel[0]
                }
                if (!!device.arming_actions_channel2 && device.arming_actions_channel2.includes("TURN_OFF_ON_DISARMING")) {
                    return reactionsModel[1]
                }
                return reactionsModel[reactionsModel.length - 1]
            }

            width: parent.width

            visible: rightButtonSwitch.checked

            Repeater {
                model: reactionsModel

                DS3.SettingsSingleSelection {
                    atomTitle.title: modelData
                    checked: modelData == whenDisarmingRightButton.selected
                    switchChecked: () => whenDisarmingRightButton.selected = modelData
                }
            }
        }

        DS3.Spacing {
            height: rightNightModeReaction.visible ? 24 : 0
        }

        Column {
            id: rightNightModeReaction

            width: parent.width

            visible: rightButtonSwitch.checked && (whenArmingRightButton.selected != tr.no_change || whenDisarmingRightButton.selected != tr.no_change)

            DS3.TitleSection {
                text: tr.perimeter
                isCaps: true
                isBgTransparent: true
                forceTextToLeft: true
            }

            DS3.SettingsContainer {
                width: parent.width

                DS3.SettingsSwitch {
                    id: rightNightModeReactionSwitch

                    title: tr.react_on_perimetral_arming_disarming

                    checked: !!device.arming_actions_channel2.includes("REACT_ON_NIGHT_MODE")
                }
            }

            DS3.Comment {
                width: parent.width

                text: tr.react_night_mode_descr
            }
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.SettingsContainer {
        width: parent.width

        visible: scenarioAlreadyExists

        DS3.ButtonRow {
            text: tr.delete
            isDanger: true

            onClicked: deleteArmingDisarmingScenario(1)
        }
    }

    DS3.Spacing {
        height: 24

        visible: scenarioAlreadyExists
    }

    footer: DS3.ButtonBar {
        enabled: nightModeReaction.visible || rightNightModeReaction.visible
        hasBackground: true
        button {
            text: tr.save_scenario
            onClicked: {
                var settings = {
                    "common_part": {},
                    "_params": {
                        "alt_action_success": true,
                    },
                }

                // WallSwitch family (WallSwitch, Relay, Socket)
                var armingActionField = "actions_on_arming"
                if (device.obj_type == "44") {
                    // LightSwitch family
                    armingActionField = "arming_actions_channel1"
                } else if (device.obj_type == "4c") {
                    // SocketBase family
                    armingActionField = "arming_disarming_actions"
                }

                var armingActions = []
                // Arming 1 channel
                if (whenArming.selected != tr.no_change) armingActions.push(reactionsModel.indexOf(whenArming.selected) + 1)
                // Disarming 1 channel
                if (whenDisarming.selected != tr.no_change) armingActions.push(reactionsModel.indexOf(whenDisarming.selected) + 3)

                var device_subtype = (device.subtype || "").toLowerCase()
                if (isLightSwitch) {
                    settings[device_subtype] = {}
                    settings[device_subtype][armingActionField] = []
                    if (isLSTwoGang) {
                        if (leftButtonSwitch.checked) {
                            settings[device_subtype][armingActionField] = armingActions
                        }
                    } else {
                        settings[device_subtype][armingActionField] = armingActions
                    }

                } else {
                    settings[armingActionField] = armingActions
                }


                // Night Mode 1 channel
                if (nightModeReaction.visible) {
                    if (isLightSwitch) {
                        settings["common_part"]["night_mode_arm"] = leftButtonSwitch.checked && nightModeReactionSwitch.checked
                    } else {
                        settings["common_part"]["night_mode_arm"] = nightModeReactionSwitch.checked
                    }

                    // LightSwitch family
                    if (nightModeReactionSwitch.checked && armingActionField == "arming_actions_channel1" && leftButtonSwitch.checked) {
                        settings[device_subtype][armingActionField].push(5)
                    }
                }

                if (isLSTwoGang) {
                    // Arming 2 channel
                    settings[device_subtype]["arming_actions_channel2"] = []
                    if (rightButtonSwitch.checked) {
                        if (whenArmingRightButton.selected != tr.no_change) settings[device_subtype]["arming_actions_channel2"].push(
                            reactionsModel.indexOf(whenArmingRightButton.selected) + 1
                        )
                        // Disarming 2 channel
                        if (whenDisarmingRightButton.currentIndex != tr.no_change) settings[device_subtype]["arming_actions_channel2"].push(
                            reactionsModel.indexOf(whenDisarmingRightButton.selected) + 3
                        )
                        // Night Mode 2 channel
                        if (rightNightModeReaction.visible && rightNightModeReactionSwitch.checked) {
                            settings[device_subtype]["arming_actions_channel2"].push(5)

                            // Because we need to set this field if at least one channel is selected
                            if (!settings["common_part"]["night_mode_arm"]) {
                                settings["common_part"]["night_mode_arm"] = rightNightModeReactionSwitch.checked
                            }
                        }
                    }
                }

                saveScenarioByArmingDisarming(settings)
            }
        }
    }
}