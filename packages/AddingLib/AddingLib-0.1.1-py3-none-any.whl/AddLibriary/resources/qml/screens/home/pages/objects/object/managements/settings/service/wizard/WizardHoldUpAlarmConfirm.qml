import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts

Rectangle {
    id: wizardHoldUpAlarmConfirmScreen

    property var sideMargin: 24
    property var holdUpVerifying: management.filtered_devices_hold_up_verification.verifying()
    property var holdUpDevicesAvailable: management.filtered_devices_hold_up_verification.length

    function checkWarningComment() {
        // check if added at least one holdUp device
        if (!holdUpDevicesAvailable) {
            nextButton.hasComment = false
            return
        }

        let count = 0

        for (var i = 0; i < wizardHoldUpAlarmConfirmScreen.holdUpVerifying.length; i++) {
            if (wizardHoldUpAlarmConfirmScreen.holdUpVerifying[i][2] == true) {
                count += 1
            }
        }

        if (serviceSettings.isWizard &&
            (holdUpAlarmSwitch.checked != true || !count)
        ) {
            nextButton.hasComment = true
            return
        }
        nextButton.hasComment = false
    }

    function getResultSelectDevices(arr1, arr2) {
        let result = arr1.filter((elem) => arr2.every((sub) => (elem[1] != sub[1] || elem[2] != sub[2])))
        return result
    }

    Component.onCompleted: {
        if (lastScreen == 1) {
            // check if added at least one holdUp device
            if (holdUpDevicesAvailable) {
                holdUpAlarmSwitch.checked = true
            } else {
                holdUpAlarmSwitch.checked = false
            }
            holdUptimeoutSlider.value = 8
            lastScreen += 1
        }
        // delete this screen from array if changed pd complient status
        let array = serviceSettings.notCompliantWizardScreens
        let index = array.indexOf(tr.confirmation_by_user)

        if (index != -1) {
            array.splice(index, 1)
        }
        checkWarningComment()
    }

    Connections {
        target: app

        onAltActionSuccess: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/DevicesAutoBypass.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    height: parent.height

    color: ui.ds3.bg.base

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
        id: wizardHoldUpAlarmConfirmBar

        headerText: tr.british_standard_setting_updated
        showBackArrow: true
        showCloseIcon: false
        isRound: false

        onBackAreaClicked: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/AlarmConfirmation.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: wizardHoldUpAlarmConfirmBar.bottom
            bottom: nextButton.top
            left: parent.left
            right: parent.right
        }

        width: parent.width

        padding: sideMargin

        DS3.Text {
            width: parent.width

            text: tr.hold_up_alarm
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
            visible: holdUpAlarmSwitch.visible
        }

        DS3.Spacing {
            height: holdUpAlarmSwitch.visible ? 4 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: holdUpAlarmSwitch

                enabled: devEnable
                title: tr.confirmation_by_user
                checked: hub.alarm_confirmation_hu_devices_pd6662
                visible: hub.firmware_version_dec >= 209100

                onSwitched: () => {
                    checked = !checked
                    checkWarningComment()
                }
            }
        }

        DS3.Spacing {
            height: holdUpAlarmSwitch.visible && holdUpDevicesAvailable ? 4 : 0
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
            visible: holdUpAlarmSwitch.visible && holdUpDevicesAvailable
        }

        DS3.Spacing {
            height: holdUpAlarmSwitch.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsNavigationTitlePrimary {
                id: selectHoldUpDevicesItem

                visible: holdUpAlarmSwitch.checked
                title: tr.select_devices
                subtitle: {
                    let holdUpVerifyingDevices = wizardHoldUpAlarmConfirmScreen.holdUpVerifying
                    let count = 0
                    for (var i = 0; i < holdUpVerifyingDevices.length; i++) {
                        if (holdUpVerifyingDevices[i][2] == true) {
                            count += 1
                        }
                    }
                    return count ? count : ""
                }

                onEntered: {
                    let data = {
                        "verifying": wizardHoldUpAlarmConfirmScreen.holdUpVerifying,
                        "devices_model": management.filtered_devices_hold_up_verification,
                        "mode": "holdUpVerification",
                        "parentRect": wizardHoldUpAlarmConfirmScreen,
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
            visible: {
                var count = 0

                for (var i = 0; i < wizardHoldUpAlarmConfirmScreen.holdUpVerifying.length; i++) {
                    if (wizardHoldUpAlarmConfirmScreen.holdUpVerifying[i][2] == true) {
                        count += 1
                    }
                }
                return count < 1 && holdUpAlarmSwitch.checked
            }
        }

        DS3.Spacing {
            height: selectHoldUpDevicesItem.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: holdUptimeoutSlider

                enabled: devEnable
                value: hub.verification_timeout_hu
                title: tr.user_timer_hr
                from: 8
                to: 20
                stepSize: 1
                suffix: tr.hr
                visible: holdUpAlarmSwitch.checked
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
        id: nextButton

        currentStep: 2
        commentText: tr.settings_are_not_PD6662_compliant
        commentColor: ui.ds3.figure.attention
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
        hasComment: {
            // check if added at least one holdUp device
            if (!holdUpDevicesAvailable) return false

            let count = 0

            for (var i = 0; i < wizardHoldUpAlarmConfirmScreen.holdUpVerifying.length; i++) {
                if (wizardHoldUpAlarmConfirmScreen.holdUpVerifying[i][2] == true) {
                    count += 1
                }
            }

            if (serviceSettings.isWizard &&
                (holdUpAlarmSwitch.checked != true || !count)
            ) {
                return true
            }
            return false
        }

        button.onClicked: {
            Popups.please_wait_popup()
            var data = []
            var settings = {"type": 21, "id": hub.hub_id}

            var holdUpDevices = getResultSelectDevices(wizardHoldUpAlarmConfirmScreen.holdUpVerifying,
                                                        management.filtered_devices_hold_up_verification.verifying())

            for (let dev of holdUpDevices) {
                let device_info = {}

                device_info["type"] = dev[0]
                device_info["id"] = dev[1]
                device_info["verifies_alarm"] = dev[2]

                data.push(device_info)
            }

            // Hold-up alarm
            settings["alarm_confirmation_hu_devices_pd6662"] = holdUpAlarmSwitch.checked | 0
            settings["verification_timeout_hu"] = holdUptimeoutSlider.value * 60

            data.push(settings)

            // if screen not compliant with PD
            if (nextButton.hasComment) {
                serviceSettings.notCompliantWizardScreens.push(tr.confirmation_by_user)
            }

            app.hub_management_module.update_objects_settings(data, {"emit_alt_signal": true})
        }
    }
}


