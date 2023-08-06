import QtQuick 2.12
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.13

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.Popup {
    id: popup

    property var hub: null
    property var user: hub.current_user
    property var sideMargin: 24

    property var compared_permissions: {
        // Installation Functionality. User story 4.31 (only installers might restore system)
        const restoration_permissions = appUser.company_id
            ? (companyAccess.HUB_AFTER_ALARM_RESTORE ? 31 : 0)
            : user.restore_permissions_bytes

        let permissions = hub.alarm_happened & restoration_permissions
        return permissions == hub.alarm_happened
    }

    property var management: null

    property var disarmed: {
        if (!hub) return false

        if (hub.groups_enabled && ["NO_STATE_WITH_GROUPS_INFO", "DISARMED", "DISARMED_NIGHT_MODE_OFF"].includes(hub.state_with_groups)) return true
        if (!hub.groups_enabled && ["NO_STATE_INFO", "DISARMED"].includes(hub.state)) return true

        return false
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }

        onActionFailed: {
            popup.close()
        }
    }

    Connections {
        target: hub

        onDataChanged: {
            if (hub.alarm_happened == 0) {
                popup.close()
            }
        }
    }

    width: 360

    title: tr.system_restore_required
    hasCrossButton: false

    Repeater {
        id: repeater

        model: {
            let restoreAlarms = [
                tr.confirmed_intrusion_alarm,
                tr.confirmed_hold_up_alarm,
                tr.single_intrusion_alarm,
                tr.single_hold_up_alarm,
                tr.tamper_for_post_alarm
            ];

            return restoreAlarms.filter( (elem, index) => {
                return hub.alarm_happened & (1 << index)
            })
        }

        DS3.Text {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            text: modelData
            style: ui.ds3.text.body.MRegular
            horizontalAlignment: Text.AlignHCenter
        }
    }

    DS3.Spacing {
        height: 16
    }

    DS3.Text {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        text: {
            if (!popup.disarmed) return tr.disarm_system_to_proceed
            if (hub.two_stage_arming_progress_status > 1) return tr.disarm_system_to_proceed
            return popup.compared_permissions ? tr.restore_system_after_alarms_or_deny_request : tr.prior_to_arm_request_for_system_restore
        }
        style: ui.ds3.text.body.MRegular
        horizontalAlignment: Text.AlignHCenter
    }

    DS3.Spacing {
        height: 32
    }

    ColumnLayout {
        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        spacing: 16

        DS3.ButtonContained {
            id: firstButton

            Layout.fillWidth: parent.width
            Layout.preferredHeight: height
            Layout.alignment: Qt.AlignHCenter
            enabled: {
                if (!popup.disarmed || hub.two_stage_arming_progress_status > 1) {
                    // 'need to disarm' case
                    if (!appUser.company_id) return hub.current_user.arm_access
                }
                return true
            }
            text: {
                if (!popup.disarmed) return tr.disarm
                if (hub.two_stage_arming_progress_status > 1) return tr.disarm
                return popup.compared_permissions ? tr.restore : tr.request_for_restore
            }

            onClicked: {
                if (!popup.disarmed || hub.two_stage_arming_progress_status > 1) {
                    app.hub_management_module.perform_security_action("DISARM", false)
                } else if (popup.compared_permissions) {
                    app.hub_management_module.hub_reset_alarm_condition(hub.hub_id)
                } else {
                    app.hub_management_module.request_arming_reset(hub.hub_id)
                }
            }
        }

        DS3.ButtonOutlined {
            id: secondButton

            Layout.fillWidth: parent.width
            Layout.preferredHeight: height
            Layout.alignment: Qt.AlignHCenter
            visible: {
                if (!popup.disarmed) return false
                if (hub.two_stage_arming_progress_status > 1) return false
                return popup.compared_permissions
            }
            text: tr.site_visit_required


            onClicked: {
                if (popup.compared_permissions) {
                    app.hub_management_module.engineer_attendance_required(hub.hub_id)
                }
            }
        }

        DS3.ButtonOutlined {
            id: thirdButton

            Layout.fillWidth: parent.width
            Layout.preferredHeight: height
            Layout.alignment: Qt.AlignHCenter
            text: tr.cancel

            onClicked: {
                popup.close()
            }
        }
    }
}