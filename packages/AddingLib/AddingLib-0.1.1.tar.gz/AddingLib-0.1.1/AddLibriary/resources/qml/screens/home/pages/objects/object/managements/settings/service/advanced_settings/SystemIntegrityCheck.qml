import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    property var sideMargin: 24
    property var armPreventionToCheckPdComplete: {
        if (checkHubBatteryLevel.checked || checkHubExternalPower.checked ||
            checkHubTamper.checked || checkHighNoiseLevel.checked ||
            checkATSFault.checked || checkARCPoll.checked) {

            return true
        }
        return false
    }

    Connections {
        target: app

        property string loaderSource: {
            if (serviceSettings.isWizard) {
                if (hub.hub_type == "YAVIR" || hub.hub_type == "YAVIR_PLUS") {
                    return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/FinalWizardScreen.qml"
                } else {
                    return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/ArmingDisarmingFlow.qml"
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
        let currentStep = 5
        if (hub.hub_type == "YAVIR") {
            let currentStep = 2
        } else if (hub.hub_type == "YAVIR_PLUS") {
            let currentStep = 4
        }
        if (serviceSettings.isWizard && lastScreen == currentStep) {
            // armPreventionMode
            checkSystemSwitch.checked = true

            // armPreventionsToCheck
            checkHubBatteryLevel.checked = true
            checkHubExternalPower.checked = true
            checkHubTamper.checked = true
            checkHighNoiseLevel.checked = true
            checkATSFault.checked = true
            checkARCPoll.checked = true

            armAccessSwitch.checked = true
            lastScreen += 1
        }

        // delete this screen from array if changed pd complient status
        let array = serviceSettings.notCompliantWizardScreens
        let index = array.indexOf(tr.prevention_of_arming)

        if (index != -1) {
            array.splice(index, 1)
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: {
            if (!checkSystemSwitch.checked) {
                return [checkSystemSwitch.checked]
            } else {
                return [
                    checkSystemSwitch.checked,
                    checkHubBatteryLevel.checked,
                    checkHubExternalPower.checked,
                    checkHubTamper.checked,
                    checkHighNoiseLevel.checked,
                    checkATSFault.checked,
                    checkARCPoll.checked,
                    armAccessSwitch.checked
                ]
            }
        }
    }

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }

    DS3.NavBarModal {
        id: systemIntegrityCheckBar

        headerText: tr.prevention_of_arming
        showBackArrow: true
        showCloseIcon: false
        isRound: false

        onBackAreaClicked: {
            if (serviceSettings.isWizard) {

                let advanced_path = "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/"

                if (hub.hub_type == "YAVIR") {
                    advancedSettingsLoader.setSource(advanced_path + "DevicesAutoBypass.qml")
                } else if (hub.hub_type == "YAVIR_PLUS") {
                    advancedSettingsLoader.setSource(advanced_path + "PostAlarmIndication.qml")
                } else {
                    advancedSettingsLoader.setSource(advanced_path + "RestoreAfterAlarm.qml")
                }
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: systemIntegrityCheckBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: checkSystemSwitch

                enabled: devEnable
                title: tr.prevention_of_arming
                checked: hub.arm_prevention_mode > 1

                onSwitched: () => {
                    checked = !checked
                    if (checked) armAccessSwitch.checked = true
                }
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: checkSystemSwitch.checked ? tr.prevention_of_arming_hint : tr.jeweller_warning
            color: checkSystemSwitch.checked ? ui.ds3.figure.secondary : ui.ds3.figure.attention
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.special.SectionCaps
            text: tr.hub_preventions
            color: ui.ds3.figure.secondary
            visible: hubStates.visible
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            id: hubStates

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: checkSystemSwitch.checked && hub.firmware_version_dec >= 209100

            DS3.SettingsSwitch {
                id: checkHubBatteryLevel

                enabled: devEnable
                title: tr.check_hub_battery_level
                checked: hub.arm_preventions_to_check.includes("LOW_BATTERY_CHARGE")
            }

            DS3.SettingsSwitch {
                id: checkHubExternalPower

                enabled: devEnable
                title: tr.check_hub_external_power
                checked: hub.arm_preventions_to_check.includes("NO_EXTERNAL_POWER")
            }

             DS3.SettingsSwitch {
                id: checkHubTamper

                enabled: devEnable
                title: tr.check_hub_tamper
                checked: hub.arm_preventions_to_check.includes("TAMPERED")
            }

            DS3.SettingsSwitch {
                id: checkHighNoiseLevel

                enabled: devEnable
                title: tr.check_high_noise_level
                checked: hub.arm_preventions_to_check.includes("HIGH_NOISE_LEVEL")
            }

            DS3.SettingsSwitch {
                id: checkATSFault

                enabled: devEnable
                title: tr.check_ats_fault
                checked: hub.arm_preventions_to_check.includes("NO_SERVER_CONNECTION")
            }

            DS3.SettingsSwitch {
                id: checkARCPoll

                enabled: devEnable
                title: tr.check_arc_poll
                checked: hub.arm_preventions_to_check.includes("NO_CMS_CONNECTION")
            }
        }

        DS3.Spacing {
            height: hubStates.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: {
                if (!(checkHubBatteryLevel.checked ||
                    checkHubExternalPower.checked ||
                    checkHubTamper.checked ||
                    checkHighNoiseLevel.checked ||
                    checkATSFault.checked ||
                    checkARCPoll.checked)) {
                    return tr.settings_are_not_PD6662_compliant
                }
                return tr.if_toggle_not_active_no_system_integrity_check
            }
            color: {
                if (!(checkHubBatteryLevel.checked ||
                    checkHubExternalPower.checked ||
                    checkHubTamper.checked ||
                    checkHighNoiseLevel.checked ||
                    checkATSFault.checked ||
                    checkARCPoll.checked)) {
                        return ui.ds3.figure.attention
                }
                return ui.ds3.figure.secondary
            }
            visible: hubStates.visible
        }

        DS3.Spacing {
            height: hubStates.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: armAccessSwitch

                enabled: devEnable
                title: tr.override_prevention_of_arming
                checked: hub.arm_prevention_mode == 2
                visible: checkSystemSwitch.checked
            }
        }

        DS3.Spacing {
            height: armAccessSwitch.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.override_prevention_of_arming_hint
            color: ui.ds3.figure.secondary
            visible: armAccessSwitch.visible
        }
    }

    Parts.ButtonNextCancelPD {
        id: saveButton

        buttonText: serviceSettings.isWizard ? tr.next: tr.save
        enabled: serviceSettings.isWizard ? true : devEnable && changesChecker.hasChanges
        hasStepper: serviceSettings.isWizard
        stepAmount: {
            if (hub.hub_type == "YAVIR") {
                return 5
            } else if (hub.hub_type == "YAVIR_PLUS") {
                return 7
            } else {
                return 10
            }
        }
        currentStep: {
            if (hub.hub_type == "YAVIR") {
                return 3
            } else if (hub.hub_type == "YAVIR_PLUS") {
                return 5
            } else {
                return 6
            }
        }
        commentText: tr.settings_are_not_PD6662_compliant
        commentColor: ui.ds3.figure.attention
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
        hasComment: serviceSettings.isWizard && (!checkSystemSwitch.checked || !armPreventionToCheckPdComplete)


        button.onClicked: {
            var settings = {
                "arm_preventions_to_check": [],
                "_params": {"alt_action_success": true},
            }

            // arm_prevention_mode
            var armPreventionMode = 0
            if (checkSystemSwitch.checked) {
                armPreventionMode = armAccessSwitch.checked ? 2 : 3
            } else {
                armPreventionMode = 1
            }
            if (armPreventionMode != hub.arm_prevention_mode) {
                settings["arm_prevention_mode"] = armPreventionMode
            }

            // arm_preventions_to_check
            if (checkHubBatteryLevel.checked) {
                settings["arm_preventions_to_check"].push("LOW_BATTERY_CHARGE")
            }
            if (checkHubExternalPower.checked) {
                settings["arm_preventions_to_check"].push("NO_EXTERNAL_POWER")
            }
            if (checkHubTamper.checked) {
                settings["arm_preventions_to_check"].push("TAMPERED")
            }
            if (checkHighNoiseLevel.checked) {
                settings["arm_preventions_to_check"].push("HIGH_NOISE_LEVEL")
            }
            if (checkATSFault.checked) {
                settings["arm_preventions_to_check"].push("NO_SERVER_CONNECTION")
            }
            if (checkARCPoll.checked) {
                settings["arm_preventions_to_check"].push("NO_CMS_CONNECTION")
            }

            // if screen not compliant with PD
            if (saveButton.hasComment) {
                serviceSettings.notCompliantWizardScreens.push(tr.prevention_of_arming)
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
