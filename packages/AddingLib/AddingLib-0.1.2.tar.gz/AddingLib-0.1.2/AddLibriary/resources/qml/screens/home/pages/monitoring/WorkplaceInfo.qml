import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/utils.js" as Utils


Rectangle {
    color: ui.colors.dark4
    Layout.minimumWidth: incidentPage.width
    Layout.maximumWidth: incidentPage.width
    Layout.fillHeight: true
    Layout.minimumHeight: gridLayout.implicitHeight + gridLayout.rows * 8
    Layout.maximumHeight: gridLayout.implicitHeight + gridLayout.rows * 8

    Item {
        width: parent.width - 64
        anchors {
            top: parent.top
            left: parent.left
            bottom: parent.bottom
        }

        GridLayout {
            id: gridLayout
            width: parent.width
            rows: 5
            columns: 2
            rowSpacing: 8
            columnSpacing: 24
            anchors {
                top: parent.top
                topMargin: 16
            }

            Item {
                Layout.minimumWidth: 144
                Layout.maximumWidth: 144
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.middle1
                    opacity: 0.6
                    text: tr.a911_employee_name
                    maximumLineCount: 2
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.light3
                    maximumLineCount: 2
                    font.pixelSize: 16
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    text: {
                        if (!incident) return ui.empty
                        if (!incident.workplace_employee) return ui.empty

                        return incident.workplace_employee.first_name + " " + incident.workplace_employee.last_name
                    }
                }
            }

            Item {
                Layout.minimumWidth: 144
                Layout.maximumWidth: 144
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.middle1
                    opacity: 0.6
                    text: tr.a911_login
                    maximumLineCount: 2
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.light3
                    maximumLineCount: 2
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    text: {
                        if (!incident) return ui.empty
                        if (!incident.workplace_employee) return ui.empty

                        return incident.workplace_employee.email
                    }
                }
            }

            Item {
                Layout.minimumWidth: 144
                Layout.maximumWidth: 144
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.middle1
                    opacity: 0.6
                    text: tr.machine_id
                    maximumLineCount: 2
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.light3
                    maximumLineCount: 2
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    text: {
                        if (!incident) return ui.empty
                        if (!incident.workplace) return ui.empty
                        if (!incident.workplace.machine_id) return ui.empty

                        return incident.workplace.machine_id
                    }
                }
            }

            Item {
                Layout.minimumWidth: 144
                Layout.maximumWidth: 144
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.middle1
                    opacity: 0.6
                    text: tr.workplaces_911_popup
                    maximumLineCount: 2
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.light3
                    maximumLineCount: 2
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    text: {
                        if (!incident) return ui.empty
                        if (!incident.workplace) return ui.empty
                        if (!incident.workplace.name) return ui.empty

                        return incident.workplace.name
                    }
                }
            }

            Item {
                Layout.minimumWidth: 144
                Layout.maximumWidth: 144
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.middle1
                    opacity: 0.6
                    text: tr.a911_status
                    maximumLineCount: 2
                    font.pixelSize: 12
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignRight
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        right: parent.right
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Item {
                Layout.fillWidth: true
                Layout.minimumHeight: 28
                Layout.maximumHeight: 28

                Rectangle {
                    width: 6
                    height: 6
                    radius: height / 2
                    anchors {
                        left: parent.left
                        verticalCenter: parent.verticalCenter
                    }

                    color: {
                        if (!incident || !incident.workplace) return "transparent"
                        if (incident.workplace.connection_status == "ONLINE") return ui.colors.green1
                        if (incident.workplace.connection_status == "OFFLINE") return ui.colors.red1
                        if (incident.workplace.connection_status == "LOGGED_OUT") return ui.colors.light3
                        return "transparent"
                    }
                }

                Custom.FontText {
                    width: parent.width - 24
                    height: parent.height
                    color: ui.colors.light3
                    maximumLineCount: 2
                    font.pixelSize: 14
                    wrapMode: Text.WordWrap
                    textFormat: Text.PlainText
                    elide: Text.ElideRight
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors {
                        left: parent.left
                        leftMargin: incident && incident.workplace && ["ONLINE", "OFFLINE", "LOGGED_OUT"].includes(incident.workplace.connection_status) ? 16 : 0
                        verticalCenter: parent.verticalCenter
                    }

                    text: {
                        if (!incident || !incident.workplace) return ui.empty
                        if (incident.workplace.connection_status == "ONLINE") return tr.online
                        if (incident.workplace.connection_status == "OFFLINE") return tr.offline
                        if (incident.workplace.connection_status == "LOGGED_OUT") return tr.logged_out_workplaces
                        return ui.empty
                    }
                }
            }
        }
    }

    Item {
        width: 64
        anchors {
            top: parent.top
            right: parent.right
            bottom: parent.bottom
        }

        Image {
            sourceSize.width: 48
            sourceSize.height: 48
            source: validMachine ? "qrc:/resources/images/icons/a-plus-button.svg" : "qrc:/resources/images/icons/a-plus-button-red.svg"
            visible: incident && incident.system_incident_type == "UNVERIFIED_LOGIN" && topLevel.manageVisible && !util.is_operator(appUser.role) && incident.workplace.verificationStatus != "VERIFIED"
            anchors {
                top: parent.top
                topMargin: 16
                horizontalCenter: parent.horizontalCenter
            }

            property var validMachine: incident && incident.workplace && incident.workplace.machine_id

            Custom.HandMouseArea {
                onClicked: {
                    if (parent.validMachine) {
                        Popups.create_workplace_popup(incident.workplace, incident.id)
                    } else {
                        Popups.text_popup(tr.information, tr.without_machine_id)
                    }
                }
            }
        }
    }
}
