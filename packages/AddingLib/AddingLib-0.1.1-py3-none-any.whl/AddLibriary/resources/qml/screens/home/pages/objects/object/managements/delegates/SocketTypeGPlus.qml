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
        opacity: enabled ? 1 : 0.3

        DS3.Switch {
            id: smallSwitch

            anchors {
                right: parent.right
                verticalCenter: parent.verticalCenter
            }

            checked: device.turned_on
            isDanger: (
                device.voltage_low ||
                device.voltage_high ||
                device.current_limit ||
                device.temperature_high ||
                device.relay_stuck
            )
            cancelBinding: false
            visible: {
                if (!device) return false
                if (!hub.current_user.relay_access) return false
                if (device.channel_mode == 2) return false
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

            source: !device.turned_on
                    ? "qrc:/resources/images/Athena/views_icons/Impulse-M.svg"
                    : "qrc:/resources/images/Athena/views_icons/Stop-M.svg"
            color: ui.ds3.figure[device.channel_status_color]
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
