import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/desktop/popups.js" as Popups

Rectangle {
    width: restoreAlarmButton.width + 26
    height: 32
    radius: 16
    color: "#f64347"

    opacity: enabled ? 1 : 0.2
    enabled: companyAccess.HUB_AFTER_ALARM_RESTORATION_REQUEST || companyAccess.HUB_AFTER_ALARM_RESTORE

    visible: {
        if (true) {

            if (hub && hub.alarm_happened) {
                systemState.restoreButtonVisible = true
                return true
            }
            else {
                systemState.restoreButtonVisible = false
                return false
            }
        } else {
            systemState.restoreButtonVisible = false
            return false
        }
    }

    Row {
        id: restoreAlarmButton

        height: parent.width
        anchors.centerIn: parent
        spacing: 12

        property var once: false
        property var popup: null

        Item {
            width: 20
            height: parent.height

            anchors.verticalCenter: parent.verticalCenter

            Image {
                id: volumeImg
                width: 20
                height: 20

                visible: false
                anchors.centerIn: parent
                source: "qrc:/resources/images/desktop/icons/restore-after-alarm.png"
            }

            ColorOverlay {
                anchors.fill: volumeImg
                source: volumeImg
                color: ui.colors.light1
            }
        }

        Text {
            text: tr.reset_after_alarm_for_action_bar
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
            Popups.reset_alarm_popup(hub, management)
        }
    }
}