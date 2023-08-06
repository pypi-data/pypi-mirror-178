import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    property var user: null
    property var devEnable: true
    property var sideMargin: 24

    Connections {
        target: app

        onActionSuccess: {
            changesChecker.changeInitialValues()
        }
    }

    anchors.fill: parent

    color: ui.backgrounds.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            malfunctionsSMS.checked,
            malfunctionsPush.checked,
            alertsCall.checked,
            alertsSMS.checked,
            alertsPush.checked,
            eventsSMS.checked,
            eventsPush.checked,
            armDisarmSMS.checked,
            armDisarmPush.checked
        ]
    }

    DS3.NavBarModal {
        id: notificationBar

        headerText: tr.notifications
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UserSettings.qml", {'user': user})
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: notificationBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin
        enabled: devEnable

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: viewNotifications

                title: tr.view_notifications_title
                visible: user.hub_role == "USER"
                checked: user.hub_role == "USER" ?
                    malfunctionsPush.checked || alertsPush.checked || eventsPush.checked || armDisarmPush.checked :
                    true

                onSwitched: () => {
                    checked = !checked
                    if (checked) {
                        malfunctionsPush.checked = user.malfunctions_push
                        alertsPush.checked = user.alarms_push
                        eventsPush.checked = user.events_push
                        armDisarmPush.checked = user.arm_push
                    } else {
                        malfunctionsPush.checked = false
                        alertsPush.checked = false
                        eventsPush.checked = false
                        armDisarmPush.checked = false
                    }
                }
            }
        }

        DS3.Spacing {
            height: viewNotifications.visible ? 4 : 0
        }

        DS3.Comment {
            width: parent.width

            text: tr.view_notifications_descr
            visible: viewNotifications.visible
        }

        DS3.Spacing {
            height: viewNotifications.visible ? 24 : 0
        }

        //--------------------- malfunctions --------------------------------------

        DS3.Text {
            text: tr.malfunctions
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: malfunctionsSMS

                title: tr.sms
                checked: user.malfunctions_sms
            }

            DS3.SettingsSwitch {
                id: malfunctionsPush

                title: tr.push
                checked: user.malfunctions_push
                visible: viewNotifications.checked
            }
        }

        DS3.Spacing {
            height: 24
        }

        //--------------------- alerts --------------------------------------

        DS3.Text {
            text: tr.alerts
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: alertsCall

                title: tr.call
                checked: user.alarms_call
            }

            DS3.SettingsSwitch {
                id: alertsSMS

                title: tr.sms
                checked: user.alarms_sms
            }

            DS3.SettingsSwitch {
                id: alertsPush

                title: tr.push
                checked: user.alarms_push
                visible: viewNotifications.checked
            }
        }

        DS3.Spacing {
            height: 24
        }

        //--------------------- events --------------------------------------

        DS3.Text {
            text: tr.events
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: eventsSMS

                title: tr.sms
                checked: user.events_sms
            }

            DS3.SettingsSwitch {
                id: eventsPush

                title: tr.push
                checked: user.events_push
                visible: viewNotifications.checked
            }
        }

        DS3.Spacing {
            height: 24
        }

        //--------------------- arm_disarm --------------------------------------

        DS3.Text {
            text: tr.arm_disarm
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            DS3.SettingsSwitch {
                id: armDisarmSMS

                title: tr.sms
                checked: user.arm_sms
            }

            DS3.SettingsSwitch {
                id: armDisarmPush

                title: tr.push
                checked: user.arm_push
                visible: viewNotifications.checked
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
            var settings = {
                "notification_settings": {
                    "malfunctions": [],
                    "alarms": [],
                    "events": [],
                    "armings": [],
                },
            }

            if (malfunctionsSMS.checked) {
                settings["notification_settings"]["malfunctions"].push("SMS")
            }
            if (malfunctionsPush.checked) {
                settings["notification_settings"]["malfunctions"].push("PUSH")
            }

            if (alertsCall.checked) {
                settings["notification_settings"]["alarms"].push("CALL")
            }
            if (alertsSMS.checked) {
                settings["notification_settings"]["alarms"].push("SMS")
            }
            if (alertsPush.checked) {
                settings["notification_settings"]["alarms"].push("PUSH")
            }

            if (eventsSMS.checked) {
                settings["notification_settings"]["events"].push("SMS")
            }
            if (eventsPush.checked) {
                settings["notification_settings"]["events"].push("PUSH")
            }

            if (armDisarmSMS.checked) {
                settings["notification_settings"]["armings"].push("SMS")
            }
            if (armDisarmPush.checked) {
                settings["notification_settings"]["armings"].push("PUSH")
            }

            Popups.please_wait_popup()
            app.hub_management_module.apply_update(management, user, settings)
        }
    }
}
