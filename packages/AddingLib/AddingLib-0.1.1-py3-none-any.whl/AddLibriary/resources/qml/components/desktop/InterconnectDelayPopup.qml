import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/desktop/"
import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


AjaxPopup {
    id: popup
    width: 360
    height: 360

    modal: true
    focus: true

    property var fire_alarms: null
    property var trigger: null

    property int timerTime: hub.interconnect_delay_expiration_diff

    closePolicy: Popup.CloseOnEscape | Popup.NoAutoClose

    property var management: null
    property var actionsEnabled: {
        if (!appUser.company_id || !popup.management) return true
        return companyAccess.HUB_INTERCONNECT_PROCESS && popup.management.facility_access
    }

    Component.onCompleted: countdown.start()

    Rectangle {
        id: rect

        width: 360
        height: popup.height
        color: "#252525"

        radius: 3
        border.width: 1
        border.color: "#1a1a1a"

        Item {
            id: headerItem

            width: parent.width
            height: 78

            anchors {
                top: parent.top
                topMargin: 14
            }

            Text {
                id: labelText

                width: 288
                height: contentHeight

                text: {
                    let device = fire_alarms[0]

                    if (trigger == "smoke") {
                        return util.insert(tr.potential_smoke_interconnect_delay, [device.name, device.room_name])
                    } else if (trigger == "co") {
                        return util.insert(tr.potential_co_interconnect_delay, [device.name, device.room_name])
                    } else if (trigger == "temp") {
                        return util.insert(tr.potential_temperature_interconnect_delay, [device.name, device.room_name])
                    } else {
                        return util.insert(tr.potential_temperature_difference_interconnect_delay, [device.name, device.room_name])
                    }
                }

                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 20
                font.weight: Font.Bold
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter

                anchors {
                    top: parent.top
                    left: parent.left
                    leftMargin: 38
                }
            }

            Image {
                id: icoClose

                source: "qrc:/resources/images/desktop/icons/ic-close.svg"

                width: 16
                height: 16
                opacity: 0.9
                anchors {
                    top: parent.top
                    left: labelText.right
                }

                MouseArea {
                    id: mouseArea
                    anchors.fill: icoClose
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: popup.close()
                    onEntered: icoClose.opacity = 1.0
                    onExited: icoClose.opacity = 0.9
                }
            }
        }

        Column {
            id: column
            width: parent.width

            spacing: 12

            anchors {
                top: headerItem.bottom
                topMargin: 18
                bottom: delayInterconnectButton.top
            }

            Text {
                id: potentialAlertCheck

                width: parent.width - 48
                height: contentHeight

                text: tr.potential_alert_check

                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter

                anchors.horizontalCenter: parent.horizontalCenter
            }

            Item {
                width: parent.width
                height: 32
            }

            Text {
                id: interconnectDelayTimerText

                width: parent.width - 48
                height: contentHeight

                text: tr.interconnect_delay_timer_popup

                color: ui.colors.light1
                font.family: roboto.name
                font.pixelSize: 14
                font.weight: Font.Bold
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter

                anchors.horizontalCenter: parent.horizontalCenter
            }

            DS3.ProgressCountdownS {
                id: countdown

                anchors.horizontalCenter: parent.horizontalCenter

                timeElapsedOnStart: time - hub.interconnect_delay_expiration_diff
                time: hub.interconnect_delay_timeout

                onTimerFinished: popup.close()
            }
        }

        Item {
            id: delayInterconnectButton

            width: parent.width
            height: 48

            enabled: popup.actionsEnabled
            opacity: enabled ? 1 : 0.4

            anchors.bottom: parent.bottom

            Rectangle {
                anchors.top: parent.top
                height: 1
                width: parent.width
                color: ui.colors.light1
                opacity: 0.1
            }

            Text {
                id: delayInterconnectText

                width: parent.width
                height: contentHeight

                text: tr.delay_interconnect

                color: ui.colors.green1
                font.family: roboto.name
                font.pixelSize: 14
                font.weight: Font.Light
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter

                anchors.centerIn: parent

            }

            MouseArea {
                anchors.fill: parent

                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor

                onClicked: {
                    Popups.confirm_or_cancel(
                        tr.are_you_sure_early_warning,
                        tr.are_you_sure_early_warning_info,
                        function todo() {
                            app.hub_management_module.delay_interconnect(hub.hub_id)
                        },
                        tr.delay_interconnect_short
                    )
                }
            }
        }
    }

    Connections {
        target: app

        onActionSuccess: {
            popup.close()
        }
    }
}