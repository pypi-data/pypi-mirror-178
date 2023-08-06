
import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: interconnectHubButton
    width: 26
    height: 26
    radius: 5
    color: ui.colors.yellow1

    property var fire_alarms: management ? management.devices.fire_alarms : null

//    if interconnect in delay
    visible: hub.hasOwnProperty("interconnect_state") && hub.interconnect_state == 1 && fire_alarms["fires"].length

    /*
    onVisibleChanged: {
        if (visible) {
            popup = Popups.interconnect_delay_popup(fire_alarms["fires"], fire_alarms["trigger"])
        } else {
            if (popup) { popup.close() }
        }
    }

    Component.onCompleted: {
        if (hub.interconnect_state == 1) {
            popup = Popups.interconnect_delay_popup(fire_alarms["fires"], fire_alarms["trigger"])
        }
    }
    */

    property var once: false
    property var popup: null

    anchors {
        verticalCenter: parent.verticalCenter
    }

    Image {
        width: 20
        height: 20

        source: "qrc:/resources/images/desktop/icons/interconnect_early_warning@2x.png"
        anchors.centerIn: parent
    }

    /*
    MouseArea {
        anchors.fill: parent

        onClicked: {
            Popups.interconnect_delay_popup(fire_alarms["fires"], fire_alarms["trigger"])
        }
    }
    */
}
