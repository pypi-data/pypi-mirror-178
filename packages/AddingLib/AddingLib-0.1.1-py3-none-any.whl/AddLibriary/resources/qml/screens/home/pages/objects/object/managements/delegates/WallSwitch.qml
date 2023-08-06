import QtQuick 2.7
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3" as DS3

CommonPart {

    property alias smallSwitch: smallSwitch

    Item {
        id: onOffDevice

        width: 40
        height: 22

        anchors {
            top: parent.top
            topMargin: 24
            right: parent.right
            rightMargin: deviceDelegate.settingsVisible ? 60 : 16
        }

        enabled: !!hub && !!device && hub.online && device.online && !device.is_bypassed

        DS3.Switch {
            id: smallSwitch

            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }

            checked: device.turned_on
            isDanger: {
                var real_state = device.real_state_alt
                return (
                    (real_state & 32) == 32 ||
                    (real_state & 16) == 16 ||
                    (real_state & 8) == 8 ||
                    (real_state & 4) == 4 ||
                    (real_state & 2) == 2 ||
                    (real_state & 1) == 1
                )
            }
            cancelBinding: false
            visible: {
                if (parent.rexDeleg) return false
                if (!hub.current_user.relay_access) return false
                if (!!device && device.lockup_relay_mode == 2) return false
                return true
            }

            onToggle: () => {
                if (!smallSwitch.enabled || !hub.online) return
                if (checked) {
                    app.hub_management_module.device_command(device, 7)
                } else {
                    app.hub_management_module.device_command(device, 6)
                }
            }
        }

        DS3.ButtonMini {
            id: impulseButton

            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }

            source: !device.turned_on ?
                "qrc:/resources/images/Athena/views_icons/Impulse-M.svg" :
                "qrc:/resources/images/Athena/views_icons/Stop-M.svg"
            opacity: enabled ? 1 : 0.3
            color: {
                let intersection_states = [
                    "OFF_HIGH_TEMPERATURE",
                    "CONTACT_HANG",
                    "OFF_TOO_LOW_VOLTAGE",
                    "OFF_HIGH_VOLTAGE",
                    "OFF_SHORT_CIRCUIT",
                    "OFF_HIGH_CURRENT"
                ].filter(x => device.real_state.includes(x))
                return intersection_states.length ? ui.ds3.figure.attention : ui.ds3.figure.interactive
           }
            visible: {
                if (parent.rexDeleg) return false
                if (smallSwitch.visible) return false
                if (hub.current_user.relay_access) return true
                return false
            }

            DS3.MouseArea {
                id: impulseArea

                onClicked: {
                    if (!device.turned_on) app.hub_management_module.device_command(device, 6)
                    else app.hub_management_module.device_command(device, 7)
                }
            }

            states: State {
                name: "pressed"; when: impulseArea.pressed
                PropertyChanges { target: impulseButton; scale: 0.9 }
            }

            transitions: Transition {
                NumberAnimation { properties: "scale"; duration: 200; easing.type: Easing.InOutQuad }
            }
        }
    }
}