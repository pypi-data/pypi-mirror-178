import QtQuick 2.12

import "qrc:/resources/qml/components/911" as Custom
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups


Item {
    id: iconSettings

    width: 40
    height: 40

    opacity: enabled ? 1 : 0.4
    enabled: {
        if (!hub) return false

        // case with ARMING_INCOMPLETE - ?

        if (!deviceSettings) {
            // rooms & groups
            if (!disarmed) return false
            if (hub.two_stage_arming_progress_status > 1) return false
            if (!hub.current_user.room_edit_access) return false
            // groups edit access - ?
            return true
        }

        if (!device) return false
        if (device.obj_type == "21") {
            // hubs
            if (!hub.online && !disarmed) return true
            if (!disarmed) return false
            if (hub.two_stage_arming_progress_status > 1) return false
            return true
        }

        // devices
        if (!disarmed) return false
        if (hub.two_stage_arming_progress_status > 1) return false
        if (!hub.current_user.device_edit_access) return false
        return true
    }

    anchors {
        top: parent.top
        topMargin: 16
        right: parent.right
        rightMargin: 16
    }

    property var deviceSettings: true
    property var groupSetting: false
    property var bridgeOutput: 0

    property var disarmed: {
        if (!hub) return false

        if (hub.groups_enabled && ["NO_STATE_WITH_GROUPS_INFO", "DISARMED", "DISARMED_NIGHT_MODE_OFF"].includes(hub.state_with_groups)) return true
        if (!hub.groups_enabled && ["NO_STATE_INFO", "DISARMED"].includes(hub.state)) return true

        return false
    }

    /* ------------------------------------------------ */
    /* desktop tests */
    property var accessiblePrefix: ""
    /* ------------------------------------------------ */

    Image {
        id: iconSettingsIco

        source: "qrc:/resources/images/icons/a-settings-icon.svg"
        sourceSize.width: 40
        sourceSize.height: 40
        anchors.centerIn: parent
    }

    Custom.HandMouseArea {
        id: iconSettingsArea

        onClicked: {
            if (bridgeOutput) {
                return DesktopPopups.vhf_output_settings_popup(device, bridgeOutput)
            }
            if (deviceSettings) {
                DesktopPopups.device_settings_popup(device)
            } else if (groupSetting) {
                DesktopPopups.group_settings_popup(group)
            } else {
                DesktopPopups.room_settings_popup(room)
            }
        }

        /* -------------------------------------------- */
        /* desktop tests */
        Accessible.name: {
            if (!iconSettings.accessiblePrefix) return ""
            return __accessible_unique_ids__ ? iconSettings.accessiblePrefix + "_settings_button" : "settings_button"
        }
        Accessible.description: "<button enabled=" + Accessible.checkable + ">" + iconSettingsIco.source + "</button>"
        Accessible.role: Accessible.Button
        Accessible.checkable: visible && enabled
        Accessible.onPressAction: {
            if (!Accessible.checkable) return
            iconSettingsArea.clicked(true)
        }
        /* -------------------------------------------- */
    }
}
