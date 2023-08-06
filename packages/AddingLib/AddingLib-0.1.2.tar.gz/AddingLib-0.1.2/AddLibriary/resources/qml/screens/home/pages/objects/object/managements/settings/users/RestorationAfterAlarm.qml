import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    property var user: null
    property var devEnable: true
    property var sideMargin: 24

    Connections {
        target: app

        onAltActionSuccess: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UserSettings.qml", {"user": user})
        }
    }

    anchors.fill: parent

    color: ui.backgrounds.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            tamperForPostAlarm.checked,
            singleIntrusionAlarm.checked,
            singleHoldUpAlarm.checked,
            confirmedIntrusionAlarm.checked,
            confirmedHoldUpAlarm.checked
        ]
    }

    DS3.NavBarModal {
        id: restorationAfterAlarmBar

        headerText: tr.reset_after_alarm
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UserSettings.qml", {'user': user})
        }
    }

    DS3.ScrollView {
        id: scroll

        anchors {
            fill: undefined
            top: restorationAfterAlarmBar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: sideMargin
        enabled: devEnable

        //--------------------- malfunctions --------------------------------------
        DS3.Text {
            id: chooseAlarmResetUserSettings

            text: tr.choose_alarm_reset_user_settings
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.SettingsContainer {
            id: chooseAlarmResetUserSettingsContainer

            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: tamperForPostAlarm

                title: tr.tamper_for_post_alarm
                checked: user.restore_permissions.includes("RESTORE_TAMPER_ACTIVATION")
            }

            DS3.SettingsSwitch {
                id: singleIntrusionAlarm

                title: tr.single_intrusion_alarm
                checked: user.restore_permissions.includes("RESTORE_UNCONFIRMED_ALARMS")
            }

            DS3.SettingsSwitch {
                id: singleHoldUpAlarm

                title: tr.single_hold_up_alarm
                checked: user.restore_permissions.includes("RESTORE_UNCONFIRMED_HU_ALARMS")
            }

            DS3.SettingsSwitch {
                id: confirmedIntrusionAlarm

                title: tr.confirmed_intrusion_alarm
                checked: user.restore_permissions.includes("RESTORE_CONFIRMED_ALARMS")
            }

            DS3.SettingsSwitch {
                id: confirmedHoldUpAlarm

                title: tr.confirmed_hold_up_alarm
                checked:  user.restore_permissions.includes("RESTORE_CONFIRMED_HU_ALARMS")
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            text: tr.reset_after_alarm_info
            style: ui.ds3.text.body.MRegular
            color: ui.colors.nonessential
            verticalAlignment: Text.AlignVCenter
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
            var settings = {
                "restore_permissions": [],
                "_params": {
                    "alt_action_success": true,
                },
            }

            if (tamperForPostAlarm.checked) {
                settings["restore_permissions"].push("RESTORE_TAMPER_ACTIVATION")
            }
            if (singleIntrusionAlarm.checked) {
                settings["restore_permissions"].push("RESTORE_UNCONFIRMED_ALARMS")
            }
            if (singleHoldUpAlarm.checked) {
                settings["restore_permissions"].push("RESTORE_UNCONFIRMED_HU_ALARMS")
            }
            if (confirmedIntrusionAlarm.checked) {
                settings["restore_permissions"].push("RESTORE_CONFIRMED_ALARMS")
            }
            if (confirmedHoldUpAlarm.checked) {
                settings["restore_permissions"].push("RESTORE_CONFIRMED_HU_ALARMS")
            }

            app.hub_management_module.apply_update(management, user, settings)
        }
    }
}
