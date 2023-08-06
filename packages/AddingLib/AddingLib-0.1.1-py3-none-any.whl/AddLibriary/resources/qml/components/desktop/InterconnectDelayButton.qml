import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups

Rectangle {
    id: interconnectHubButton
    width: 26
    height: 26
    radius: 5
    color: ui.colors.yellow1

    property var fire_alarms: management.devices.fire_alarms

//    if interconnect in delay
    visible: hub.hasOwnProperty("interconnect_state") && hub.interconnect_state == 1 && fire_alarms["fires"].length

    onVisibleChanged: {
        if (visible) {
            popup = Popups.interconnect_delay_popup(fire_alarms["fires"], fire_alarms["trigger"], management)
        } else {
            if (popup) { popup.close() }
        }
    }

    Component.onCompleted: {
        if (hub.interconnect_state == 1) {
            popup = Popups.interconnect_delay_popup(fire_alarms["fires"], fire_alarms["trigger"], management)
        }
    }

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


    MouseArea {
        anchors.fill: parent

        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: {
            Popups.interconnect_delay_popup(fire_alarms["fires"], fire_alarms["trigger"], management)
        }
    }
}