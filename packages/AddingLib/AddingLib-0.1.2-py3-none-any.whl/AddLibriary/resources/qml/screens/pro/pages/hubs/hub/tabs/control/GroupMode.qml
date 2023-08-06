import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/utils.js" as Utils

Item {
    id: groupsControlView

    anchors {
        top: parent.top
        left: parent.left
        right: parent.right
        bottom: parent.bottom
    }

    visible: hub && hub.groups_enabled

    Timer {
        id: buttonTimer

        interval: 500
        running: false
        repeat: false

        onTriggered: {
            securityButtonsItemWithGroups.buttonsWithGroups = null
        }
    }

    Custom.BlockLoading {
        opacity: 1
        radius: 32
        minTime: 500
        customOpacity: 0.1
        startSignals: [app.hub_management_module.startPerformSecurityAction]
        stopSignals: [app.hub_management_module.endPerformSecurityAction]
    }

    Item {
        id: groupsGridItem

        anchors.fill: parent

        Custom.FontText {
            id: groupsTitle

            anchors {
                horizontalCenter: parent.horizontalCenter
                bottom: nightModeWrapper.top
                bottomMargin: 24
            }

            text: tr.group_mode_title
            color: ui.colors.light3
            font.pixelSize: 16
        }

        Item {
            id: nightModeWrapper

            width: Math.max(637, [groupsControlView.width * 0.5])
            height: nightModeRect.height

            anchors {
                horizontalCenter: parent.horizontalCenter
                topMargin: parent.height / 2 - nightModeRect.height / 2 - 52
                top: parent.top
            }

            enabled: hub && hub.online
            opacity: hub && hub.online ? 1 : 0.4

            Rectangle {
                id: nightModeRect

                property var borderColor: hub && hub.groups_night_mode_enabled ? ui.colors.green1 : ui.colors.light3

                height: {
                    if (gridView.contentHeight >= 340) return 340
                    if (gridView.contentHeight > (application.height - 364)) return application.height - 364
                    return gridView.contentHeight + 32
                }
                width: parent.width

                color: "transparent"

                border {
                    width: 1

                    color: borderColor
                }

                Rectangle {
                    id: nightRectCanvas // to hide nightModeRect.border behind opaq nightRect Button

                    width: Math.max(195, [(groupsControlView.width - 22) * 0.5 / 3 - 10])
                    height: 40

                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -20
                        horizontalCenter: parent.horizontalCenter
                    }

                    radius: 8
                    color: ui.colors.dark3
                }

                Custom.ButtonIconed {
                    id: nightRect

                    height: 40
                    width: Math.max(195, [(groupsControlView.width - 22) * 0.5 / 3 - 10])

                    anchors {
                        bottom: parent.bottom
                        bottomMargin: -20
                        horizontalCenter: parent.horizontalCenter
                    }

                    radius: 8
                    color: (hub && hub.groups_night_mode_enabled) ? ui.colors.green1 : ui.colors.dark1

                    z: 99
                    opacity: enabled ? 1 : 0.3
                    textButton.color: transparent ? color : ui.colors.black
                    backgroundItem.color: transparent ? "transparent" : color
                    backgroundItem.opacity: 1
                    backgroundItem.border.color: color

                    onClicked: {
                        if (hub) {
                            nightRect.enabled = false
                            security_timer.start()
                            if (hub.groups_night_mode_enabled) {
                                app.hub_management_module.perform_security_action("PARTIAL_DISARM", false)
                            } else {
                                app.hub_management_module.perform_security_action("PARTIAL_ARM", false)
                            }
                        }
                    }

                    Timer {
                        id: security_timer

                        running: false
                        repeat: false
                        interval: 1000

                        onTriggered: nightRect.enabled = true
                    }

                    Item {
                        anchors.fill: parent

                        Image {
                            width: 24
                            height: 24

                            anchors {
                                left: parent.left
                                leftMargin: 6
                                verticalCenter: parent.verticalCenter
                            }

                            sourceSize.width: 24
                            sourceSize.height: 24

                            source: {
                                if (hub && hub.groups_night_mode_enabled) {
                                    return "qrc:/resources/images/icons/night-mode-dark.svg"
                                }
                                return "qrc:/resources/images/desktop/button_icons/night-mode-light.svg"
                            }
                        }

                        Custom.FontText {
                            width: parent.width - 12 - 24

                            anchors.centerIn: parent
                            anchors.horizontalCenterOffset: {
                                if (truncated) return 12
                                return 0
                            }

                            text: tr.part_arm
                            color: hub && hub.groups_night_mode_enabled ? ui.colors.black : ui.colors.light3
                            textFormat: Text.PlainText
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                }

                GridView {
                    id: gridView

                    anchors {
                        topMargin: 24
                        fill: parent
                        margins: 12
                        rightMargin: 6
                    }

                    cellWidth: (parent.width - 24) / 3
                    cellHeight: 64
                    clip: true
                    opacity: enabled ? 1 : 0.5
                    model: management ? management.filtered_groups : []

                    ScrollBar.vertical: ScrollBar {
                        anchors.right: parent.right
                        anchors.rightMargin: 0

                        policy: {
                            if (management.filtered_groups.length > 15) return ScrollBar.AlwaysOn
                            return ScrollBar.AlwaysOff
                        }
                    }

                    delegate: Item {
                        id: groupDelegate

                        property var armed: group && group.state == "ARMED"
                        property var tsaEnabled: hub ? hub.firmware_version_dec >= 209100 && hub.groups_enabled : false
                        property var imageUrl: ""
                        property var buttonColor: ui.colors.white

                        property var nothing: {
                            if (!hub || !group) return Utils.get_data_hub_state("DISARMED")

                            var stateGroup = group.state

                            if ((hub.firmware_version_dec >= 209100) && group.two_stage_arming_status > 1) {
                                stateGroup = group.tsa_status
                            }
                            [groupDelegate.imageUrl, , groupDelegate.buttonColor] = Utils.get_data_hub_state(stateGroup)
                        }

                        width: (nightModeRect.width - 24) / 3
                        height: 42

                        Custom.ButtonIconed {
                            id: groupButton

                            width: parent.width - 8
                            height: 40

                            anchors {
                                verticalCenter: parent.verticalCenter
                            }

                            color: groupDelegate.buttonColor
                            transparent: true

                            onClicked: {
                                app.hub_management_module.perform_group_security_action(group, false)
                            }

                            Item {
                                anchors.fill: parent

                                Image {
                                    width: 24
                                    height: 24

                                    anchors {
                                        left: parent.left
                                        leftMargin: 6
                                        verticalCenter: parent.verticalCenter
                                    }

                                    sourceSize.width: 24
                                    sourceSize.height: 24
                                    source: groupDelegate.imageUrl
                                }

                                Custom.FontText {
                                    width: parent.width - 12 - 24

                                    anchors.centerIn: parent
                                    anchors.horizontalCenterOffset: truncated ? 12 : 0

                                    text: group && group.name ? group.name : ""
                                    color: armed ? ui.colors.green1 : ui.colors.light3
                                    textFormat: Text.PlainText
                                    elide: Text.ElideRight
                                    horizontalAlignment: Text.AlignHCenter
                                }
                            }
                        }
                    }
                }
            }
        }

        Row {
            id: securityButtonsItemWithGroups

            property var buttonsWithGroups: null
            property var buttonWidth: Math.max(205, [(groupsControlView.width - 22) * 0.5 / 3])

            height: 40

            anchors {
                top: nightModeWrapper.bottom
                topMargin: 52
                horizontalCenter: parent.horizontalCenter
            }

            spacing: 11

            Custom.ButtonIconed {
                id: armButtonWithGroups

                width: securityButtonsItemWithGroups.buttonWidth

                visible: gridView.model.length > 1
                enabled: hub && hub.online
                opacity: hub && hub.online ? 1 : 0.4
                color: ui.colors.green1

                iconImage.source: "qrc:/resources/images/icons/personal_account/ArmedOnGreen.svg"

                textButton.text: tr.arm
                textButton.color: ui.colors.black

                onClicked: {
                    securityButtonsItemWithGroups.buttonsWithGroups = armButtonWithGroups
                    buttonTimer.start()
                    app.hub_management_module.perform_security_action("ARM", false)
                }
            }

            Custom.ButtonIconed {
                id: disarmButtonWithGroups

                width: securityButtonsItemWithGroups.buttonWidth

                visible: gridView.model.length > 1
                enabled: hub && hub.online
                opacity: hub && hub.online ? 1 : 0.4

                iconImage.source: "qrc:/resources/images/icons/personal_account/Disarmed.svg"

                textButton.text: tr.disarm
                textButton.color: ui.colors.middle1

                backgroundItem.color: 'transparent'
                backgroundItem.border.color: ui.colors.middle1

                onClicked: {
                    securityButtonsItemWithGroups.buttonsWithGroups = disarmButtonWithGroups
                    buttonTimer.start()
                    app.hub_management_module.perform_security_action("DISARM", false)
                }
            }

            Custom.ButtonIconed {
                id: alarmButtonWithGroups

                width: securityButtonsItemWithGroups.buttonWidth

                iconImage.source: "qrc:/resources/images/icons/personal_account/Panic.svg"

                textButton.text: tr.panic
                textButton.color: ui.colors.red1

                backgroundItem.color: 'transparent'
                backgroundItem.border.color: ui.colors.red1

                onClicked: {
                    if (hub && !hub.current_user.alarm_button_access) {
                        Popups.text_popup(tr.error, tr.Com_no_access0)
                        return
                    }
                    Popups.hub_alarm_countdown_popup("PANIC", false)
                }
            }
        }
    }
}
