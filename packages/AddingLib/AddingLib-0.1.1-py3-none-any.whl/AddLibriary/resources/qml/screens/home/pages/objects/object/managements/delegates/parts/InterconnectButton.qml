
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: interconnectHubButton
    width: 26
    height: 26
    radius: 5
    color: ui.colors.red1

    property var fire_alarms: management ? management.devices.fire_alarms : null

    visible: {
        var state = (hub.fire_interconnected && fire_alarms["flag"])
        return state && hub.is_interconnected
    }

    /*
    onVisibleChanged: {
        if (visible) {
            popup = Popups.interconnect_popup(fire_alarms["fires"])
        } else {
            if (popup) { popup.close() }
        }
    }

    Component.onCompleted: {
        var state = (hub.fire_interconnected && fire_alarms["flag"])

        if (state && hub.hasOwnProperty("interconnect_delay_timeout") && !hub.interconnect_delay_timeout) {
            popup = Popups.interconnect_popup(fire_alarms["fires"])
        } else if (state && hub.hasOwnProperty("interconnect_state") && hub.interconnect_state == 3) {
            popup = Popups.interconnect_popup(fire_alarms["fires"])
        } else if (state && !hub.hasOwnProperty("interconnect_state")) {
            popup = Popups.interconnect_popup(fire_alarms["fires"])
        }
    }
    */

    property var once: false
    property var popup: null

    anchors {
        verticalCenter: parent.verticalCenter
    }

    Image {
        id: volumeImg
        width: 24
        height: 24
        visible: false

        source: "qrc:/resources/images/desktop/icons/ic-no-volume.svg"
        anchors.centerIn: parent
    }

    ColorOverlay {
        anchors.fill: volumeImg
        source: volumeImg
        color: ui.colors.white
    }

    /*
    MouseArea {
        anchors.fill: parent

        onClicked: {
            Popups.interconnect_popup(fire_alarms["fires"])
        }
    }
    */
}

