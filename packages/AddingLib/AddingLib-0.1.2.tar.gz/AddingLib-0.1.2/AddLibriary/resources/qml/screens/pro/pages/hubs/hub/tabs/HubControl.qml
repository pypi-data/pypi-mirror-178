import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13


import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/utils.js" as Utils
import "qrc:/resources/qml/screens/pro/pages/hubs/hub/tabs/control/" as Parts

Item {
    id: controlView

    Rectangle {
        anchors.fill: parent
        color: ui.colors.dark3
    }

    Anime.ClickAnimation { id: clickAnimation }

    signal reBillingInfo(variant info)

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
        id: billing

        width: parent.width
        height: visible ? 24 : 0
        visible: info
        anchors.top: parent.top

        property var info: null
        property var twoStageArming: hub && hub.firmware_version_dec >= 209100 && hub.two_stage_arming_state

        Text {
            color: {
                if (billing.info) return billing.info.attention ? "#f64347" : "#60e3ab"
                return "#60e3ab"
            }
            font.family: "Open Sans"
            font.pixelSize: 18
            font.letterSpacing: 0.6
            anchors.centerIn: parent
            text: {
                if (billing.info) return billing.info.balance + " " + billing.info.currency
                return ""
            }
        }

        MouseArea {
            anchors.fill: parent
            pressAndHoldInterval: 3000
            onPressAndHold: {
                Popups.text_popup("BILLING INFO", billing.info.text)
            }
        }
    }

    Column {
        id: noGroupsControlView

        width: 345

        visible: hub && !hub.groups_enabled
        spacing: 32

        anchors.centerIn: parent

        Row {
            id: stateItem

            spacing: 11
            anchors.horizontalCenter: parent.horizontalCenter


            Image {
                id: hubStateIcon

                width: 24
                height: 24
                sourceSize.width: 24
                sourceSize.height: 24

                anchors.verticalCenter: parent.verticalCenter

                source: {
                    if (billing.twoStageArming){
                        if (hub.two_stage_arming_progress_status == 2) {
                            return "qrc:/resources/images/icons/tsa-red.svg"
                        } else if (hub.two_stage_arming_progress_status == 3) {
                            return "qrc:resources/images/icons/tsa-green.svg"
                        } else if (hub.two_stage_arming_progress_status == 4) {
                            return "qrc:resources/images/icons/tsa-yellow.svg"
                        } else if (hub.two_stage_arming_progress_status == 5) {
                            return "qrc:resources/images/icons/tsa-green.svg"
                        }
                    }
                    if (hub) {
                        if (hub.state == "ARMED") {
                            return "qrc:resources/images/desktop/icons/ic-state-arm@2x.png"
                        } else if (hub.state == "DISARMED") {
                            return "qrc:resources/images/desktop/icons/ic-state-disarm@2x.png"
                        } else if (hub.state == "NIGHT_MODE") {
                            return "qrc:resources/images/desktop/icons/ic-state-perimeter@2x.png"
                        } else {
                            return "qrc:resources/images/desktop/icons/ic-state-disarm@2x.png"
                        }
                    } else {
                        return ""
                    }
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "control_without-groups_state_icon"
                Accessible.description: source
                Accessible.role: Accessible.Graphic
                /* ------------------------------------------------ */
            }

            Text {
                id: hubStateText

                height: contentHeight

                function render_text() {
                    wrapMode = Text.NoWrap
                    width = contentWidth
                    if (contentWidth > 288) {
                        width = 288
                        wrapMode = Text.Wrap
                    } else {
                        width = contentWidth
                        wrapMode = Text.NoWrap
                    }
                }

                onTextChanged: {
                    render_text()
                }

                Component.onCompleted: {
                    render_text()
                }

                text: {
                    if (billing.twoStageArming){
                        if (hub.two_stage_arming_progress_status == 2) {
                            return tr.arming_in_progress_please_wait
                        } else if (hub.two_stage_arming_progress_status == 3) {
                            return tr.finish_arm_by_clicking_on_device_or_activating_final_door_devices
                        } else if (hub.two_stage_arming_progress_status == 4) {
                            return tr.arming_incomplete_instructions
                        } else if (hub.two_stage_arming_progress_status == 5) {
                            return tr.finish_arm_by_clicking_on_device_or_activating_final_door_devices
                        }
                    }

                    if (hub && hub.state == "ARMED") {
                        return tr.armed
                    } else if (hub && hub.state == "DISARMED") {
                        return tr.disarmed
                    } else if (hub && hub.state == "NIGHT_MODE") {
                        return tr.partially_armed
                    } else return tr.disarmed
                }

                color: {

                    if (billing.twoStageArming) {
                        if (hub && hub.two_stage_arming_progress_status == 2) {
                            return ui.colors.red2
                        } else if (hub && hub.two_stage_arming_progress_status == 3) {
                            return ui.colors.lime2
                        } else if (hub && hub.two_stage_arming_progress_status == 4) {
                            return ui.colors.yellow1
                        } else if (hub && hub.two_stage_arming_progress_status == 5) {
                            return ui.colors.lime2
                        }
                    }
                    if (hub && hub.state == "ARMED") {
                        return ui.colors.green1
                    } else if (hub && hub.state == "DISARMED") {
                        return ui.colors.middle1
                    } else if (hub && hub.state == "NIGHT_MODE") {
                        return ui.colors.green1
                    }
                    return "#fdfdfd"
                }

                font.family: roboto.name
                font.pixelSize: 14

                anchors.verticalCenter: hubStateIcon.verticalCenter

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "control_without-groups_state_text"
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ------------------------------------------------ */
            }
        }


        Column {
            id: securityButtonsItem

            width: parent.width

            spacing: 16

            property var button: null
            property var buttonWidth: Math.max(220, [controlView.width / 4.8541])

            Custom.ButtonIconed {
                id: armButton

                width: securityButtonsItem.buttonWidth

                enabled: hub && hub.online
                opacity: hub && hub.online ? 1 : 0.4
                color: ui.colors.green1

                iconImage.source: "qrc:/resources/images/icons/personal_account/ArmedOnGreen.svg"

                textButton.text: tr.arm
                textButton.color: ui.colors.black

                anchors.horizontalCenter: parent.horizontalCenter

                onClicked: {
                    securityButtonsItem.button = armButton
                    buttonTimer.start()
                    app.hub_management_module.perform_security_action("ARM", false)
                }

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "control_without-groups_arm_icon"
                accessibleIconDescription: iconImage.source

                accessibleTextName: "control_without-groups_arm_text"
                accessibleTextDescription: textButton.text

                accessibleAreaName: "control_without-groups_arm_area"
                accessibleAreaDescription: "color-button:" + backgroundItem.color + " color-border:" + backgroundItem.border.color
                /* -------------------------------------------------------- */
            }

            Custom.ButtonIconed {
                id: disarmButton

                width: securityButtonsItem.buttonWidth

                enabled: hub && hub.online
                opacity: hub && hub.online ? 1 : 0.4

                iconImage.source: "qrc:/resources/images/icons/personal_account/Disarmed.svg"

                textButton.text: tr.disarm
                textButton.color: ui.colors.middle1

                backgroundItem.color: 'transparent'
                backgroundItem.border.color: ui.colors.middle1

                anchors.horizontalCenter: parent.horizontalCenter

                onClicked: {
                    securityButtonsItem.button = disarmButton
                    buttonTimer.start()
                    app.hub_management_module.perform_security_action("DISARM", false)
                }

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "control_without-groups_disarm_icon"
                accessibleIconDescription: iconImage.source

                accessibleTextName: "control_without-groups_disarm_text"
                accessibleTextDescription: textButton.text

                accessibleAreaName: "control_without-groups_disarm_area"
                accessibleAreaDescription: "color-button:" + backgroundItem.color + " color-border:" + backgroundItem.border.color
                /* -------------------------------------------------------- */
            }

            Custom.ButtonIconed {
                id: nightModeButton

                width: securityButtonsItem.buttonWidth

                enabled: hub && hub.online
                opacity: hub && hub.online ? 1 : 0.4

                iconImage.source: "qrc:/resources/images/icons/personal_account/NightMode.svg"

                textButton.text: tr.part_arm
                textButton.color: ui.colors.green1

                backgroundItem.color: 'transparent'
                backgroundItem.border.color: ui.colors.green1

                anchors.horizontalCenter: parent.horizontalCenter

                onClicked: {
                    securityButtonsItem.button = nightModeButton
                    buttonTimer.start()
                    app.hub_management_module.perform_security_action("PARTIAL_ARM", false)
                }

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "control_without-groups_night_icon"
                accessibleIconDescription: iconImage.source

                accessibleTextName: "control_without-groups_night_text"
                accessibleTextDescription: textButton.text

                accessibleAreaName: "control_without-groups_night_area"
                accessibleAreaDescription: "color-button:" + backgroundItem.color + " color-border:" + backgroundItem.border.color
                /* -------------------------------------------------------- */
            }

            Custom.ButtonIconed {
                id: alarmButton

                width: securityButtonsItem.buttonWidth

                iconImage.source: "qrc:/resources/images/icons/personal_account/Panic.svg"

                textButton.text: tr.panic
                textButton.color: ui.colors.red1

                backgroundItem.color: 'transparent'
                backgroundItem.border.color: ui.colors.red1

                anchors.horizontalCenter: parent.horizontalCenter

                onClicked: {
                    if (hub && !hub.current_user.alarm_button_access) {
                        Popups.text_popup(tr.error, tr.Com_no_access0)
                        return
                    }
                    Popups.hub_alarm_countdown_popup("PANIC", false)
                }

                /* -------------------------------------------------------- */
                /* desktop tests */
                accessibleIconName: "control_without-groups_alarm_icon"
                accessibleIconDescription: iconImage.source

                accessibleTextName: "control_without-groups_alarm_text"
                accessibleTextDescription: textButton.text

                accessibleAreaName: "control_without-groups_alarm_area"
                accessibleAreaDescription: "color-button:" + backgroundItem.color + " color-border:" + backgroundItem.border.color
                /* -------------------------------------------------------- */
            }
        }
    }

    Parts.GroupModeWithImages {}

    Connections {
        target: controlView

        onReBillingInfo: {
            billing.info = info
        }
    }
}