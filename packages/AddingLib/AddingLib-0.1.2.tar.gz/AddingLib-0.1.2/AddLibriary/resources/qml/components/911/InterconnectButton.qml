import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    height: 32
    width: interconnectHubButton.width + 26
    radius: 16
    color: "#f64347"

    opacity: enabled ? 1 : 0.2
    enabled: companyAccess.HUB_INTERCONNECT_PROCESS && management.facility_access

    property var popup: null

    visible: {
        var state = (hub && hub.fire_interconnected && management && management.devices && management.devices.fire_alarms["flag"])
        var isHubInterconnected = state && device.is_interconnect_delay_available
        systemState.interconnectButtonVisible = isHubInterconnected
        return isHubInterconnected
    }

    onVisibleChanged: {
        if (visible) {
            popup = Popups.interconnect_popup(management.devices.fire_alarms["fires"], management)
        } else {
            if (popup) { popup.close() }
        }
    }

    Component.onCompleted: {
        var fires = management.devices.fire_alarms
        var state = hub.fire_interconnected && fires["flag"]

        if (state && hub.is_interconnected) popup = Popups.interconnect_popup(fires["fires"], null, fires["isCriticalCOAlarm"]))
    }

    Row {
        id: interconnectHubButton

        height: 26
        anchors.centerIn: parent
        spacing: 12

        property var once: false
        property var popup: null

        Item {
            width: 24
            height: parent.height

            anchors.verticalCenter: parent.verticalCenter

            DS3.Icon {
                id: noVolumeImg

                visible: false
                source: "qrc:/resources/images/desktop/icons/ic-no-volume.svg"
                anchors.centerIn: parent
            }

            ColorOverlay {
                anchors.fill: noVolumeImg
                source: noVolumeImg
                color: ui.colors.light1
            }
        }

        Text {

            width: contentWidth
            text: tr.interconnect
            font.family: roboto.name
            font.pixelSize: 14
            font.weight: Font.Light
            color: ui.colors.light1

            anchors.verticalCenter: parent.verticalCenter
        }
    }

    MouseArea {
        anchors.fill: parent

        hoverEnabled: true
        cursorShape: Qt.PointingHandCursor

        onClicked: {
            Popups.interconnect_popup(management.devices.fire_alarms["fires"], management, management.devices.fire_alarms["isCriticalCOAlarm"])
        }
    }
}