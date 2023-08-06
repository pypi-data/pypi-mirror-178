import QtQuick 2.7
import QtQuick.Controls 2.2


import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    property var sideMargin: 24

    Connections {
        target: app

        onAltActionSuccess: {
            verificationModeLoader.setSource("")
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            alarmRestorePicker.currentIndex,
            reportPanicAlarmSwitch.checked
        ]
    }

    DS3.NavBarModal {
        id: reportZoneRestoreBar

        headerText: tr.report_zone_restore
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            verificationModeLoader.setSource("")
        }
    }

    DS3.ScrollView {
        id: userSettings

        anchors {
            fill: undefined
            top: reportZoneRestoreBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsPickerTitleSecondary {
                id: alarmRestorePicker

                model: [tr.follow_zone, tr.at_disarm]
                atomTitle.title: tr.alarm_restore
                enabled: devEnable
                currentIndex: hub.report_alarm_restore - 1
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            text: tr.alarm_restore_info
            color: ui.ds3.figure.secondary
            style: ui.ds3.text.body.MRegular
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: reportPanicAlarmSwitch

                width: parent.width

                title: tr.report_panic_alarm_restore
                checked: hub.report_panic_alarm_restore == 2
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
                "report_alarm_restore": alarmRestorePicker.currentIndex + 1,
                "report_panic_alarm_restore": reportPanicAlarmSwitch.checked ? 2 : 1,
                "_params": {"alt_action_success": true},
            }

            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}