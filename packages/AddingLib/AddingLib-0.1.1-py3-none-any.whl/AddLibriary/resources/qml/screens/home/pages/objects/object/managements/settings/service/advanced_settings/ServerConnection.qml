import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    Connections {
        target: app

        onActionSuccess: {
            advancedSettingsLoader.setSource("")
        }
    }

    color: ui.ds3.bg.base

    DS3.ChangesChecker {
        id: changesChecker

        listeningValues: [
            hubOfflineAlarm.value,
            pingPeriodSlider.value,
            connectionLostAsMalfunctionSwitch.checked,
            ethernetChannel.checked,
            gsmChannel.checked,
            wifiChannel.checked,
            notificationDelaySlider.value
        ]
    }

    DS3.NavBarModal {
        id: serverConnectionBar

        headerText: tr.server_connection
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            advancedSettingsLoader.setSource("")
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: serverConnectionBar.bottom
            bottom: saveButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: hubOfflineAlarm

                enabled: devEnable
                value: hub.hub_offline_alarm
                title: tr.rise_alarm_delay_when_hub_goes_offline
                from: 30
                to: 600
                stepSize: 10
                visible: hub.hub_type != "YAVIR"
                suffix: tr.sec
            }
        }

        DS3.Spacing {
            height: hubOfflineAlarm.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.rise_alarm_delay_when_hub_goes_offline_hint
            color: ui.ds3.figure.secondary
            visible: hubOfflineAlarm.visible
        }

        DS3.Spacing {
            height: hubOfflineAlarm.visible ? 24 : 0
        }

        Column {
            width: parent.width

            visible: !hub.hub_type.startsWith("YAVIR")

            DS3.SettingsContainer {
                width: parent.width

                anchors.horizontalCenter: parent.horizontalCenter

                DS3.SettingsSliderValue {
                    id: pingPeriodSlider

                    enabled: devEnable
                    value: hub.hub_ping_period
                    title: tr.hub_server_ping_interval
                    from: 10
                    to: 300
                    stepSize: 10
                    suffix: tr.sec
                }
            }

            DS3.Spacing {
                height: 4
            }

            DS3.Text {
                width: parent.width

                style: ui.ds3.text.body.MRegular
                text: tr.hub_server_ping_interval_hint
                color: ui.ds3.figure.secondary
            }

            DS3.Spacing {
                height: 24
            }
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: connectionLostAsMalfunctionSwitch

                enabled: devEnable
                title: tr.connection_lost_as_mulfunction
                checked: hub.connection_lost_as_malfunction
            }
        }

        DS3.Spacing {
            height: connectionLostAsMalfunctionSwitch.visible ? 4 : 0
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.connection_lost_as_mulfunction_desc
            visible: connectionLostAsMalfunctionSwitch.visible
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: connectionLostAsMalfunctionSwitch.visible ? 24 : 0
        }

        DS3.Text {
            width: parent.width

            text: tr.channel_lost_notifications_title
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSwitch {
                id: ethernetChannel

                enabled: devEnable
                title: "Ethernet"
                checked: hub.channel_connectivity_notification_active.includes("ETHERNET")
            }

            DS3.SettingsSwitch {
                id: gsmChannel

                enabled: devEnable
                title: tr.cellular
                checked: hub.channel_connectivity_notification_active.includes("GSM")
            }

            DS3.SettingsSwitch {
                id: wifiChannel

                enabled: devEnable
                title: "Wi-Fi"
                checked: hub.channel_connectivity_notification_active.includes("WIFI")
                visible: hub.hub_type.endsWith("PLUS") && !hub.hub_type.startsWith("YAVIR")
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            text: tr.channel_lost_notifications_desc
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.SettingsSliderValue {
                id: notificationDelaySlider

                enabled: devEnable
                value: hub.channel_offline_alarm_delay_seconds / 60
                title: tr.channel_lost_delay
                from: 3
                to: 30
                stepSize: 1
                suffix: tr.min
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            style: ui.ds3.text.body.MRegular
            text: tr.channel_lost_delay_desc
            color: ui.ds3.figure.secondary
        }
    }

    DS3.ButtonBar {
        id: saveButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.save
        hasBackground: true
        enabled: devEnable && changesChecker.hasChanges

        button.onClicked: {
            var settings = {
                "ping_period_seconds": pingPeriodSlider.value,
                "connection_lost_as_malfunction": connectionLostAsMalfunctionSwitch.checked,
                "channel_offline_alarm_delay_seconds": notificationDelaySlider.value * 60,
                "channel_connectivity_notification_active": [],
            }

            if (hubOfflineAlarm.visible) {
                settings["offline_alarm_seconds"] = hubOfflineAlarm.value
            }

            if (ethernetChannel.checked) {
                settings["channel_connectivity_notification_active"].push("ETHERNET")
            }
            if (gsmChannel.checked) {
                settings["channel_connectivity_notification_active"].push("GSM")
            }
            if (wifiChannel.checked) {
                settings["channel_connectivity_notification_active"].push("WIFI")
            }

            DesktopPopups.please_wait_popup()
            app.hub_management_module.apply_update(management, hub, settings)
        }
    }
}
