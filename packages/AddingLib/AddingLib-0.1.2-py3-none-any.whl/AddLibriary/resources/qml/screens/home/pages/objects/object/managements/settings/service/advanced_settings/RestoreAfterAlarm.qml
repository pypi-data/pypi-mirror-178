import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    id: restoreAfterAlarmSettings

    property var sideMargin: 24
    property var isPdComplete: {
        if (lidOpeningSwitch.checked || singleIntrusionAlarmSwitch.checked ||
                singleHoldUpAlarmSwitch.checked || confirmedIntrusionAlarmSwitch.checked ||
                confirmedHoldUpAlarmSwitch.checked
        ){
            return true
        }
        return false
    }

    function check() {
        let array = [
            lidOpeningSwitch.checked,
            singleIntrusionAlarmSwitch.checked,
            singleHoldUpAlarmSwitch.checked,
            confirmedIntrusionAlarmSwitch.checked,
            confirmedHoldUpAlarmSwitch.checked
        ]

        if ((array.filter((elem) => elem).length == 1) && management.devices.not_pd_devices_reset.length) {
            Popups.not_pd_compliant_devices_popup(management.devices.not_pd_devices_reset)
        }
    }

    Connections {
        target: app

        onAltActionSuccess: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SystemIntegrityCheck.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    Component.onCompleted: {
        if (serviceSettings.isWizard && lastScreen == 4) {

            lidOpeningSwitch.checked = true
            singleIntrusionAlarmSwitch.checked = true
            singleHoldUpAlarmSwitch.checked = true
            confirmedIntrusionAlarmSwitch.checked = true
            confirmedHoldUpAlarmSwitch.checked = true
            lastScreen += 1
        }

        if ( (hub.restore_required || serviceSettings.isWizard) && management.devices.not_pd_devices_reset.length) {
            Popups.not_pd_compliant_devices_popup(management.devices.not_pd_devices_reset)
        }

        // delete this screen from array if changed pd complient status
        let array = serviceSettings.notCompliantWizardScreens
        let index = array.indexOf(tr.reset_after_alarm)

        if (index != -1) {
            array.splice(index, 1)
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            lidOpeningSwitch.checked,
            singleIntrusionAlarmSwitch.checked,
            singleHoldUpAlarmSwitch.checked,
            confirmedIntrusionAlarmSwitch.checked,
            confirmedHoldUpAlarmSwitch.checked
        ]
    }

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }

    DS3.NavBarModal {
        id: restoreAfterAlarmBar

        headerText: tr.reset_after_alarm
        showBackArrow: true
        showCloseIcon: false
        isRound: false

        onBackAreaClicked: {
            if (serviceSettings.isWizard) {
                advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/PostAlarmIndication.qml")
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: restoreAfterAlarmBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.Text {
            width: parent.width

            text: tr.choose_alarm_reset_after
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
                id: lidOpeningSwitch

                enabled: devEnable
                title: tr.tamper_for_post_alarm
                checked: hub.restore_required.includes("TAMPER_ACTIVATION")

                onSwitched: () => {
                    checked = !checked
                    if (checked) restoreAfterAlarmSettings.check()
                }
            }

            DS3.SettingsSwitch {
                id: singleIntrusionAlarmSwitch

                enabled: devEnable
                title: tr.single_intrusion_alarm
                checked: hub.restore_required.includes("UNCONFIRMED_ALARMS")

                onSwitched: () => {
                    checked = !checked
                    if (checked) restoreAfterAlarmSettings.check()
                }
            }

            DS3.SettingsSwitch {
                id: singleHoldUpAlarmSwitch

                enabled: devEnable
                title: tr.single_hold_up_alarm
                checked: hub.restore_required.includes("UNCONFIRMED_HU_ALARMS")

                onSwitched: () => {
                    checked = !checked
                    if (checked) restoreAfterAlarmSettings.check()
                }
            }

            DS3.SettingsSwitch {
                id: confirmedIntrusionAlarmSwitch

                enabled: devEnable
                title: tr.confirmed_intrusion_alarm
                checked: hub.restore_required.includes("CONFIRMED_ALARMS")

                onSwitched: () => {
                    checked = !checked
                    if (checked) restoreAfterAlarmSettings.check()
                }
            }

            DS3.SettingsSwitch {
                id: confirmedHoldUpAlarmSwitch

                enabled: devEnable
                title: tr.confirmed_hold_up_alarm
                checked: hub.restore_required.includes("CONFIRMED_HU_ALARMS")

                onSwitched: () => {
                    checked = !checked
                    if (checked) restoreAfterAlarmSettings.check()
                }
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            text: {
                if (isPdComplete) {
                    return tr.reset_after_alarm_info
                } else {
                    return tr.enable_at_least_one_toggle_to_make_compliant
                }

            }
            style: ui.ds3.text.body.MRegular
            color: isPdComplete ? ui.ds3.figure.secondary : ui.ds3.figure.attention
        }

        DS3.Spacing {
            height: 24
        }
    }

    Parts.ButtonNextCancelPD {
        id: saveButton

        buttonText: serviceSettings.isWizard ? tr.next: tr.save
        enabled: serviceSettings.isWizard ? true : devEnable && changesChecker.hasChanges
        hasStepper: serviceSettings.isWizard
        stepAmount: 10
        currentStep: 5
        commentText: tr.settings_are_not_PD6662_compliant
        commentColor: ui.ds3.figure.attention
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
        hasComment: serviceSettings.isWizard && !isPdComplete

        button.onClicked: {
            var settings = {
                "restore_required": [],
                "_params": {"alt_action_success": true},
            }

            if (lidOpeningSwitch.checked) {
                settings["restore_required"].push("TAMPER_ACTIVATION")
            }
            if (singleIntrusionAlarmSwitch.checked) {
                settings["restore_required"].push("UNCONFIRMED_ALARMS")
            }
            if (singleHoldUpAlarmSwitch.checked) {
                settings["restore_required"].push("UNCONFIRMED_HU_ALARMS")
            }
            if (confirmedIntrusionAlarmSwitch.checked) {
                settings["restore_required"].push("CONFIRMED_ALARMS")
            }
            if (confirmedHoldUpAlarmSwitch.checked) {
                settings["restore_required"].push("CONFIRMED_HU_ALARMS")
            }

            // if screen not compliant with PD
            if (saveButton.hasComment) {
                serviceSettings.notCompliantWizardScreens.push(tr.reset_after_alarm)
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
