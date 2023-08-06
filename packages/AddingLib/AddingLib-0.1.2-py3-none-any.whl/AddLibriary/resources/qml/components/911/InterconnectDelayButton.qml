import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups

Rectangle {
    width: interconnectDelayHubButton.width + 26
    height: 32
    radius: 16
    color: ui.colors.yellow1

    opacity: enabled ? 1 : 0.2
    enabled: companyAccess.HUB_INTERCONNECT_PROCESS && management.facility_access

    property var popup: null
    property var fire_alarms: management.devices.fire_alarms

    // if interconnect in delay
    visible: {
        if (true) {

            let state = hub && hub.hasOwnProperty("interconnect_state") && (hub.interconnect_state == 1) && fire_alarms["fires"].length

            systemState.interconnectDelayButtonVisible = state
            return state
        } else {
            systemState.interconnectDelayButtonVisible = false
            return false
        }
    }

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

    Row {
        id: interconnectDelayHubButton

        height: parent.height
        anchors.centerIn: parent
        spacing: 12

        Image {
            width: 20
            height: 20

            source: "qrc:/resources/images/desktop/icons/interconnect_early_warning@2x.png"
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            text: tr.delay_interconnect_in_action_bar
            font.family: roboto.name
            font.pixelSize: 14
            font.weight: Font.Light
            color: "black"

            anchors.verticalCenter: parent.verticalCenter
        }
    }

    MouseArea {
        anchors.fill: parent

        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: {
            Popups.interconnect_delay_popup(management.devices.fire_alarms["fires"], management.devices.fire_alarms["trigger"], management)
        }
    }

}