import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3/" as DS3

LightSwitch {
//  Initial time for second button
    property var startTimestampSecond: device.shut_off_time_channel2
//  Current time left for second button
    property var timeLeftSecond: Math.ceil(device.shut_off_time_channel2 - Date.now() / 1000)

    property var subtitleValueSecond: {
        if (onOffSwitchSecond.checked && device.shut_off_mode_enabled_ch2 && startTimestampSecond > 0) {
            var hours = Math.floor(timeLeftSecond / 3600)
            var min = Math.floor(timeLeftSecond / 60) % 60
            var sec = timeLeftSecond % 60
            return hours.toString().padStart(2, "0") + ":" + min.toString().padStart(2, "0") + ":" + sec.toString().padStart(2, "0")
        } else {
            return device.shut_off_period_channel2_str
        }
    }

    height: 72 + separator.height + onOffSwitchRectangle.height + separatorSecond.height + onOffSwitchRectangleSecond.height

    Rectangle {
        id: separatorSecond

        width: parent.width - 32
        height: 1

        anchors {
            top: parent.top
            topMargin: 72 + separator.height + onOffSwitchRectangle.height
            horizontalCenter: parent.horizontalCenter
        }

        color: list.currentIndex == index ? ui.colors.dark1 : deviceDelegate.selectedColor
    }

    Item {
        id: onOffSwitchRectangleSecond

        width: parent.width
        height: Math.max(buttonTitleSecond.height, onOffSwitchSecond.height) + 16

        anchors {
            top: parent.top
            topMargin: 72 + separator.height + onOffSwitchRectangle.height + separatorSecond.height
        }

        DS3.MouseArea {
            onClicked: {
                list.currentIndex = index
            }
        }

        DS3.AtomTitle {
            id: buttonTitleSecond

            anchors {
                left: parent.left
                leftMargin: 16
                right: onOffSwitchSecond.left
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            title: device.button2_name
            subtitle: device.shut_off_mode_enabled_ch2 ? subtitleValueSecond : ""
            subtitleIcon {
                source: "qrc:/resources/images/Athena/common_icons/Timer-S.svg"
                color: ui.ds3.figure.base
                visible: !!subtitle.length
            }
        }

        DS3.Switch {
            id: onOffSwitchSecond

            anchors {
                right: parent.right
                rightMargin: 16
                verticalCenter: parent.verticalCenter
            }

            checked: device.channel2_on
            enabled: hub.current_user.relay_access && hub.online && device.online
            cancelBinding: false

            onCheckedChanged: {
                if (!device.shut_off_mode_enabled_ch2) return
                checked ? timerSecond.start() : timerSecond.stop()
            }

            onToggle: () => {
                if (!onOffSwitchSecond.enabled || !hub.online) return
                if (checked) {
                    app.hub_management_module.device_command_for_ls(device, 7, ["CHANNEL_2"])
                } else {
                    app.hub_management_module.device_command_for_ls(device, 6, ["CHANNEL_2"])
                }
            }
        }
    }

    Timer {
        id: timerSecond

        interval: 1000
        repeat: true
        triggeredOnStart: true

        onTriggered: {
            if (Date.now() / 1000 >= startTimestampSecond) {
                timeLeftSecond = 0
                stop()
            }
            else {
                timeLeftSecond = Math.ceil(startTimestampSecond - Date.now() / 1000)
            }
        }
    }
}