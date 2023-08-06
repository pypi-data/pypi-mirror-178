import QtQuick 2.7
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/"
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/"


Rectangle {
    anchors.fill: parent
    color: "#393939"
    border.width: 1
    border.color: ui.colors.dark1

    property var user: null

    Item {
        id: resetAfterAlarmLabel

        width: parent.width - 2
        height: 72

        anchors.top: parent.top

        Item {
            id: backItem
            height: parent.height
            width: backImage.width + 8 + backText.width

            anchors.left: parent.left
        }

        BackArea {
            backArea.onClicked: {
                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/users/UserSettings.qml", {'user': user})
            }
        }

        Text {
            id: labelText

            width: parent.width - backItem.width - 40

            text: tr.reset_after_alarm

            font.family: roboto.name
            font.pixelSize: 16
            font.weight: Font.Light
            color: ui.colors.light1
            wrapMode: Text.Wrap
            horizontalAlignment: Text.AlignHCenter

            anchors {
                left: backItem.right
//                leftMargin: 16
                verticalCenter: backItem.verticalCenter
            }
        }
    }

    ScrollView {
        id: resetAfterAlarm

        width: parent.width

        anchors {
            top: resetAfterAlarmLabel.bottom
            topMargin: 16
            bottom: saveCancel.top
        }

        Column {
            width: resetAfterAlarm.width
            anchors.fill: parent

            Rectangle {
                width: parent.width
                height: textLabel.height + 8
                color: "#504e4e"
                opacity: 1.0

                Text {
                    id: textLabel

                    width: parent.width - 48
                    height: contentHeight

                    text: tr.choose_alarm_reset_user_settings
                    color: ui.colors.light1

                    font.family: roboto.name
                    font.pixelSize: 14
                    font.weight: Font.Light
                    font.letterSpacing: 1
                    wrapMode: Text.Wrap
                    opacity: 0.6
                    horizontalAlignment: Text.AlignHCenter

                    anchors.centerIn: parent
                }
            }

             AjaxSettingsSwitch {
                id: lidOpeningSwitch

                enabled: devEnable

                height: 48
                width: view.width
                text: tr.tamper_for_post_alarm
                area.onClicked: {
                    checked = !checked
                }

                checked: user.restore_permissions.includes("RESTORE_TAMPER_ACTIVATION")
            }

            AjaxSettingsSwitch {
                id: singleIntrusionAlarmSwitch

                enabled: devEnable

                height: 48
                width: view.width
                text: tr.single_intrusion_alarm
                area.onClicked: {
                    checked = !checked
                }

                checked: user.restore_permissions.includes("RESTORE_UNCONFIRMED_ALARMS")
            }

            AjaxSettingsSwitch {
                id: singleHoldUpAlarmSwitch

                enabled: devEnable

                height: 48
                width: view.width
                text: tr.single_hold_up_alarm
                area.onClicked: {
                    checked = !checked
                }

                checked: user.restore_permissions.includes("RESTORE_UNCONFIRMED_HU_ALARMS")
            }

            AjaxSettingsSwitch {
                id: confirmedIntrusionAlarmSwitch

                enabled: devEnable

                height: 48
                width: view.width
                text: tr.confirmed_intrusion_alarm
                area.onClicked: {
                    checked = !checked
                }

                checked: user.restore_permissions.includes("RESTORE_CONFIRMED_ALARMS")
            }

            AjaxSettingsSwitch {
                id: confirmedHoldUpAlarmSwitch

                enabled: devEnable

                height: 48
                width: view.width
                text: tr.confirmed_hold_up_alarm
                area.onClicked: {
                    checked = !checked
                }

                checked: user.restore_permissions.includes("RESTORE_CONFIRMED_HU_ALARMS")
            }

            Item {
                width: parent.width
                height: hint.contentHeight + 16

                Text {
                    id: hint
                    width: parent.width - 80
                    font.family: roboto.name
                    font.pixelSize: 11
                    color: ui.colors.light1
                    opacity: 0.6
                    text: tr.reset_after_alarm_info
                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignLeft

                    anchors {
                        top: parent.top
                        topMargin: 4
                        horizontalCenter: parent.horizontalCenter
                    }
                }
            }
        }
    }

    AjaxSaveCancel {
        id: saveCancel
        anchors.bottom: parent.bottom

        cancelArea.onClicked: {
            systemRestoreLoader.setSource("")
        }

        saveArea.enabled: devEnable
        saveArea.onClicked: {
            var settings = {
                "restore_permissions": [],
                "_params": {
                    "alt_action_success": true,
                },
            }

            if (lidOpeningSwitch.checked) {
                settings["restore_permissions"].push("RESTORE_TAMPER_ACTIVATION")
            }
            if (singleIntrusionAlarmSwitch.checked) {
                settings["restore_permissions"].push("RESTORE_UNCONFIRMED_ALARMS")
            }
            if (singleHoldUpAlarmSwitch.checked) {
                settings["restore_permissions"].push("RESTORE_UNCONFIRMED_HU_ALARMS")
            }
            if (confirmedIntrusionAlarmSwitch.checked) {
                settings["restore_permissions"].push("RESTORE_CONFIRMED_ALARMS")
            }
            if (confirmedHoldUpAlarmSwitch.checked) {
                settings["restore_permissions"].push("RESTORE_CONFIRMED_HU_ALARMS")
            }

            app.hub_management_module.apply_update(management, user, settings)
        }
    }

    Connections {
        target: app

        onAltActionSuccess: {
            systemRestoreLoader.setSource("")
        }
    }
}
