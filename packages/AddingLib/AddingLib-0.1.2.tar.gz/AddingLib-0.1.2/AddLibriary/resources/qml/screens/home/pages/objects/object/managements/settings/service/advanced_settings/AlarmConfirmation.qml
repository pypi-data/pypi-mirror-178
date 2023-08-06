import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    id: alarmConfirmationSettings

    property var verifying: management.filtered_devices_for_verification_mode.verifying().sort()
    property var holdUpVerifying: management.filtered_devices_hold_up_verification.verifying().sort()
    property var sideMargin: 24
    property var holdUpVerifyingDevicesCount: {
        let count = 0

        for (var i = 0; i < holdUpVerifying.length; i++) {
            if (holdUpVerifying[i][2] == true) {
                count += 1
            }
        }
        return count ? count : ""
    }
    
    function getResultSelectDevices(arr1, arr2) {
        let result = arr1.filter((elem) => arr2.every((sub) => (elem[1] != sub[1] || elem[2] != sub[2])))
        return result
    }

    function checkWarningComment() {
        let count = 0

        for (var i = 0; i < alarmConfirmationSettings.verifying.length; i++) {
            if (alarmConfirmationSettings.verifying[i][2] == true) {
                count += 1
            }
        }

        if (serviceSettings.isWizard &&
            (activeSwitch.checked != true || tamperAlarmConfirm.checked != false
            || alarmOnDelayedDevices.checked != false || count < 2)
        ) {
            saveButton.hasComment = true
            return
        }
        saveButton.hasComment = false
    }

    Connections {
        target: app

        property string loaderSource: {
            if (serviceSettings.isWizard) {
                if (hub.hub_type == "YAVIR") {
                    return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/DevicesAutoBypass.qml"
                } else {
                    return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/WizardHoldUpAlarmConfirm.qml"
                }
            } else {
                return ""
            }
        }

        onAltActionSuccess: {
            advancedSettingsLoader.setSource(loaderSource)
        }
    }

    Component.onCompleted: {
        if (serviceSettings.isWizard && lastScreen == 0) {

            activeSwitch.checked = true
            timeoutSlider.value = 30
            tamperAlarmConfirm.checked = false
            alarmOnDelayedDevices.checked = false

            holdUpAlarmSwitch.checked = true
            holdUptimeoutSlider.value = 8
            lastScreen += 1
        }

        // delete this screen from array if changed pd complient status
        let array = serviceSettings.notCompliantWizardScreens
        let index = array.indexOf(tr.automatic_confirmation)
        if (index != -1) {
            array.splice(index, 1)
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: {
            let changes_list = [activeSwitch.checked, holdUpAlarmSwitch.checked]
            if (activeSwitch.checked) {
                changes_list.push(
                    alarmConfirmationSettings.verifying,
                    timeoutSlider.value,
                    tamperAlarmConfirm.checked,
                    alarmOnDelayedDevices.checked
                )
            }
            if (holdUpAlarmSwitch.checked) {
                changes_list.push(
                    selectHoldUpDevicesItem.subtitle,
                    holdUptimeoutSlider.value
                )
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
        id: alarmConfirmationBar

        headerText: tr.british_standard_setting_updated
        showBackArrow: true
        showCloseIcon: false
        isRound: false

        onBackAreaClicked: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/StartWizardScreen.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: alarmConfirmationBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.Text {
            width: parent.width

            text: tr.advanced_settings
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: activeSwitch

                enabled: devEnable
                title: tr.automatic_confirmation
                checked: hub.verification_enabled

                onSwitched: () => {
                    checked = !checked
                    checkWarningComment()
                }
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            color: activeSwitch.checked ? ui.ds3.figure.secondary : ui.ds3.figure.attention
            text: activeSwitch.checked ?
                tr.automatic_confirmation_description_if_active :
                tr.confirmation_by_user_enable_tip
        }

        DS3.Spacing {
            height: activeSwitch.checked ? 24 : 0
        }

        DS3.SettingsContainer {
            DS3.SettingsNavigationTitlePrimary {
                id: selectDevicesItem

                visible: activeSwitch.checked
                title: tr.select_devices
                subtitle: {
                    let verifyingDevices = alarmConfirmationSettings.verifying
                    let count = 0
                    for (var i = 0; i < verifyingDevices.length; i++) {
                        if (verifyingDevices[i][2] == true) {
                            count += 1
                        }
                    }
                    return count ? count : ""
                }

                onEntered: {
                    management.filtered_devices_for_verification_mode.invalidate()
                    let data = {
                        "verifying": alarmConfirmationSettings.verifying,
                        "devices_model": management.filtered_devices_for_verification_mode,
                        "mode": "verificationMode",
                        "emptyImage" : "qrc:/resources/images/desktop/icons/ic-no-select-devices.svg",
                        "parentRect": alarmConfirmationSettings,
                        "callback": checkWarningComment,
                    };
                    selectDeviceLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SelectDevicesForVerificationSettings.qml", data)
                }
            }
        }

        DS3.Spacing {
            height: selectDevicesItem.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.select_at_least_two_pd_devices
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.attention
            visible: {
                var count = 0
                for (var i = 0; i < verifying.length; i++) {
                    if (verifying[i][2] == true) {
                        count += 1
                    }
                }
                return count < 2 && activeSwitch.checked
            }
        }

        DS3.Spacing {
            height: selectDevicesItem.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            DS3.SettingsSliderValue {
                id: timeoutSlider

                enabled: devEnable
                value: hub.verification_timeout
                title: tr.confirmation_timer_min
                from: 30
                to: 60
                stepSize: 1
                suffix: tr.min
                visible: activeSwitch.checked
            }
        }

        DS3.Spacing {
            height: timeoutSlider.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.british_verification_timer_desc
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: timeoutSlider.visible
        }

        DS3.Spacing {
            height: timeoutSlider.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: tamperAlarmConfirm

                enabled: devEnable
                title: tr.second_open_lids_as_confirmation
                checked: hub.tamper_alarm_confirmation
                visible: activeSwitch.checked

                onSwitched: () => {
                    checked = !checked
                    checkWarningComment()
                }
            }
        }

        DS3.Spacing {
            height: tamperAlarmConfirm.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.second_open_lids_as_confirmation_tip
            color: ui.ds3.figure.secondary
            visible: tamperAlarmConfirm.visible
        }

        DS3.Spacing {
            height: tamperAlarmConfirm.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: alarmOnDelayedDevices

                enabled: devEnable
                title: tr.confirmed_alarm_on_delayed_devices
                checked: hub.confirmed_alarm_on_delayed_devices
                visible: hub.firmware_version_dec >= 209100 && activeSwitch.checked

                onSwitched: () => {
                    checked = !checked
                    checkWarningComment()
                }
            }
        }

        DS3.Spacing {
            height: alarmOnDelayedDevices.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.confirmed_alarm_on_delayed_devices_tip
            color: ui.ds3.figure.secondary
            visible: alarmOnDelayedDevices.visible
        }

        DS3.Spacing {
            height: holdUpAlarmSwitch.visible ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.single_hold_up_alarm
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: holdUpAlarmSwitch.visible
        }

        DS3.Spacing {
            height: holdUpAlarmSwitch.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            DS3.SettingsSwitch {
                id: holdUpAlarmSwitch

                enabled: devEnable
                title: tr.confirmation_by_user
                checked: hub.alarm_confirmation_hu_devices_pd6662
                visible: hub.hub_type != "YAVIR" && hub.firmware_version_dec >= 209100 && !serviceSettings.isWizard
            }
        }

        DS3.Spacing {
            height: holdUpAlarmSwitch.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: {
                if (holdUpAlarmSwitch.checked) {
                    return tr.confirmation_by_user_description_if_active
                } else {
                    return tr.confirmation_by_user_enable_tip
                }

            }
            style: ui.ds3.text.body.MRegular
            color: holdUpAlarmSwitch.checked ? ui.ds3.figure.secondary : ui.ds3.figure.attention
            visible: holdUpAlarmSwitch.visible
        }

        DS3.Spacing {
            height: selectHoldUpDevicesItem.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            DS3.SettingsNavigationTitlePrimary {
                id: selectHoldUpDevicesItem

                title: tr.select_devices
                subtitle: {
                    let holdUpVerifyingDevices = alarmConfirmationSettings.holdUpVerifying
                    let count = 0
                    for (var i = 0; i < holdUpVerifyingDevices.length; i++) {
                        if (holdUpVerifyingDevices[i][2] == true) {
                            count += 1
                        }
                    }
                    return count ? count : ""
                }
                visible: holdUpAlarmSwitch.checked && hub.hub_type != "YAVIR" && !serviceSettings.isWizard

                onEntered: {
                    let data = {
                        "verifying": alarmConfirmationSettings.holdUpVerifying,
                        "devices_model": management.filtered_devices_hold_up_verification,
                        "mode": "holdUpVerification",
                        "parentRect": alarmConfirmationSettings,
                        "callback": checkWarningComment,
                    };
                    selectDeviceLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SelectDevicesForVerificationSettings.qml", data)
                }
            }
        }

        DS3.Spacing {
            height: selectHoldUpDevicesItem.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.select_at_least_one_pd_device
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.attention
            visible: alarmConfirmationSettings.holdUpVerifyingDevicesCount < 1 &&
                holdUpAlarmSwitch.checked &&
                !serviceSettings.isWizard &&
                selectHoldUpDevicesItem.visible
        }

        DS3.Spacing {
            height: selectHoldUpDevicesItem.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            DS3.SettingsSliderValue {
                id: holdUptimeoutSlider

                enabled: devEnable
                value: hub.verification_timeout_hu
                title: tr.user_timer_hr
                from: 8
                to: 20
                stepSize: 1
                suffix: tr.hr
                visible: holdUpAlarmSwitch.checked  && !serviceSettings.isWizard && hub.hub_type != "YAVIR"
            }
        }

        DS3.Spacing {
            height: holdUptimeoutSlider.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.user_timer_hr_tip
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: holdUptimeoutSlider.visible
        }
    }

    Parts.ButtonNextCancelPD {
        id: saveButton

        currentStep: 1
        hasStepper: serviceSettings.isWizard
        buttonText: serviceSettings.isWizard ? tr.next: tr.save
        enabled: serviceSettings.isWizard ? true : devEnable && changesChecker.hasChanges
        commentText: tr.settings_are_not_PD6662_compliant
        commentColor: ui.ds3.figure.attention
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
        hasComment: {
            let count = 0

            for (var i = 0; i < alarmConfirmationSettings.verifying.length; i++) {
                if (alarmConfirmationSettings.verifying[i][2] == true) {
                    count += 1
                }
            }

            if (serviceSettings.isWizard &&
                (activeSwitch.checked != true || tamperAlarmConfirm.checked != false
                || alarmOnDelayedDevices.checked != false || count < 2)
            ) {
                return true
            }
            return false
        }

        button.onClicked: {
            Popups.please_wait_popup()

            var data = []
            var settings = {"type": "21", "id": hub.hub_id}

            // verification Mode
            settings["verification_enabled"] = activeSwitch.checked

            var selectedDevices = getResultSelectDevices(alarmConfirmationSettings.verifying,
                                                                 management.filtered_devices_for_verification_mode.verifying())

            var selectedHoldUpDevices = getResultSelectDevices(alarmConfirmationSettings.holdUpVerifying,
                                                        management.filtered_devices_hold_up_verification.verifying())

            selectedDevices.push(...selectedHoldUpDevices)

            for (let dev of selectedDevices) {
                let device_info = {}

                device_info["type"] = dev[0]
                device_info["id"] = dev[1]
                device_info["verifies_alarm"] = dev[2]

                data.push(device_info)
            }

            settings["verification_timeout"] = timeoutSlider.value

            // someValue | 0 - convert bool to int
            settings["tamper_alarm_confirmation"] = tamperAlarmConfirm.checked | 0
            settings["confirmed_alarm_on_delayed_devices"] = alarmOnDelayedDevices.checked | 0

            // Hold-up alarm
            settings["alarm_confirmation_hu_devices_pd6662"] = holdUpAlarmSwitch.checked | 0
            settings["verification_timeout_hu"] = holdUptimeoutSlider.value * 60

            data.push(settings)

             // if screen not compliant with PD
            if (saveButton.hasComment) {
                serviceSettings.notCompliantWizardScreens.push(tr.automatic_confirmation)
            }

            app.hub_management_module.update_objects_settings(data, {"emit_alt_signal": true})
        }
    }
}


