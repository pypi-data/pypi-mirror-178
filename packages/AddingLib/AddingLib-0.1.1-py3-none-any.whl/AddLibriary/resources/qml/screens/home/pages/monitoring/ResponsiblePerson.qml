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
                text: tr.a911_responsible_person_responsible + " " + (index + 1) + " " + tr.a911_of + " " + incident.filtered_responsible_persons.length
                color: ui.colors.middle3
                font.pixelSize: 14
            }

            Custom.FontText {
                text: {
                    var temp = ""
                    if (!person) return temp
                    if (person.last_name) {
                        temp += person.last_name + " "
                    }
                    if (person.first_name) {
                        temp += person.first_name
                    }
                    return temp
                }
                color: ui.colors.light3
                font.pixelSize: 16
                Layout.preferredWidth: deleg.width
                elide: Text.ElideRight
                textFormat: Text.PlainText
            }

            Custom.ComboBox {
                Layout.fillWidth: true
                model: numbers
            }

            ColumnLayout {
                Layout.fillHeight: true
                Layout.minimumHeight: 80
                Layout.maximumHeight: 80
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
                            if (person_status == "REACHED") return
                            app.responsible_person_module.set_responsible_person_status(incident, person.id, 1) // # REACHED
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
                                if (person_status == "REACHED") {
                                    return "qrc:/resources/images/incidents/cards/a-green-badge.svg"
                                }
                                return "qrc:/resources/images/incidents/cards/a-default-badge.svg"
                            }
                            sourceSize.width: 40
                            sourceSize.height: 40
                        }
                        Text {
                            font.pixelSize: 14
                            text: tr.a911_contacted
                            color: {
                                if (person_status == "REACHED") return ui.colors.white
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
                            if (person_status == "UNREACHABLE") return
                            app.responsible_person_module.set_responsible_person_status(incident, person.id, 2) // # UNREACHED
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
                                if (person_status == "UNREACHABLE") {
                                    return "qrc:/resources/images/incidents/cards/a-red-badge.svg"
                                }
                                return "qrc:/resources/images/incidents/cards/a-default-badge.svg"
                            }
                            sourceSize.width: 40
                            sourceSize.height: 40
                        }
                        Text {
                            font.pixelSize: 14
                            text: tr.a911_not_available
                            color: {
                                if (person_status == "UNREACHABLE") return ui.colors.white
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
            color: ui.colors.green1
            anchors.top: parent.top
        }
    }
}

