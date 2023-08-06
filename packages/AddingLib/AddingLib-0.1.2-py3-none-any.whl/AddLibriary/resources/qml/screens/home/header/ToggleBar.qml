import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Item {
    id: toggleBar
    anchors.fill: parent

    property var events: 0
    property var in_progress: 0
    property var sleep: 0

    property var customWidth: 140
    property var customHeight: 34

    Component.onCompleted: {
        currentIncidentsModel = appCompany.filtered_new_or_viewing_incidents_model
    }

    Connections {
        target: appCompany.incidents_model

        onGoToIncident: {
            if (tab == "SLEEP") {
                sleepTabArea.clicked(true)
                application.selectIncidentWithId(incident_id)
                return
            }

            if (tab == "NEW_VIEWING") {
                newTabArea.clicked(true)
                application.selectIncidentWithId(incident_id)
                return
            }

            if (tab == "PROCESSING") {
                processingTabArea.clicked(true)
                application.selectIncidentWithId(incident_id)
                return
            }
        }
    }

    RowLayout {
        width: parent.width
        height: parent.height
        anchors.centerIn: parent

        spacing: 20

        Item {
            Layout.minimumWidth: 1
            Layout.fillWidth: true
        }

        Rectangle {
            radius: height / 2
            color: ui.colors.dark4

            Layout.minimumWidth: customWidth * 2
            Layout.minimumHeight: customHeight
            Layout.preferredWidth: customWidth * 2
            Layout.preferredHeight: customHeight

            Custom.RoundedRect {
                id: eventsItem
                width: customWidth - 1
                height: customHeight
                anchors.left: parent.left
                color: {
                    if (appCompany == null) return ui.colors.black
                    return currentIncidentsModel == appCompany.filtered_new_or_viewing_incidents_model ? ui.colors.white : ui.colors.dark4
                }

                topLeftCorner: true
                bottomLeftCorner: true

                Custom.FontText {
                    text: tr.a911_incidents
                    color: {
                        if (currentIncidentsModel == appCompany.filtered_new_or_viewing_incidents_model) return ui.colors.dark4
                        return ui.colors.middle1
                    }
                    font.pixelSize: 15
                    font.bold: true
                    anchors {
                        centerIn: parent
                        horizontalCenterOffset: events ? -10 : 0
                    }
                }

                Rectangle {
                    width: customHeight - 12
                    height: customHeight - 12
                    radius: height / 2
                    color: ui.colors.red1

                    visible: events

                    anchors {
                        right: parent.right
                        rightMargin: 4
                        verticalCenter: parent.verticalCenter
                    }

                    Custom.FontText {
                        text: events
                        font.pixelSize: 12
                        font.weight: Font.Bold
                        anchors.centerIn: parent
                    }
                }

                Custom.HandMouseArea {
                    id: newTabArea
                    anchors.fill: parent
                    onClicked: {
                        application.debug("company -> header -> 'new' toggle")
                        header.sidebarVisible = false
                        header.currentState = 0
                        // application.debug("TEST -> toggle bar -> before changing currentIncidentsModel is -> " + currentIncidentsModel)
                        if (currentIncidentsModel == appCompany.filtered_new_or_viewing_incidents_model) {
                            // application.debug("TEST -> toggle bar -> currentId & currentIncidentsModel need no changes")
                            return
                        }
                        currentId = null
                        // application.debug("TEST -> toggle bar -> currentId (incident) to null")
                        currentIncidentsModel = appCompany.filtered_new_or_viewing_incidents_model
                        // application.debug("TEST -> toggle bar -> currentIncidentsModel changed to -> " + currentIncidentsModel)
                    }
                }
            }

            Rectangle {
                width: 2
                height: customHeight
                color: ui.colors.black
                anchors.centerIn: parent
            }

            Custom.RoundedRect {
                id: inProgressItem
                width: customWidth - 1
                height: customHeight
                anchors.right: parent.right
                color: {
                    if (appCompany == null) return ui.colors.black
                    return currentIncidentsModel == appCompany.filtered_processing_incidents_model ? ui.colors.white : ui.colors.dark4
                }

                topRightCorner: true
                bottomRightCorner: true

                Custom.FontText {
                    text: tr.a911_in_processing
                    color: {
                        if (currentIncidentsModel == appCompany.filtered_processing_incidents_model) return ui.colors.dark4
                        return ui.colors.middle1
                    }
                    font.pixelSize: 15
                    font.bold: true
                    anchors {
                        centerIn: parent
                        horizontalCenterOffset: in_progress ? -10 : 0
                    }
                }

                Rectangle {
                    width: customHeight - 12
                    height: customHeight - 12
                    radius: height / 2
                    color: ui.colors.yellow1

                    visible: in_progress

                    anchors {
                        right: parent.right
                        rightMargin: 4
                        verticalCenter: parent.verticalCenter
                    }

                    Custom.FontText {
                        text: in_progress
                        font.pixelSize: 12
                        font.weight: Font.Bold
                        anchors.centerIn: parent
                    }
                }

                Custom.HandMouseArea {
                    id: processingTabArea
                    anchors.fill: parent
                    onClicked: {
                        application.debug("company -> header -> 'in progress' toggle")
                        header.sidebarVisible = false
                        header.currentState = 0
                        // application.debug("TEST -> toggle bar -> before changing currentIncidentsModel is -> " + currentIncidentsModel)
                        if (currentIncidentsModel == appCompany.filtered_processing_incidents_model) {
                            // application.debug("TEST -> toggle bar -> currentId & currentIncidentsModel need no changes")
                            return
                        }
                        currentId = null
                        // application.debug("TEST -> toggle bar -> currentId (incident) to null")
                        currentIncidentsModel = appCompany.filtered_processing_incidents_model
                        // application.debug("TEST -> toggle bar -> currentIncidentsModel changed to -> " + currentIncidentsModel)
                    }
                }
            }
        }

        Rectangle {
            id: sleepItem
            radius: height / 2
            color: {
                if (appCompany == null) return ui.colors.black
                return currentIncidentsModel == appCompany.filtered_snoozing_incidents_model ? ui.colors.white : ui.colors.dark4
            }

            Layout.minimumWidth: customWidth + 24
            Layout.minimumHeight: customHeight
            Layout.preferredWidth: customWidth + 24
            Layout.preferredHeight: customHeight

            Custom.FontText {
                text: tr.a911_sleeping
                color: {
                    if (currentIncidentsModel == appCompany.filtered_snoozing_incidents_model) return ui.colors.dark4
                    return ui.colors.middle1
                }
                font.pixelSize: 15
                font.bold: true
                anchors {
                    centerIn: parent
                    horizontalCenterOffset: sleep ? -10 : 0
                }
            }

            Rectangle {
                width: customHeight - 12
                height: customHeight - 12
                radius: height / 2
                color: ui.colors.middle1

                visible: sleep

                anchors {
                    right: parent.right
                    rightMargin: 4
                    verticalCenter: parent.verticalCenter
                }

                Custom.FontText {
                    text: sleep
                    font.pixelSize: 12
                    font.weight: Font.Bold
                    anchors.centerIn: parent
                }
            }

            Custom.HandMouseArea {
                id: sleepTabArea
                anchors.fill: parent
                onClicked: {
                    application.debug("company -> header -> 'sleep mode' toggle")
                    header.sidebarVisible = false
                    header.currentState = 0
                    // application.debug("TEST -> toggle bar -> before changing currentIncidentsModel is -> " + currentIncidentsModel)
                    if (currentIncidentsModel == appCompany.filtered_snoozing_incidents_model) {
                        // application.debug("TEST -> toggle bar -> currentId & currentIncidentsModel need no changes")
                        return
                    }
                    currentId = null
                    // application.debug("TEST -> toggle bar -> currentId (incident) to null")
                    currentIncidentsModel = appCompany.filtered_snoozing_incidents_model
                    // application.debug("TEST -> toggle bar -> currentIncidentsModel changed to -> " + currentIncidentsModel)
                }
            }
        }

        Item {
            Layout.minimumWidth: 1
            Layout.fillWidth: true
        }
    }
}