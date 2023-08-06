import QtQuick 2.13
import QtQuick.Controls 2.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom


Image {
    width: 24
    height: 24

    property var hub: management.devices.hub

    visible: {
        if (!hub || !hub.online || !hub.chimes_available || !hub.current_user.chimes_activation_access) return false
        if (hub.groups_enabled) return (management.groups.chimes_all_ready_groups_exist || management.groups.chimes_half_ready_groups_exist)
        return hub.chimes_status != "NOT_READY"
    }
    source: {
        if (hub && hub.groups_enabled) {
            if (!management.groups.chimes_all_ready_groups_exist)
                return "qrc:/resources/images/desktop/chimes/ChimesProblem.svg"
            if (management.groups.chimes_enabled_groups_exist)
                return "qrc:/resources/images/desktop/chimes/TurnChimesOff.svg"
            return "qrc:/resources/images/desktop/chimes/TurnChimesOn.svg"
        } else {
            if (hub && hub.chimes_status == "HALF_READY")
                return "qrc:/resources/images/desktop/chimes/ChimesProblem.svg"
            if (hub && hub.chimes_status == "ENABLED")
                return "qrc:/resources/images/desktop/chimes/TurnChimesOff.svg"
            return "qrc:/resources/images/desktop/chimes/TurnChimesOn.svg"
        }
    }

    Custom.HandMouseArea {
        onClicked: {
            if (!hub.groups_enabled && hub.chimes_status != "HALF_READY") {
                Popups.please_wait_popup()
                app.chimes_module.hub_chimes_action(hub.chimes_status != "ENABLED")
            }
            else Popups.chimes_activation_popup()
        }
    }
}
