import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3


CommonPart {
    id: delegate

    property alias separator: separator
    property alias onOffSwitchRectangle: onOffSwitchRectangle

//  Initial time
    property var startTimestamp: device.shut_off_time_channel1
//  Current time left
    property var timeLeft: Math.ceil(device.shut_off_time_channel1 - Date.now() / 1000)

    property var subtitleValue: {
        if (onOffSwitch.checked && device.shut_off_mode_enabled_ch1 && startTimestamp > 0) {
            var hours = Math.floor(timeLeft / 3600)
            var min = Math.floor(timeLeft / 60) % 60
            var sec = timeLeft % 60
            return hours.toString().padStart(2, "0") + ":" + min.toString().padStart(2, "0") + ":" + sec.toString().padStart(2, "0")
        } else {
            return device.shut_off_period_channel1_str
        }
    }

    height: 72 + separator.height + onOffSwitchRectangle.height

    flow.anchors {
        top: flow.parent.top
        topMargin: 48
        bottom: undefined
        bottomMargin: 0
    }

    Rectangle {
        id: separator

        width: parent.width - 32
        height: 1

        anchors.horizontalCenter: parent.horizontalCenter

        color: list.currentIndex == index ? ui.colors.dark1 : deviceDelegate.selectedColor

        anchors {
            top: parent.top
            topMargin: 72
        }
    }

    Item {
        id: onOffSwitchRectangle

        width: parent.width
        height: Math.max(buttonTitle.height, onOffSwitch.height) + 16

        anchors {
            top: parent.top
            topMargin: 73
        }

        DS3.MouseArea {
            onClicked: {
                list.currentIndex = index
            }
        }

        DS3.AtomTitle {
            id: buttonTitle

            anchors {
                left: parent.left
                leftMargin: 16
                right: onOffSwitch.left
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            title: device.button1_name
            subtitle: device.shut_off_mode_enabled_ch1 ? subtitleValue : ""
            subtitleIcon {
                source: "qrc:/resources/images/Athena/common_icons/Timer-S.svg"
                color: ui.ds3.figure.base
                visible: !!subtitle.length
            }
        }

        DS3.Switch {
            id: onOffSwitch

            anchors {
                right: parent.right
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            checked: device.channel1_on
            enabled: hub.current_user.relay_access && hub.online && device.online
            cancelBinding: false

            onCheckedChanged: {
                if (!device.shut_off_mode_enabled_ch1) return
                checked ? timer.start() : timer.stop()
            }

            onToggle: () => {
                if (!onOffSwitch.enabled || !hub.online) return
                if (checked) {
                    app.hub_management_module.device_command_for_ls(device, 7, ["CHANNEL_1"])
                } else {
                    app.hub_management_module.device_command_for_ls(device, 6, ["CHANNEL_1"])
                }
            }
        }
    }

    Timer {
        id: timer

        interval: 1000
        repeat: true
        triggeredOnStart: true

        onTriggered: {
            if (Date.now() / 1000 >= startTimestamp) {
                timeLeft = 0
                stop()
            }
            else {
                timeLeft = Math.ceil(startTimestamp - Date.now() / 1000)
            }
        }
    }
}