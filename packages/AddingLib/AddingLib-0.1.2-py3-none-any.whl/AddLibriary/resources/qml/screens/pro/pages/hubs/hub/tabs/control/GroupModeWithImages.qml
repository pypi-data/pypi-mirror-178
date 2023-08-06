import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13


import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/utils.js" as Utils



Item {
    id: groupsControlView
    visible: hub && hub.groups_enabled

    anchors {
        top: parent.top
        left: parent.left
        right: parent.right
        bottom: parent.bottom
    }

    Timer {
        id: buttonTimer

        interval: 500
        running: false
        repeat: false
        onTriggered: {
            securityButtonsItem.button = null
            securityButtonsItemWithGroups.buttonsWithGroups = null
        }
    }

    Item {
        id: groupsGridItem

        anchors.fill: parent

        Item {
           id: nightModeWrapper

           width: groupsControlView.width * 0.797
           height: nightModeRect.height

            enabled: hub && hub.online
            opacity: hub && hub.online ? 1 : 0.4

            anchors {
                horizontalCenter: parent.horizontalCenter
                topMargin:  parent.height / 2 - nightModeRect.height / 2 - 52
                top: parent.top
            }

            Rectangle {
                id: nightModeRect

                height: {
                    var rows = 2
                    if (application.height > 720) {rows = 3}
                    if (application.height > 880) {rows = 4}
                    var nRowsHeight = 160 * rows + 2
                    return 160 * rows + 2

                }
                width: parent.width

                color: "transparent"
                border {
                    color: hub && hub.groups_night_mode_enabled ? ui.colors.green1 : ui.colors.light3
                    width: 1
                }
                radius: 10

                /* -------------------------------------------------------- */
                /* desktop tests */
                Accessible.name: "control_with-groups_night_border"
                Accessible.description: "color:" + border.color
                Accessible.role: Accessible.Graphic
                /* -------------------------------------------------------- */

                Rectangle {
                    id: nightRectCanvas  // to hide nightModeRect.border behind opaq nightRect Button

                    width: Math.max(195, [(groupsControlView.width - 22) * 0.5/3 - 10])
                    height: 40

                    radius: 8
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: -20
                    anchors.horizontalCenter: parent.horizontalCenter

                    color: ui.colors.dark3
                }

                Custom.ButtonIconed {
                    id: nightRect

                    height: 40
                    width: Math.max(195, [(groupsControlView.width - 22)* 0.5/3 - 10])

                    radius: 8
                    color: (hub && hub.groups_night_mode_enabled) ? ui.colors.green1 : ui.colors.dark1
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: -20
                    anchors.horizontalCenter: parent.horizontalCenter
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
                            id: nightModeIcon

                            width: 24
                            height: 24

                            sourceSize.width: 24
                            sourceSize.height: 24
                            source: {
                                if (hub && hub.groups_night_mode_enabled) {
                                    return "qrc:/resources/images/icons/night-mode-dark.svg"
                                }
                                return "qrc:/resources/images/desktop/button_icons/night-mode-light.svg"
                            }
                            anchors {
                                left: parent.left
                                leftMargin: 6
                                verticalCenter: parent.verticalCenter
                            }

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: "control_with-groups_night_icon"
                            Accessible.description: source
                            Accessible.role: Accessible.Graphic
                            /* -------------------------------------------- */
                        }

                        Custom.FontText {
                            text: tr.part_arm
                            color: hub && hub.groups_night_mode_enabled ? ui.colors.black : ui.colors.light3
                            width: parent.width - 12 - 24
                            anchors.centerIn: parent
                            anchors.horizontalCenterOffset: {
                                if (truncated) return 12
                                return 0
                            }
                            textFormat: Text.PlainText
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignHCenter

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: "control_with-groups_night_text"
                            Accessible.description: text
                            Accessible.role: Accessible.Paragraph
                            /* -------------------------------------------- */
                        }
                    }

                    /* ---------------------------------------------------- */
                    /* desktop tests */
                    accessibleAreaName: "control_with-groups_night_area"
                    accessibleAreaDescription: "color-button:" + backgroundItem.color + " color-border:" + backgroundItem.border.color
                    /* ---------------------------------------------------- */
                }

                GridView {
                    id: gridView

                    cellWidth: 160
                    cellHeight: 160
                    clip: true

                    opacity: enabled ? 1 : 0.5

                    anchors.fill: parent
                    anchors.margins: 1

                    model: management ? management.filtered_groups : []

                    ScrollBar.vertical: ScrollBar {
                        policy: {
                            if (management.filtered_groups.length > 10) return ScrollBar.AlwaysOn
                            return ScrollBar.AlwaysOff
                        }
                        anchors.right: parent.right
                        anchors.rightMargin: 0
                    }

                    delegate: Item {
                        id: groupDelegate

                        width: gridView.cellWidth
                        height: gridView.cellHeight

                        z: 98

                        property var armed: !!group && group.state == "ARMED"

                        property var nothing: {
                            if (!hub || !group) return Utils.get_data_hub_state("DISARMED")

                            var stateGroup = group.state

                            if ((hub.firmware_version_dec >= 209100) && group.two_stage_arming_status > 1) {
                                stateGroup = group.tsa_status
                            }
                            [roundGroupStatusIcon.source, , ] = Utils.get_data_hub_state(stateGroup)
                        }

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        property var accessibleBasis: __accessible_unique_ids__ ? "control_with-groups_group_" + group.group_id : "group"

                        Accessible.name: "control_with-groups_group_" + group.group_id + "_area"
                        Accessible.description: groupDelegate.armed ? "<button enabled=" + Accessible.checkable + ">" + "state:armed" + "</button>" : "<button enabled=" + Accessible.checkable + ">" + "state:disarmed" + "</button>"
                        Accessible.role: Accessible.Button
                        Accessible.checkable: visible && enabled
                        Accessible.onPressAction: {
                            if (!Accessible.checkable) return
                            mouseArea.clicked(true)
                        }
                        /* ------------------------------------------------ */

                        Rectangle {
                            id: groupCanvasOnHover

                            anchors.fill: parent
                            radius: 8

                            color: mouseArea.containsMouse ? ui.colors.dark2 : "transparent"

                            MouseArea {
                                id: mouseArea

                                hoverEnabled: true
                                anchors.fill: parent
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    app.hub_management_module.perform_group_security_action(group, false)
                                }
                            }

                        }

                        Custom.RoundImage {
                            id: imageItem

                            imageWidthHeight: 80
                            imageSource: !!group ? group.big_image_link : ""
                            anchors.centerIn: parent

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: groupDelegate.accessibleBasis + "_image"
                            Accessible.description: imageItem.objImage.source
                            Accessible.role: Accessible.Graphic
                            /* -------------------------------------------- */
                        }

                        ColorOverlay {
                            anchors.fill: imageItem
                            source: imageItem
                            opacity: 0.6
                            color: {
                                if (!group) return ""
                                return group.group_state == "ARMED" ? ui.colors.green1 : "transparent"
                            }
                        }
                        Rectangle {
                            id: roundGroupStatusIconBackground

                            height: 32
                            width: 32

                            radius: 16

                            color: ui.colors.dark3

                            anchors {
                                left: imageItem.left
                                bottom: imageItem.bottom
                            }
                        }
                        Image {
                            id: roundGroupStatusIcon

                            sourceSize.width: 24
                            sourceSize.height: 24
                            height: 24
                            width: 24

                            source: 'xxxxxxxxxxx'

                            anchors {
                                left: roundGroupStatusIconBackground.left
                                leftMargin: 4
                                bottom: roundGroupStatusIconBackground.bottom
                                bottomMargin: 4
                            }

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: groupDelegate.accessibleBasis + "_icon"
                            Accessible.description: source
                            Accessible.role: Accessible.Graphic
                            /* -------------------------------------------- */
                        }

                        Custom.FontText {
                            text: !!group ? group.name : ""

                            color: armed ? ui.colors.green1 : ui.colors.light3

                            width: parent.width - 12 - 24
                            anchors {
                                top: imageItem.bottom
                                topMargin: 6
                                horizontalCenter: imageItem.horizontalCenter
                            }
                            textFormat: Text.PlainText
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignHCenter

                            /* -------------------------------------------- */
                            /* desktop tests */
                            Accessible.name: groupDelegate.accessibleBasis + "_name"
                            Accessible.description: text
                            Accessible.role: Accessible.Paragraph
                            /* -------------------------------------------- */
                        }
                    }
                }
            }
        }
        Row {
            id: securityButtonsItemWithGroups

            property var buttonsWithGroups: null
            property var buttonWidth: Math.max(205, [(groupsControlView.width - 22)* 0.5/3])

            height: 40
            spacing: 11

            anchors {
                top: nightModeWrapper.bottom
                topMargin: 52
                horizontalCenter: parent.horizontalCenter
            }

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

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "control_with-groups_arm_icon"
                accessibleIconDescription: iconImage.source

                accessibleTextName: "control_with-groups_arm_text"
                accessibleTextDescription: textButton.text

                accessibleAreaName: "control_with-groups_arm_area"
                accessibleAreaDescription: "color-button:" + backgroundItem.color + " color-border:" + backgroundItem.border.color
                /* -------------------------------------------------------- */
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

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "control_with-groups_disarm_icon"
                accessibleIconDescription: iconImage.source

                accessibleTextName: "control_with-groups_disarm_text"
                accessibleTextDescription: textButton.text

                accessibleAreaName: "control_with-groups_disarm_area"
                accessibleAreaDescription: "color-button:" + backgroundItem.color + " color-border:" + backgroundItem.border.color
                /* -------------------------------------------------------- */
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

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "control_with-groups_alarm_icon"
                accessibleIconDescription: iconImage.source

                accessibleTextName: "control_with-groups_alarm_text"
                accessibleTextDescription: textButton.text

                accessibleAreaName: "control_with-groups_alarm_area"
                accessibleAreaDescription: "color-button:" + backgroundItem.color + " color-border:" + backgroundItem.border.color
                /* -------------------------------------------------------- */
            }
        }
    }
}