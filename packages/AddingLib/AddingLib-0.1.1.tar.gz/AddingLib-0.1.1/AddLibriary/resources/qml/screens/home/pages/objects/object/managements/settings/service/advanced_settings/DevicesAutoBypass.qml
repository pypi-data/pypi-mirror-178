import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/parts" as Parts


Rectangle {
    property var sideMargin: 24

    Connections {
        target: app

        property string loaderSource: {
            if (serviceSettings.isWizard) {
                if (hub.hub_type == "YAVIR") {
                    return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/SystemIntegrityCheck.qml"
                } else {
                    return "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/PostAlarmIndication.qml"
                }
            } else {
                return ""
            }
        }

        onActionSuccess: {
            advancedSettingsLoader.setSource(loaderSource)
        }
    }

    Component.onCompleted: {
        let currentStep = hub.hub_type == "YAVIR" ? 1 : 2
        if (serviceSettings.isWizard && lastScreen == currentStep) {
            autoBypassSwitch.checked = true
            bypassTimer.value = hub.verification_timeout
            lastScreen += 1
        }

        // delete this screen from array if changed pd complient status
        let array = serviceSettings.notCompliantWizardScreens
        let index = array.indexOf(tr.auto_bypass)

        if (index != -1) {
            array.splice(index, 1)
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: {
            let changes_list = [autoBypassSwitch.checked, numberOfAlarmsCombobox.currentIndex]
            if (autoBypassSwitch.checked) {
                changes_list.push(bypassTimer.value)
            }
            return changes_list
        }
    }

    DS3.MouseArea {
        cursorShape: Qt.ArrowCursor
    }

    DS3.NavBarModal {
        id: devicesAutoBypassBar

        headerText: tr.auto_bypass
        showBackArrow: true
        showCloseIcon: false
        isRound: false

        onBackAreaClicked: {
            if (serviceSettings.isWizard) {
                if (hub.hub_type == "YAVIR") {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/advanced_settings/AlarmConfirmation.qml")
                } else {
                    advancedSettingsLoader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/service/wizard/WizardHoldUpAlarmConfirm.qml")
                }
            } else {
                advancedSettingsLoader.setSource("")
            }
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: devicesAutoBypassBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: autoBypassSwitch

                enabled: devEnable
                title: tr.auto_bypass_activate
                checked: hub.auto_bypass_timer_minutes != 0
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: bypassTimer

                enabled: devEnable
                value: hub.auto_bypass_timer_minutes
                title: tr.auto_bypass_timer
                from: 1
                to: 60
                stepSize: 1
                suffix: tr.min
                visible: autoBypassSwitch.checked && hub.hub_type != "YAVIR"
            }
        }

        DS3.Spacing {
            height: bypassTimer.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            visible: bypassTimer.visible
            text: {
                if (hub.verification_enabled) {
                    bypassTimer.value != hub.verification_timeout ?
                    tr.set_same_value_as_for_intrusion_confirmation_timer :
                    tr.auto_bypass_timer_info
                } else {
                    bypassTimer.value >= 30 ?
                    tr.auto_bypass_timer_info :
                    tr.timer_at_least_30_minutes_for_PD
                }
            }
            color: {
                if ((hub.verification_enabled &&
                    bypassTimer.value != hub.verification_timeout) || bypassTimer.value < 30
                ) {
                    return ui.ds3.figure.attention
                }
                return ui.ds3.figure.secondary
            }
        }

        DS3.Spacing {
            height: bypassTimer.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsPickerTitleSecondary {
                id: numberOfAlarmsCombobox

                model: {
                    var alarm_numbers = [];

                    for (let i = 1; i < 16; i++ ) {
                        alarm_numbers.push(i)
                    }
                    alarm_numbers.unshift(tr.off)

                    return alarm_numbers
                }
                currentIndex: hub.auto_bypass_counter
                atomTitle.title: tr.bypass_on_automatically_by_numbers
                visible: !serviceSettings.isWizard
            }
        }

        DS3.Spacing {
            height: numberOfAlarmsCombobox.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.auto_bypass_active_by_numbers_info
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            visible: numberOfAlarmsCombobox.visible
        }

        DS3.Spacing {
            height: numberOfAlarmsCombobox.visible ? 24 : 0
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.CommentImportant {
                atomTitle.title: tr.no_bypass_mode_in_active_mode
                status: DS3.CommentImportant.Status.Attention
            }
        }
    }

    Parts.ButtonNextCancelPD {
        id: saveButton

        hasStepper: serviceSettings.isWizard
        buttonText: serviceSettings.isWizard ? tr.next: tr.save
        enabled: serviceSettings.isWizard ? true : devEnable && changesChecker.hasChanges
        currentStep: hub.hub_type == "YAVIR" ? 2 : 3
        hasComment: {
            if (serviceSettings.isWizard && (
                (hub.verification_enabled &&
                    (bypassTimer.value != hub.verification_timeout || !autoBypassSwitch.checked)
                ) || bypassTimer.value < 30 || !autoBypassSwitch.checked)
            ) {
                return true
            }
            return false
        }

        commentText: tr.settings_are_not_PD6662_compliant
        commentColor: ui.ds3.figure.attention
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"

        button.onClicked: {
            var settings = {
                "auto_bypass_timer_minutes": autoBypassSwitch.checked ? bypassTimer.value : 0,
                "auto_bypass_counter": numberOfAlarmsCombobox.currentIndex,
            }

            //  if screen not compliant with PD
            if (saveButton.hasComment) {
                serviceSettings.notCompliantWizardScreens.push(tr.auto_bypass)
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}

