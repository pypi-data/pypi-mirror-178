import QtQuick 2.12
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.13


import "qrc:/resources/js/desktop/popups.js" as PopupsDesk
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/utils.js" as Utils
import "qrc:/resources/qml/animations/" as Anime
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/desktop/"


Column {
    id: column

    width: parent.width
    visible: hub && !hub.groups_enabled

    anchors {
        top: parent.top
        topMargin: 16
    }

    Repeater {
        model: [
            {
                icon: "qrc:/resources/images/icons/a-hub-status-icon-armed.svg",
                text: tr.arm,
                command: "ARM",
            },
            {
                icon:  "qrc:/resources/images/icons/a-hub-status-icon-disarmed.svg",
                text: tr.disarm,
                command: "DISARM",
            },
            {
                icon:  "qrc:/resources/images/icons/night-mode.svg",
                text: tr.part_arm,
                command: hub.groups_enabled && hub.groups_night_mode_enabled ? "PARTIAL_DISARM" : "PARTIAL_ARM",
            },
            {
                icon: "qrc:/resources/images/icons/panic-alt.svg",
                text: tr.panic,
                command: "PANIC",
            }
        ]

        Rectangle {
            width: parent.width
            height: 40

            color: ui.colors.dark1

            Item {
                id: repeaterAction

                anchors.fill: parent
                Custom.HandMouseArea {
                    anchors.fill: parent
                    onClicked: {
                        var command = modelData.command

                        if (command == "PANIC") {
                            if (hub && !hub.current_user.alarm_button_access) {
                                Popups.text_popup(tr.error, tr.Com_no_access0)
                                return
                            }
                            Popups.hub_alarm_countdown_popup(command, false, null)
                        } else {
                            repeaterAction.enabled = false
                            security_timer.start()
                            app.hub_management_module.perform_security_action(command, false, null)
                        }

                        contextMenu.close()
                    }
                }

                Timer {
                    id: security_timer

                    running: false
                    repeat: false
                    interval: 1000
                    onTriggered: repeaterAction.enabled = true
                }

                Connections {
                    target: app.hub_management_module
                    onMalfunctionsFound: {
                        PopupsDesk.malfunctions_popup(jsonData, null)
                    }
                }

                Image {
                    id: statusIcon

                    sourceSize.width: 24
                    sourceSize.height: 24
                    source: modelData.icon

                    anchors {
                        left: parent.left
                        leftMargin: 6
                        verticalCenter: parent.verticalCenter
                    }
                }

                Custom.FontText {
                    width: parent.width
                    text: modelData.text
                    font.pixelSize: 14
                    color: ui.colors.light3

                    anchors {
                        left: statusIcon.right
                        leftMargin: 6
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Rectangle {
                width: parent.width
                height: 1

                color: ui.colors.black
                anchors.bottom: parent.bottom
            }
        }
    }
}