import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/utils.js" as Utils
import "qrc:/resources/js/images.js" as Images
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/qml/screens/pro/pages/hubs/hub/tabs/control/"
import "qrc:/resources/qml/components/desktop/" as CustomDesktop
import "qrc:/resources/qml/components/911/DS/components" as DSComponents
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: wrapper

    width: parent.width
    height: 64

    color: ui.colors.dark4
    anchors.top: parent.top

    RowLayout {
        width: parent.width - 32
        height: parent.height - 16

        anchors.centerIn: parent

        Item {
            id: hubObjectItem

            Layout.minimumWidth: parent.width / 4
            Layout.maximumWidth: Layout.minimumWidth
            Layout.fillHeight: true

            Row {
                anchors.fill: parent

                spacing: 18

                Item {
                    id: imageItem

                    width: 48
                    height: 48

                    property var serverSource: (hub && hub.small_image_link && hub.small_image_link != "WRONG" && !hub.small_image_link.endsWith("00000000_small.jpg")) ? hub.small_image_link : ""
                    property var defaultSource: Images.get_image(hub.image_type_name, "Small", hub.color)
                    property int timerTime: hub ? hub.exit_timer_expiration_diff : 0
                    property var arm_timer: {
                        if (hub.two_stage_arming_progress_status == 2) { return hub.app_exit_timer }
                        else if (hub.two_stage_arming_progress_status == 3) { return hub.second_stage_exit_timer }
                        else if (hub.two_stage_arming_progress_status == 5) { return hub.second_stage_exit_timer }
                        return 0
                    }

                    Image {
                        id: hubImage

                        anchors.centerIn: parent

                        source: imageItem.serverSource ? imageItem.serverSource : imageItem.defaultSource
                        visible: !imageItem.serverSource

                        onStatusChanged: {
                            if (status == Image.Error) {
                                imageItem.serverSource = ""
                                source = imageItem.defaultSource
                            }
                        }
                    }

                    OpacityMask {
                        anchors.fill: hubImage

                        source: hubImage
                        visible: !hubImage.visible

                        maskSource: Rectangle {
                            width: 64
                            height: 64
                            radius: width / 2
                            visible: imageItem.serverSource
                        }

                        Rectangle {
                            width: 48
                            height: 48

                            radius: width / 2
                            color: "#66f8df52" // 66 - alpha chanel

                            visible: hub.two_stage_arming_progress_status == 4
                            border {
                                color: ui.colors.yellow1
                                width: 1
                            }
                        }
                    }

                    Connections {
                        target: hub

                        onTsaStatusChanged: {
                            if (hub.two_stage_arming_progress_status == 4) return
                            if((hub.two_stage_arming_progress_status > 1 && hub.two_stage_arming_progress_status != 5 && !timer.running) || (hub.two_stage_arming_progress_status == 5 && timer.running)) {
                                imageItem.timerTime = hub.exit_timer_expiration_diff
                                timeCircle.arcBegin = timer.seconds_to_arc(imageItem.arm_timer) * (imageItem.arm_timer - imageItem.timerTime)
                                timer.reset()
                                timer.start()
                            } else {
                                timer.stop()
                                timeCircle.arcBegin = 0
                            }
                        }
                    }

                    Timer {
                        id: timer

                        property var timeOnStart: null
                        property var timeElapsed: 0
                        property var time: 0

                        function reset() {
                            time = imageItem.timerTime
                            timeOnStart = Date.now() / 1000
                            timeElapsed = 0
                        }
                        function seconds_to_arc(seconds) { return 360 / seconds }

                        running: false
                        interval: 100
                        repeat: true
                        triggeredOnStart: true


                        onTriggered: {
                            timeElapsed = Math.round(Date.now() / 1000 - timeOnStart)
                            imageItem.timerTime = time - timeElapsed + 1
                            timeCircle.arcBegin = timer.seconds_to_arc(imageItem.arm_timer) * (imageItem.arm_timer - imageItem.timerTime)
                            if (imageItem.timerTime == 0) {
                                timer.stop()
                                timeCircle.arcBegin = 0
                                return
                            }
                        }

                        Component.onCompleted: {
                            if (hub.two_stage_arming_progress_status == 4) return
                            if((hub.two_stage_arming_progress_status > 1 && hub.two_stage_arming_progress_status != 5 && !timer.running) || (hub.two_stage_arming_progress_status == 5 && timer.running)) {
                                timeCircle.arcBegin = timer.seconds_to_arc(imageItem.arm_timer) * (imageItem.arm_timer - hub.exit_timer_expiration_diff)
                                timer.reset()
                                timer.start()
                            }
                        }
                    }

                    CustomDesktop.AjaxAltTimeCircle {
                        id: timeCircle

                        anchors.fill: hubImage

                        size: 48
                        visible: timer.running

                        colorCircle: {
                            if (hub.two_stage_arming_progress_status == 2) {
                                return ui.colors.red1
                            } else if (hub.two_stage_arming_progress_status == 3 || hub.two_stage_arming_progress_status == 5) {
                                return ui.colors.lime1
                            }
                            return "transparent"
                        }

                        arcBegin: 0
                        arcEnd: 360
                        lineWidth: 1
                        colorBackground: "transparent"
                        showBackground: true
                        isPie: true
                        opacityPie: 0.4
                        addCircleToPie: true
                    }
                }

                Item {
                    id: nameAndId

                    height: parent.height
                    width: 160

                    DS3.Text {
                        id: panelHubName

                        width: parent.width

                        anchors {
                            top: parent.top
                            topMargin: 4
                            left: parent.left
                        }

                        text: hub ? hub.name : ui.empty
                        color: ui.colors.white
                        elide: Text.ElideRight
                        verticalAlignment: Text.AlignVCenter
                    }

                    DS3.Text {
                        id: panelHubId

                        width: parent.width

                        anchors {
                            left: parent.left
                            bottom: parent.bottom
                            bottomMargin: 4
                        }

                        text: hub ? "ID  " + hub.hub_id.toUpperCase() : ui.empty
                        color: ui.colors.light3
                        wrapMode: Text.NoWrap
                        verticalAlignment: Text.AlignVCenter
                    }
                }
            }
        }

        Item {
            id: hubStateItem

            Layout.minimumWidth: stateTextItem.contentWidth
            Layout.maximumWidth: Layout.minimumWidth
            Layout.fillHeight: true

            property var imageUrl: ""
            property var stateText: ""
            property var textColor: ui.colors.white

            property var nothing: {
                if (!hub) return Utils.get_data_hub_state("DISARMED")

                var stateHub = hub.groups_enabled ? hub.state_with_groups : hub.state

                if ((hub.firmware_version_dec >= 209100) && hub.two_stage_arming_progress_status > 1) {
                    stateHub = hub.tsa_status
                }
                [hubStateItem.imageUrl, hubStateItem.stateText, hubStateItem.textColor] = Utils.get_data_hub_state(stateHub)
            }

            Item {
                width: 64
                height: parent.height

                anchors {
                    left: parent.left
                    verticalCenter: parent.verticalCenter
                }

                Image {
                    sourceSize.width: 40
                    sourceSize.height: 40
                    source: "qrc:/resources/images/facilities/info/a.HubStatus-Convex.svg"
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    Image {
                        sourceSize.width: 24
                        sourceSize.height: 24
                        anchors.centerIn: parent
                        source: hubStateItem.imageUrl

                        /* ------------------------------------------------ */
                        /* desktop tests */
                        Accessible.name: "panel_state_icon"
                        Accessible.description: source
                        Accessible.role: Accessible.Graphic
                        /* ------------------------------------------------ */
                    }
                }

                Item {
                    width: 24
                    height: parent.height

                    anchors.right: parent.right

                    Custom.Triangle {
                        rotation: 0
                        scale: 0.8
                        anchors.centerIn: parent
                    }
                }
            }

            Custom.FontText {
                id: stateTextItem

                width: contentWidth
                height: contentHeight

                text: hubStateItem.stateText

                maximumLineCount: 1
                color: hubStateItem.textColor
                font.pixelSize: 14

                wrapMode: Text.NoWrap
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignVCenter

                anchors {
                    left: parent.left
                    leftMargin: 64
                    verticalCenter: parent.verticalCenter
                }

                /* ------------------------------------------------ */
                /* desktop tests */
                Accessible.name: "panel_state_text"
                Accessible.description: text
                Accessible.role: Accessible.Paragraph
                /* ------------------------------------------------ */
            }

            Custom.HandMouseArea {
                onClicked: {
                    contextMenu.popup()
                }
            }

            ContexMenuControl {
                id: contextMenu
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
        }

        Item {
            id: additionalRowItem

            Layout.minimumWidth: additionalRow.width + 32
            Layout.maximumWidth: Layout.minimumWidth
            Layout.fillHeight: true

            Row {
                id: additionalRow

                anchors.centerIn: parent

                spacing: 16
                height: parent.height

                Row {
                    height: parent.height

                    InterconnectButton { id: interconnectButton }

                    InterconnectDelayButton { id: interconnectDelayButton }
                }

                RestoreAlarmButton { id: restoreAlarmButton }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            visible: additionalRowItem.visible
        }

        Item {
            Layout.minimumWidth: malfText.contentWidth + 48
            Layout.maximumWidth: Layout.minimumWidth
            Layout.fillHeight: true

            Rectangle {
                width: 8
                height: width

                radius: height / 2
                color: ui.colors.red3
                anchors {
                    left: parent.left
                    leftMargin: 16
                    verticalCenter: parent.verticalCenter
                }
            }

            AjaxChimesControl {
                anchors {
                    verticalCenter: parent.verticalCenter
                    right: malfText.left
                    rightMargin: 46
                }
            }

            Custom.FontText {
                id: malfText

                anchors {
                    left: parent.left
                    leftMargin: 32
                    verticalCenter: parent.verticalCenter
                }

                color: ui.colors.light3
                maximumLineCount: 1
                font.pixelSize: 12
                wrapMode: Text.NoWrap
                textFormat: Text.PlainText
                verticalAlignment: Text.AlignVCenter
                text: {
                    var count = !hub ? 0 : hub.warnings_total
                    return tr.malfunctions + ": " + count
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: permissionItem.visible
        }

        Item {
            Layout.minimumWidth: permissionItem.width + 64
            Layout.maximumWidth: Layout.minimumWidth
            Layout.fillHeight: true

            DSComponents.HubPermissions {
                id: permissionItem

                anchors.centerIn: parent

                visible: !!management && !!hub && !!hub.current_user
                isPermanentAccess: hub.current_user.has_full_access && management.pro_access_time == 0
                endTimestamp: management.pro_access_time + Date.now() / 1000
                isCurrentUserPro: true

                onTimeEnded: management.pro_access_time_expired()
            }
        }
    }
}
