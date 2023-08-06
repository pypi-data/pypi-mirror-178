import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    id: armingDisarmingSettings

    property var verifying: management.filtered_devices_for_arming.confirming().sort()
    property var sideMargin: 24

    function getResultSelectDevices(arr1, arr2) {
        let result = arr1.filter((elem) => arr2.every((sub) => (elem[1] != sub[1] || elem[2] != sub[2])))
        return result
    }

    Connections {
        target: app

        onAltActionSuccess: {
            if (serviceSettings.isWizard) {
                if (!twoStepArming.checked) {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/FinalWizardScreen.qml")
                } else {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/WizardBeepDevices.qml")
                }
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    Component.onCompleted: {
        if (serviceSettings.isWizard && lastScreen == 6) {
            twoStepArming.checked = true

            secondExitTimer.value = 60
            exitTimer.value = 30
            bounceTimerSlider.value = 3

            alarmDelayTimer.value = 30

            disarmingByKeypad.checked = false
            lastScreen += 1
        }

        if (twoStepArming.checked && management.devices.not_pd_devices_tsa.length) {
            Popups.not_pd_compliant_devices_popup(management.devices.not_pd_devices_tsa)
        }

        // delete this screen from array if changed pd complient status
        let array = serviceSettings.notCompliantWizardScreens
        let index = array.indexOf(tr.arming_disarming)

        if (index != -1) {
            array.splice(index, 1)
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: {
            let changes_list = [twoStepArming.checked, alarmDelayTimer.value]
            if (twoStepArming.checked) {
                changes_list.push(
                    secondExitTimer.value,
                    armingDisarmingSettings.verifying,
                    bounceTimerSlider.value,
                    exitTimer.value,
                )
            }
            if (alarmDelayTimer.value) {
                changes_list.push(disarmingByKeypad.checked)
            }
            return changes_list
        }
    }

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }

    Loader {
        id: selectDeviceLoader

        anchors.fill: parent

        source: ""
        z: 3
    }

    DS3.NavBarModal {
        id: armingDisarmingBar

        headerText: tr.arming_disarming
        showBackArrow: true
        showCloseIcon: false
        isRound: false

        onBackAreaClicked: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SystemIntegrityCheck.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: armingDisarmingBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.Text {
            width: parent.width

            text: tr.arm_header
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: twoStepArming

                enabled: devEnable
                title: tr.two_step_arming
                checked: hub.two_stage_arming_state

                onSwitched: () => {
                    checked = !checked
                    if (checked && management.devices.not_pd_devices_tsa.length) {
                        Popups.not_pd_compliant_devices_popup(management.devices.not_pd_devices_tsa)
                    }
                }
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            text: twoStepArming.checked ? tr.two_step_arming_description_if_active : tr.two_step_arming_tip
            style: ui.ds3.text.body.MRegular
            color: twoStepArming.checked ? ui.ds3.figure.secondary : ui.ds3.figure.attention
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            width: parent.width

            text: tr.confirm_arming_by_device
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: secondExitTimer.visible
        }

        DS3.Spacing {
            height: secondExitTimer.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: secondExitTimer

                enabled: devEnable
                value: hub.second_stage_exit_timer
                title: tr.second_stage_exit_timer
                from: 60
                to: 240
                stepSize: 5
                suffix: tr.sec
                visible: twoStepArming.checked
            }
        }

        DS3.Spacing {
            height: secondExitTimer.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.second_stage_exit_timer_tip
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: secondExitTimer.visible
        }

        DS3.Spacing {
            height: secondExitTimer.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsNavigationTitlePrimary {
                id: selectDevicesItem

                title: tr.select_devices
                subtitle: {
                    let verifyingDevices = armingDisarmingSettings.verifying
                    let count = 0
                    for (var i = 0; i < verifyingDevices.length; i++) {
                        if (verifyingDevices[i][2] == true) {
                            count += 1
                        }
                    }
                    return count ? count : ""
                }
                visible: twoStepArming.checked

                onEntered: {
                    management.filtered_devices_for_arming.invalidate()
                    let data = {
                        "verifying": armingDisarmingSettings.verifying,
                        "devices_model": management.filtered_devices_for_arming,
                        "empty_image": "qrc:/resources/images/desktop/icons/ic-no-select-devices.svg",
                        "empty_text": tr.no_devices_for_arming,
                        "parentRect": armingDisarmingSettings
                    };
                    selectDeviceLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SelectDevices.qml", data)
                }
            }
        }

        DS3.Spacing {
            height: selectDevicesItem.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.select_at_least_one_pd_device
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.attention
            visible: {
                var count = 0
                for (var i = 0; i < verifying.length; i++) {
                    if (verifying[i][2] == true) {
                        count += 1
                    }
                }
                return count < 1 && selectDevicesItem.visible
            }
        }

        DS3.Spacing {
            height: selectDevicesItem.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: bounceTimerSlider

                enabled: devEnable
                value: hub.final_door_bounce_timer
                title: tr.bounce_timer
                from: 0
                to: 5
                stepSize: 1
                suffix: tr.sec
                visible: twoStepArming.checked
            }
        }

        DS3.Spacing {
            height: bounceTimerSlider.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.bounce_timer_tip
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: bounceTimerSlider.visible
        }

        DS3.Spacing {
            height: bounceTimerSlider.visible ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.arm_with_app
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: exitTimer.visible
        }

        DS3.Spacing {
            height: exitTimer.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: exitTimer

                enabled: devEnable
                value: hub.app_exit_timer
                title: tr.exit_timer
                from: 30
                to: 60
                stepSize: 5
                suffix: tr.sec
                visible: twoStepArming.checked
            }
        }

        DS3.Spacing {
            height: exitTimer.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.exit_timer_tip
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: exitTimer.visible
        }

        DS3.Spacing {
            height: exitTimer.visible ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.disarm_header
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: alarmDelayTimer.visible
        }

        DS3.Spacing {
            height: alarmDelayTimer.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: alarmDelayTimer

                enabled: devEnable
                value: hub.remote_notification_delay
                title: tr.arc_alarm_delay_timer
                from: 0
                to: 60
                stepSize: 5
                suffix: tr.sec
            }
        }

        DS3.Spacing {
            height: alarmDelayTimer.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: alarmDelayTimer.value < 30 ? tr.timer_at_least_30_sec_for_PD : tr.arc_alarm_delay_timer_tip
            style: ui.ds3.text.body.MRegular
            color: alarmDelayTimer.value < 30 ? ui.ds3.figure.attention : ui.ds3.figure.secondary
            visible: alarmDelayTimer.visible
        }

        DS3.Spacing {
            height: alarmDelayTimer.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: disarmingByKeypad

                enabled: devEnable
                title: tr.allow_disarming_by_keypad
                checked: hub.disarming_by_keypad
                visible: alarmDelayTimer.value
            }
        }

        DS3.Spacing {
            height: disarmingByKeypad.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.allow_disarming_by_keypad_info
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: disarmingByKeypad.visible
        }
    }

    Parts.ButtonNextCancelPD {
        id: saveButton

        buttonText: serviceSettings.isWizard ? tr.next: tr.save
        enabled: serviceSettings.isWizard ? true : devEnable && changesChecker.hasChanges
        hasStepper: serviceSettings.isWizard
        stepAmount: 10
        currentStep: 7
        commentText: tr.settings_are_not_PD6662_compliant
        commentColor: ui.ds3.figure.attention
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
        hasComment: {
            let count = 0

            for (let i = 0; i < armingDisarmingSettings.verifying.length; i++) {
                if (armingDisarmingSettings.verifying[i][2] == true) {
                    count += 1
                }
            }

            if (serviceSettings.isWizard &&
                (!twoStepArming.checked ||
                    disarmingByKeypad.checked ||
                    !count || alarmDelayTimer.value < 30)
            ) {
                return true
            }
            return false
        }

        button.onClicked: {
            Popups.please_wait_popup()

            var data = []

            var settings = {"type": "21", "id": hub.hub_id}

            // arming
            settings["two_stage_arming_state"] = twoStepArming.checked
            settings["second_stage_exit_timer"] = secondExitTimer.value
            settings["final_door_bounce_timer"] = bounceTimerSlider.value
            settings["app_exit_timer"] = exitTimer.value

            // disarming
            settings["remote_notification_delay"] = alarmDelayTimer.value
            settings["disarming_by_keypad"] = disarmingByKeypad.checked

            data.push(settings)

            // save arming devices

            var armingDevices = getResultSelectDevices(armingDisarmingSettings.verifying, management.filtered_devices_for_arming.confirming())

            for (let dev of armingDevices) {
                let device_info = {}

                device_info["type"] = dev[0]
                device_info["id"] = dev[1]
                device_info["device_alarm_logic_type"] = dev[2] ? "ARMING_COMPLETION_DEVICE" : "NONE"

                data.push(device_info)
            }

            if (saveButton.hasComment) {
                serviceSettings.notCompliantWizardScreens.push(tr.arming_disarming)
            }
            if (!twoStepArming.checked) {
                serviceSettings.notCompliantWizardScreens.push(tr.beep_on_delay_pd)
            }

            app.hub_management_module.update_objects_settings(data, {"emit_alt_signal": true})
        }
    }
}
