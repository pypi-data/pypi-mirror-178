import QtQuick 2.12
import QtQuick.Controls 2.1
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: rect
//  Current scenario
    property var scenario: null
//  Device where scenario is (hub)
    property var device: null
//  Facility availability
    property var devEnable: true
//  All groups of the hub
    property var groups: hub.groups_enabled ? management.filtered_groups.get_all_groups() : []
//  Selected groups of the scenario
    property var selected: []
//  schedules items
    property var schedules: scheduleList.contentItem.children
//  Check if all of the groups selected to make AllGroups field checked
    function is_all_groups_selected() {
        for (var index in schedules) {
            if (schedules[index].objectName == "delegate" && !schedules[index].checked) {
                return false
            }
        }
        return true
    }
//  Check if nothing selected because you can't create scenario without group
    function nothing_selected() {
        if (securityObjectsPicker.currentIndex == 0) return false
        if (!groups.length) return false
        for (var index in schedules) {
            if (schedules[index].objectName == "delegate" && schedules[index].checked ){
                return false
            }
        }
        return true
    }
    property var hasGroupsChanged: {
        if (securityObjectsPicker.currentIndex == 1 && rect.groups.length) {
            // get scenario selected groups
            let active_scenario_groups = !!scenario ? scenario.get_selected_groups() : []
            // get choosen groups
            let active_choosen_groups = []
            for(var index in schedules) {
                if (schedules[index].objectName == "delegate" && schedules[index].checked == true) {
                    active_choosen_groups.push(schedules[index].groupId)
                }
            }
            // check if count of selected groups is equil
            if (active_scenario_groups.length != active_choosen_groups.length) return true
            // compare scenario selected and chosen groups
            for (var i = 0; i < active_scenario_groups.length; i++) {
                if (active_scenario_groups[i]["id"] != active_choosen_groups[i]) return true
            }
        }
        return false
    }

    Connections {
        target: app.hub_management_module

        onScenarioSuccess: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScenariosScreen.qml")
        }

        onDelScenarioSuccess: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScenariosScreen.qml")
        }
    }

    width: 360
    height: 660

    color: ui.ds3.bg.base
    enabled: devEnable

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            scenarioNameField.atomInput.text,
            securityObjectsPicker.currentIndex,
            rect.hasGroupsChanged,
            armMode.checked,
            executionTimeField.leftPicker.input.atomInput.text,
            executionTimeField.rightPicker.input.atomInput.text,
            datePicker.checkedDays
        ]
    }

    DS3.NavBarModal {
        id: scenarioSettingsBar

        headerText: tr.scenario_settings
        showCloseIcon: false
        isRound: false
        showBackArrow: true

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/hub_scenarios/ArmDisarmScenariosScreen.qml")
        }
    }

    DS3.ScrollView {
        id: contentView

        width: parent.width

        anchors {
            fill: undefined
            top: scenarioSettingsBar.bottom
            bottom: saveButton.top
        }

        padding: 24

        DS3.SettingsContainer {
            id: scenarioNameFieldBlock

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputSingleLine {
                id: scenarioNameField

                atomInput {
                    text: !!scenario ? scenario.scenario_name : ""
                    label: tr.name
                    placeholderText: tr.scenario_name_placeholder

                    onTextChanged: {
                        atomInput.text = util.validator(atomInput.text, 24)
                    }
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsPickerTitleSecondary {
                id: securityObjectsPicker

                model: rect.groups.length ?
                    [tr.partially_armed, tr.groups_hub_settings] :
                    [tr.partially_armed, hub.name]
                // check if current mode is night mode or groups
                currentIndex: !!scenario && [6, 7].includes(scenario.target_action) ? 0 : 1
                atomTitle.title: tr.scenario_arm_disarm_select_target
            }
        }

        DS3.Spacing {
            height: groupsBlock.visible ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.select_group_scenario
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: groupsBlock.visible
        }

        DS3.SettingsContainer {
            id: groupsBlock

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: securityObjectsPicker.currentIndex == 1 && rect.groups.length

            DS3.SettingsMultiSelection {
                id: allGroups

                atomTitle.title: tr.scenario_arm_disarm_all_groups
                checked: {
                    if (scenario && scenario.targets[0].target_id != hub.id) {
                        return is_all_groups_selected()
                    } else {
                        for(var index in schedules) {
                            if (schedules[index].objectName == "delegate") {
                                schedules[index].checked = true
                            }
                        }
                        return true
                    }
                }

                DS3.MouseArea {
                    onClicked: {
                        allGroups.checked = !allGroups.checked
                        for(var index in schedules) {
                            if (schedules[index].objectName == "delegate") {
                                schedules[index].checked = allGroups.checked
                            }
                        }
                    }
                }
            }

            ListView {
                id: scheduleList

                width: parent.width
                height: contentHeight

                spacing: 1
                interactive: false
                model: groups

                delegate: DS3.SettingsMultiSelection {
                    id: groupField

                    property var indexRef: index
                    property var groupId: modelData["id"]

                    width: scheduleList.width
                    height: 54

                    objectName: "delegate"
                    atomTitle.title: modelData.name
                    checked: {
                        // if not night mode and scenario exists
                        if (securityObjectsPicker.currentIndex == 0 || !scenario) return false
                        var active_groups = scenario.get_selected_groups()
                        // check if current group is active
                        for (var i = 0; i < active_groups.length; i++) {
                            if (active_groups[i]["id"] == groupId) return true
                        }
                        return false
                    }

                    DS3.MouseArea {
                        onClicked: {
                            groupField.checked = !groupField.checked
                            // check if all groups selected to select AllGroups field
                            allGroups.checked = is_all_groups_selected()
                        }
                    }
                }
            }
        }

        DS3.Spacing {
            height: groupErrorText.visible ? 4 : 0
        }

        DS3.Text {
            id: groupErrorText

            width: parent.width

            text: tr.select_one_group
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.attention
            visible: nothing_selected()
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            width: parent.width

            text: tr.scenario_arm_disarm_action
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSingleSelection {
                id: armMode

                atomTitle.title: tr.arm
                // check if disarm mode not selected
                checked: scenario ? ![4, 6].includes(scenario.target_action) : true
                switchChecked: () => {
                    checked = true
                    disarmMode.checked = false
                }
            }

            DS3.SettingsSingleSelection {
                id: disarmMode

                atomTitle.title: tr.disarm
                // check if disarm mode selected
                checked: scenario ? [4, 6].includes(scenario.target_action) : false

                switchChecked: () => {
                    checked = true
                    armMode.checked = false
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            width: parent.width

            text: tr.schedule_scenario_execution_time
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.SettingsContainer {
            id: executionTimeBlock

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.InputPickerDouble {
                id: executionTimeField

                leftPicker {
                    model: util.generate_hours(settings.is_ampm_time_format)
                    input {
                        atomInput {
                            label: tr.hours
                            required: true
                            text: {
                                if (!scenario) {
                                    let date_hours = new Date().getHours().toString().padStart(2, "0")
                                    if (!settings.is_ampm_time_format) return date_hours
                                    return date_hours >= 12 ? `${date_hours - 12} pm` : `${date_hours} am`
                                }
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
                                : new Date().getMinutes()
                        }
                    }
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            width: parent.width

            text: tr.schedule_scenario_repeat
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.SettingsContainer {
            id: datePickerBlock

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.DatePicker {
                id: datePicker

                checkedDays: scenario ?
                    scenario.schedule.weekdays.sort((function(a, b) {
                      return a - b;
                    })) :
                    [0, 1, 2, 3, 4, 5, 6]
            }
        }

        DS3.Spacing {
            height: scenario ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.ButtonRow {
                id: deleteScenarioButton

                isDanger: true
                text: tr.delete_scenario_schedule
                visible: scenario

                onClicked: {
                    Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.delete,
                        text: tr.confirm_deletion,
                        firstButtonCallback: () => {
                            Popups.please_wait_popup()

                            if (scenario.obj_type == "2a") {
                                app.hub_management_module.del_scenario(scenario)
                                return
                            }

                            var settings = {
                                "common_part": {
                                    "night_mode_arm": false,
                                },
                                "actions_on_arming": [],
                                "_params": {
                                    "special_signal": "delScenarioSuccess",
                                },
                            }

                            app.hub_management_module.apply_update(management, device, settings)
                        },
                        firstButtonText: tr.delete,
                        secondButtonText: tr.cancel,
                        scenario: scenario
                    })
                    return
                }
            }
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        enabled: changesChecker.hasChanges

        button.onClicked: {
            focus = true
            var scenarioSettings = {}
            var scenarioName = scenarioNameField.atomInput.text.trim()
            var blockY = undefined

            if (!scenarioName) {
                blockY = scenarioNameFieldBlock.y
            } else if (!executionTimeField.leftPicker.input.atomInput.text || !executionTimeField.rightPicker.input.atomInput.text) {
                blockY = executionTimeBlock.y
            } else if (nothing_selected()) {
                blockY = groupsBlock.y
            }

            if (blockY != undefined) {
                contentView.scrollBar.scrollTo(blockY)
                return Popups.text_popup(tr.information, tr.please_fill_in_all_of_the_required_fields)
            }

            let hours_int = parseInt(executionTimeField.leftPicker.input.atomInput.text.split(" ")[0])
            if (settings.is_ampm_time_format && executionTimeField.leftPicker.input.atomInput.text.includes("pm")) hours_int += 12
            scenarioSettings["name"] = {"name": scenarioName, "alias": ""}
            scenarioSettings["schedules"] = []
            scenarioSettings["schedules"].push({
                "hours": hours_int,
                "minutes": parseInt(executionTimeField.rightPicker.input.atomInput.text),
                "enabled": true,
                "week_days": datePicker.checkedDays.slice().map( a => parseInt(2 ** a))
            })
            // push selected groups to list
            for(var index in schedules) {
                if (schedules[index].objectName == "delegate" && schedules[index].checked) {
                    rect.selected.push(rect.groups[schedules[index].indexRef])
                }
            }

            scenarioSettings["targets"] = rect.selected
            // if night mode
            if (securityObjectsPicker.currentIndex == 0) {
                if (armMode.checked) {
                    scenarioSettings["target_action"] = 7
                } else {
                    scenarioSettings["target_action"] = 6
                }
                scenarioSettings["targets"] = []
                scenarioSettings["targets"].push({"target_object_type": parseInt(hub.obj_type, 16), "target_id": hub.hub_id})
            // group mode
            } else {
                if (armMode.checked) {
                    scenarioSettings["target_action"] = 5
                } else {
                    scenarioSettings["target_action"] = 4
                }
                if (!rect.groups.length) {
                    scenarioSettings["targets"] = [{"target_object_type": parseInt(hub.obj_type, 16), "target_id": hub.hub_id}]
                }
            }
            // create new scenario
            if (scenario == null) {
                Popups.please_wait_popup()
                app.hub_management_module.add_schedule(device, scenarioSettings)
            // edit scenario
            } else {
                Popups.please_wait_popup()
                app.hub_management_module.save_schedule_settings(device, scenario, scenarioSettings)
            }
        }
    }
}
