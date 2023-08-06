import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/js/utils.js" as Utils
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3

CommonPart {
    property bool interconnectButtonVisible: !rexDeleg && device.is_interconnect_available && device.buzzer_state == 1
    property bool interconnectDelayButtonVisible: device.is_interconnect_delay_available
    property bool criticalButtonVisible

    height: 72 + (spreadInfoFP2.visible ? 38 : 0)

    Connections {
        target: hub

        onDataChanged: {
            if (!util.compare_jsons(device.status_icons_list, flowIconsModel)) {
                device.dataChanged()
            }
        }
    }

    Item {
        id: spreadInfoFP2 // new fp2

        width: parent.width - 32
        height: 38

        anchors {
            horizontalCenter: parent.horizontalCenter
            bottom: parent.bottom
        }

        visible: interconnectButtonVisible || interconnectDelayButtonVisible || criticalButtonVisible

        Rectangle {
            width: parent.width
            height: 1

            color: ui.ds3.bg.low
        }

        DS3.Text {
            anchors {
                verticalCenter: parent.verticalCenter
                left: parent.left
                right: interconnectButton.left
                rightMargin: 16
            }

            text: criticalButtonVisible ? tr.critical_co_level : tr.mute_detector_info
            style: ui.ds3.text.body.LRegular
        }

        DS3.ButtonMini {
            id: interconnectButton

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
            }

            // wtf, no interconnect access info (company installer case)
            enabled: !!hub && !!device && device.online && hub.online && !(appUser.company_id && !hub.current_user.device_edit_access)
            visible: interconnectButtonVisible && !interconnectDelayButton.visible && !criticalButtonVisible
            color: ui.ds3.figure.attention
            source: "qrc:/resources/images/Athena/views_icons/VolumeOff-M.svg"

            onClicked: {
                app.hub_management_module.device_command(device, 5)
            }
        }

        DS3.ButtonMini {
            id: interconnectDelayButton

            anchors {
                verticalCenter: parent.verticalCenter
                right: parent.right
            }

            visible: interconnectDelayButtonVisible && !criticalButtonVisible

            opacity: enabled ? 1.0 : 0.3
            // wtf, no interconnect access info (company installer case)
            enabled: !!hub && hub.online && !!device && device.online && !device.is_bypassed && !(!!appUser && appUser.company_id && !hub.current_user.device_edit_access)
            color: ui.ds3.figure.warningContrast
            source: "qrc:/resources/images/Athena/views_icons/Warning-M.svg"

            onClicked: {
                if (hub.interconnect_delay_expiration_diff > 0) {
                    let fire_alarms = management.devices.fire_alarms
                    Popups.interconnect_delay_popup(fire_alarms["fires"], fire_alarms["trigger"], management)
                }
            }
        }
    }
}