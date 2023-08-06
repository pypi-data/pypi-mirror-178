import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3Popups.PopupMultistep {
    id: popup

    property var device: null
    property string selectedUiScenarioType: ""

    readonly property bool armingDisarmingScenarioExists: !!(
        (
            device.arming_actions
            && device.arming_actions.length
            && !device.arming_actions.includes("NO_ARM_ACTIONS_INFO")
            && !device.arming_actions.includes("NO_ARMING_DISARMING_ACTIONS")
        )
        || (
            !!device.arming_actions_channel2
            && device.arming_actions_channel2.length
            && !device.arming_actions_channel2.includes("NO_ARMING_DISARMING_ACTIONS")
        )
    )
    readonly property bool isImpulseType: device.lockup_relay_mode == 2 && (
        !device.hasOwnProperty("pulse_mode_contact_normal_available") || !!device.pulse_mode_contact_normal_available
    )
    readonly property var deviceActionModelStates: {
        if (isImpulseType) return [tr.scenario_action_pulse]
        if (isPHOD) return [tr.take_photo_alarm_scenario]

        let states = [tr.scenario_action_ON, tr.scenario_action_OFF]
        if (hub.firmware_version_dec < 209102) return states

        // button
        if (device.obj_type == "0c") return states

        states.push(tr.scenario_action_SWITCH)

        return states
    }
    readonly property var scenarioTypeStepMap: ({
        "ARMING": "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ByArmingDisarmingStep.qml",
        "INTRUSION": "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ByAlarmStep.qml",
        "SCHEDULE": "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ByScheduleStep.qml",
        "TRIGGER": "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ScenarioTriggerSelectActionStep.qml",
        "TEMPERATURE": "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ByTemperatureStep.qml",
        "BY_ACTUATING": "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ScenarioTriggerSelectActionStep.qml",
        "THRESHOLD": "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/ThresholdStep.qml",
    })
    readonly property var scenarioTypeIconMap: ({
        "ARMING": "qrc:/resources/images/desktop/scenarios_settings/ScenarioArming.svg",
        "INTRUSION": "qrc:/resources/images/desktop/scenarios_settings/ScenarioAlarm.svg",
        "SCHEDULE": "qrc:/resources/images/desktop/scenarios_settings/ScenarioSchedule.svg",
        "TRIGGER": "qrc:/resources/images/desktop/scenarios_settings/ScenarioButton.svg",
        "TEMPERATURE": "qrc:/resources/images/desktop/scenarios_settings/ScenarioTemperature.svg",
        "BY_ACTUATING": "qrc:/resources/images/desktop/scenarios_settings/ScenarioButton.svg",
    })
    readonly property var scenariosTypes: [
        {
            type: "ARMING",
            title: tr.scenario_type_reaction,
            description: tr.scenario_type_reaction_desc,
            disabled: armingDisarmingScenarioExists,
            visible: true,
        },
        {
            type: "INTRUSION",
            title: tr.scenario_type_alarm,
            description: tr.scenario_type_alarm_desc,
            visible: true,
        },
        {
            type: "SCHEDULE",
            title: tr.scenario_type_schedule,
            description: tr.scenario_type_schedule_desc,
            visible: true,
        },
        {
            type: "BY_ACTUATING",
            title: tr.by_switch_actuating_scenario_title,
            description: tr.by_switch_actuating_scenario_descr,
            visible: isLightSwitch,
        },
        {
            type: "TEMPERATURE",
            title: tr.by_temperature_scenario_title,
            description: tr.by_temperature_scenario_title_description,
            visible: (isRelayLike || isLightSwitch) && __temperature_scenarios_features__,
        },
    ]
    readonly property bool isPHOD: ["0d", "18"].includes(device.obj_type)
    readonly property bool isFastPHOD: isPHOD && device.subtype == "PHOD"
    readonly property bool isButton: device.class_name == "button"
    readonly property bool isRelayLike: ["socket", "socket_base", "relay", "wall_switch"].includes(device.class_name)
    readonly property bool isLightSwitch: device.class_name == "light_switch"
    readonly property bool isLSTwoGang: device.subtype == "LIGHT_SWITCH_TWO_GANG"
    readonly property bool isLSTwoWay: device.subtype == "LIGHT_SWITCH_TWO_WAY"
    readonly property bool isLQ: device.class_name == "life_quality"
    readonly property bool isPhodSourceExists: {
        if (isFastPHOD) return management.filtered_devices_for_scenarios_fast_pod.length
        if (isPHOD) return management.filtered_devices_for_scenarios_pod.length
        return true
    }

    function createScenario(selectedScenarioType=undefined) {
        if (isButton && device.button_mode != 2) return Popups.text_popup(tr.information, tr.smart_button_add_scenario_warning)

        if (selectedScenarioType) selectedUiScenarioType = selectedScenarioType
        else if (isButton) selectedUiScenarioType = "TRIGGER"
        else if (isLQ) selectedUiScenarioType = "THRESHOLD"
        else if (isPHOD) selectedUiScenarioType = "INTRUSION"

        popup.child.setChild(
            selectedUiScenarioType
                ? scenarioTypeStepMap[selectedUiScenarioType]
                : "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/scenarios/SelectScenarioTypeStep.qml"
        )
    }

    function saveScenarioByAlarm(scenario, scenarioSettings, scenarioTriggers, ls_channels) {
        Popups.please_wait_popup(tr.request_send, 30, [management.scenarios.scenariosUpdated])
        const triggers = selectedUiScenarioType == "TEMPERATURE" ? [] : scenarioTriggers
        const thresholds = selectedUiScenarioType == "TEMPERATURE" ? scenarioTriggers : []

        if (scenario == null) {
            app.hub_management_module.add_scenario(device, scenarioSettings, triggers, ls_channels, thresholds)
        } else {
            app.hub_management_module.save_scenario_settings(device, scenario, scenarioSettings, triggers, ls_channels, thresholds)
        }
        goBack(popup.currentStepIndex)
    }
    function saveScenarioByArmingDisarming(settings) {
        Popups.please_wait_popup(tr.request_send, 30, [app.altActionSuccess])
        app.hub_management_module.apply_update(management, device, settings)
        goBack(popup.currentStepIndex)
    }
    function saveScenarioBySchedule(scenario, scenarioSettings, ls_channels) {
        Popups.please_wait_popup(tr.request_send, 30, [management.scenarios.scenariosUpdated])
        if (scenario == null) {
            app.hub_management_module.add_schedule(device, scenarioSettings, ls_channels)
        } else {
            app.hub_management_module.save_schedule_settings(device, scenario, scenarioSettings, ls_channels)
        }
        goBack(popup.currentStepIndex)
    }
    function saveTriggerScenario(scenario, scenarioSettings, targetActions, ls_channels, thresholds) {
        Popups.please_wait_popup(tr.request_send, 30, [management.scenarios.scenariosUpdated])
        if (scenario == null) {
            app.hub_management_module.add_scenario(device, scenarioSettings, targetActions, ls_channels, thresholds)
        } else {
            app.hub_management_module.save_scenario_settings(device, scenario, scenarioSettings, targetActions, ls_channels, thresholds)
        }
        goBack(popup.currentStepIndex)
    }
    function deleteScenario(scenario, goBackSteps) {
        Popups.please_wait_popup(tr.request_send, 30, [management.scenarios.scenariosUpdated])
        app.hub_management_module.del_scenario(scenario)
        goBack(popup.currentStepIndex)
    }
    function deleteArmingDisarmingScenario(goBackSteps) {
        var settings = {
            "_params": {
                "alt_action_success": true,
            },
        }

        if (device.obj_type == "44") {
            // LightSwitch family
            settings[device.subtype.toLowerCase()] = {}
            settings[device.subtype.toLowerCase()]["arming_actions_channel1"] = []
            if (device.subtype == "LIGHT_SWITCH_TWO_GANG") {
                // LightSwitch 2-gang
                settings[device.subtype.toLowerCase()]["arming_actions_channel2"] = []
            }
        } else if (device.obj_type == "4c") {
            // SocketBase family
            settings["arming_disarming_actions"] = []
        } else {
            // WallSwitch family (WallSwitch, Relay, Socket)
            settings["actions_on_arming"] = []
        }

        saveScenarioByArmingDisarming(settings)
        if (!!goBackSteps)
            goBack(goBackSteps)
    }

    onCurrentStepIndexChanged: if (currentStepIndex == 0) selectedUiScenarioType = ""

    width: 500

    header: DS3.NavBarModal {
        headerText: popup.title
        showBackArrow: !!currentStepIndex
        showManualIcon: !currentStepIndex
        onManualAreaClicked: {
             var locale = tr.get_locale()
             var link = "https://support.ajax.systems/" + locale + "/manuals/scenarios/"
             Qt.openUrlExternally(link)
        }

        onBackAreaClicked: goBack()
    }

    firstStepComponent: DS3Popups.PopupStep {
        id: firstStep

        readonly property bool scenariosExist: !!scenariosModel.count || armingDisarmingScenarioExists

        height: maxStepHeight

        title: tr.scenarios
        sidePadding: 24

        DS3.Spacing {
            height: 24
        }

        Column {
            width: parent.width

            visible: !scenariosExist

            spacing: 24

            DS3.InfoContainer {
                imageType: DS3.InfoContainer.ImageType.BigImage
                imageSource: "qrc:/resources/images/Athena/common_icons/EmptySecurityScheduleImage.svg"
                titleComponent.text: {
                    if (isFastPHOD && !isPhodSourceExists) return tr.no_devices_photo_alarm_scenarios
                    if (isPHOD && !isPhodSourceExists) return tr.scenarios_by_alarm_no_fires_desc
                    return tr.create_first_scenario_desc
                }
            }

            DS3.SettingsContainer {
                width: parent.width

                visible: !hub.photo_on_demand_scenario && isPHOD && isPhodSourceExists

                DS3.CommentImportant {
                    atomTitle.title: tr.photo_scenario_not_allowed_created_warning_title
                    atomTitle.subtitle: tr.photo_scenario_not_allowed_created_warning_descr
                    status: DS3.CommentImportant.Status.Attention
                }
            }

            DS3.ButtonOutlined {
                width: parent.width

                visible: isPhodSourceExists
                text: tr.create_first_scenario
                buttonIconSource: "qrc:/resources/images/Athena/common_icons/plus.svg"
                onClicked: createScenario()
            }
        }

        Column {
            width: parent.width

            visible: scenariosExist

            spacing: 24

            DS3.SettingsContainer {
                width: parent.width

                visible: !hub.photo_on_demand_scenario && isPHOD && isPhodSourceExists

                DS3.CommentImportant {
                    atomTitle.title: tr.photo_scenario_not_allowed_created_warning_title
                    atomTitle.subtitle: tr.photo_scenario_not_allowed_created_warning_descr
                    status: DS3.CommentImportant.Status.Attention
                }
            }

            DS3.SettingsContainer {
                width: parent.width

                DS3.SettingsNavigationTitlePrimary {
                    id: armingDisarmingScenario

                    signal deleteChoosen

                    onDeleteChoosen: {
                        deleteArmingDisarmingScenario()
                    }

                    visible: armingDisarmingScenarioExists
                    title: tr.scenario_reaction_when_arming_disarming_name
                    icon: scenarioTypeIconMap["ARMING"]

                    onEntered: setChild(scenarioTypeStepMap["ARMING"], {device: device})

                    DS3.MouseArea {
                        acceptedButtons: Qt.RightButton

                        onClicked: (mouse) => {
                            contextMenu.x = mouse.x
                            contextMenu.y = mouse.y
                            contextMenu.open()
                        }
                    }

                    DS3.SheetAction {
                        id: contextMenu

                        DS3.SettingsSingleSelection {
                            atomTitle {
                                title: tr.edit
                            }
                            switchChecked: () => {
                                entered()
                                contextMenu.close()
                            }
                        }

                        DS3.SettingsSingleSelection {
                            atomTitle {
                                title: tr.delete
                                titleColor: ui.ds3.figure.attention
                            }
                            switchChecked: () => {
                                armingDisarmingScenario.deleteChoosen()
                                contextMenu.close()
                            }
                        }
                    }
                }

                Repeater {
                    id: scenariosModel

                    model: device.obj_type == "0c" ?
                        management.filtered_scenarios_by_button :
                        management.filtered_scenarios_by_target

                    ScenarioDelegate {
                        readonly property string uiScenarioType: (
                            scenario.source_type == "THRESHOLD" && !isLQ && "TEMPERATURE"
                            || isButton && "TRIGGER"
                            || scenario.source_type
                        )

                        title: scenario.scenario_name
                        checked: scenario.enabled_scenario
                        icon: scenarioTypeIconMap[uiScenarioType] || ""
                        onToggleCallback: () => {
                            Popups.waitPopup(
                                management.scenarios.scenariosUpdated,
                                () => {checked = scenario.enabled_scenario}
                            )
                            app.hub_management_module.enable_scenario(scenario, !checked)
                        }

                        onEntered: {
                            selectedUiScenarioType = uiScenarioType
                            setChild(scenarioTypeStepMap[uiScenarioType], {scenario: scenario})
                        }
                        onDeleteChoosen: {
                            deleteScenario(scenario)
                        }
                    }
                }
            }

            DS3.ButtonOutlined {
                width: parent.width

                text: tr.add_scenario
                buttonIconSource: "qrc:/resources/images/Athena/common_icons/plus.svg"

                onClicked: {
                    createScenario()
                }
            }
        }
    }
}