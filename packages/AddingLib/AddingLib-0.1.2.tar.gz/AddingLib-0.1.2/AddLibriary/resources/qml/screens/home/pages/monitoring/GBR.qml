import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Page {

    contentItem: Item {
        id: deleg
        anchors {
            fill: parent
            margins: 16
        }
        ColumnLayout {
            spacing: 8
            anchors.fill: parent
            Custom.FontText {
                text: tr.response_unit + " " + (index + 1) + " " + tr.a911_of + " " + incident.filtered_rapid_response_teams.length
                color: ui.colors.middle3
                font.pixelSize: 14
                Layout.preferredWidth: deleg.width
                elide: Text.ElideRight
                textFormat: Text.PlainText
            }
            Custom.FontText {
                text: name ? name : ""
                color: ui.colors.light3
                font.pixelSize: 16
                elide: Text.ElideRight
                textFormat: Text.PlainText
                rightPadding: 32
                Layout.fillWidth: true
            }
            Custom.ComboBox {
                Layout.fillWidth: true
                model: numbers
                copyVisible: activeFocus
            }

            ColumnLayout {
                Layout.fillHeight: true
                Layout.minimumHeight: 120
                Layout.maximumHeight: 120
                Layout.fillWidth: true
                spacing: 0

                Item {
                    Layout.fillHeight: true
                    Layout.minimumHeight: 40
                    Layout.maximumHeight: 40
                    Layout.fillWidth: true

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (team_status == "SENT") return
                            app.fast_response_team_module.set_rapid_response_team_status(incident, team_id, 1) // # SENT
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.middle1
                        opacity: 0.2
                    }

                    RowLayout {
                        height: parent.height
                        Image {
                            mipmap: true
                            source: {
                                if (team_status == "SENT") {
                                    return "qrc:/resources/images/incidents/cards/a-yellow-badge.svg"
                                }
                                return "qrc:/resources/images/incidents/cards/a-default-badge.svg"
                            }
                            sourceSize.width: 40
                            sourceSize.height: 40
                        }
                        Text {
                            font.pixelSize: 14
                            text: tr.a911_group_sent
                            color: {
                                if (team_status == "SENT") return ui.colors.white
                                return ui.colors.middle1
                            }
                        }
                    }
                }

                Item {
                    Layout.fillHeight: true
                    Layout.minimumHeight: 40
                    Layout.maximumHeight: 40
                    Layout.fillWidth: true

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (team_status == "ARRIVED") return
                            app.fast_response_team_module.set_rapid_response_team_status(incident, team_id, 3) // # ARRIVED
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.middle1
                        opacity: 0.2
                    }

                    RowLayout {
                        height: parent.height
                        Image {
                            mipmap: true
                            source: {
                                if (team_status == "ARRIVED") {
                                    return "qrc:/resources/images/incidents/cards/a-yellow-badge.svg"
                                }
                                return "qrc:/resources/images/incidents/cards/a-default-badge.svg"
                            }
                            sourceSize.width: 40
                            sourceSize.height: 40
                        }
                        Text {
                            font.pixelSize: 14
                            text: tr.a911_arrived
                            color: {
                                if (team_status == "ARRIVED") return ui.colors.white
                                return ui.colors.middle1
                            }
                        }
                    }
                }
                Item {
                    Layout.fillHeight: true
                    Layout.minimumHeight: 40
                    Layout.maximumHeight: 40
                    Layout.fillWidth: true

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            if (team_status == "UNREACHABLE") return
                            app.fast_response_team_module.set_rapid_response_team_status(incident, team_id, 4) // # UNREACHABLE
                        }
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: ui.colors.middle1
                        opacity: 0.2
                    }

                    RowLayout {
                        height: parent.height
                        Image {
                            mipmap: true
                            source: {
                                if (team_status == "UNREACHABLE") {
                                    return "qrc:/resources/images/incidents/cards/a-red-badge.svg"
                                }
                                return "qrc:/resources/images/incidents/cards/a-default-badge.svg"
                            }
                            sourceSize.width: 40
                            sourceSize.height: 40
                        }
                        Text {
                            font.pixelSize: 14
                            text: tr.a911_group_unavailable
                            color: {
                                if (team_status == "UNREACHABLE") return ui.colors.white
                                return ui.colors.middle1
                            }
                        }
                    }
                }
            }
            Item {
                Layout.fillHeight: true
            }
        }
    }

    background: Rectangle {
        color: ui.colors.dark3

        Rectangle {
            width: parent.width
            height: monitoring.manageIncidentsUsesColumn ? 1 : 0
            color: ui.colors.yellow1
            anchors.top: parent.top
        }
    }
}

