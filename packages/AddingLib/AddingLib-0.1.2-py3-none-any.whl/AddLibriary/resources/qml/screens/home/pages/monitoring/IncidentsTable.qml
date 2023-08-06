import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/js/incidents.js" as Incidents
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/components/911/DS3" as DS3

ListView {
    id: incidentsView
    clip: true

    signal timeUpdated()
    signal processingFirstClicked()

    model: currentIncidentsModel
    boundsBehavior: Flickable.StopAtBounds

    Connections {
        target: home
        onCurrentIncidentsModelChanged: {
//            if ((currentId == null) && (currentIncidentsModel == appCompany.filtered_processing_incidents_model)) {
//                processingFirstClicked()
//            }
        }
    }


    spacing: 1

    ScrollBar.vertical: Custom.ScrollBar {}

    section.property: "is_system"
    section.criteria: ViewSection.FullString
    section.labelPositioning: ViewSection.CurrentLabelAtStart | ViewSection.InlineLabels
    section.delegate: Rectangle {
        color: ui.colors.dark3
        implicitHeight: 32
        implicitWidth: incidentsView.width

        RowLayout {
            visible: section == "false"
            anchors.fill: parent

            spacing: 1

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.maximumWidth: 48
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    text: tr.a911_status
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 80
                Layout.maximumWidth: 80
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    text: tr.a911_time
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.maximumWidth: 260
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    text: tr.object_name
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.fillWidth: true
                Layout.preferredHeight: 32
                visible: incidentsView.width > 700

                Custom.FontText {
                    text: tr.address
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 110
                Layout.maximumWidth: 110
                Layout.fillWidth: true
                Layout.preferredHeight: 32
                Layout.alignment: Qt.AlignRight

                Custom.FontText {
                    text: tr.source_monitoring
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }
        }

        RowLayout {
            visible: section == "true"
            anchors.fill: parent

            spacing: 1

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.maximumWidth: 48
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    text: tr.a911_status
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 80
                Layout.maximumWidth: 80
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    text: tr.a911_time
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.maximumWidth: parent.width - 240
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    text: tr.incident_cause
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 110
                Layout.maximumWidth: 110
                Layout.fillWidth: true
                Layout.preferredHeight: 32
                Layout.alignment: Qt.AlignRight

                Custom.FontText {
                    text: tr.source_monitoring
                    color: ui.colors.white
                    opacity: 0.7
                    font.pixelSize: 11
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }
        }

        Rectangle {
            width: parent.width
            anchors.bottom: parent.bottom
            color: ui.colors.black
        }
    }

    /*
    add: Transition {
        NumberAnimation { property: "opacity"; from: 0; to: 1.0; duration: 200; alwaysRunToEnd: true }
        NumberAnimation { property: "scale"; from: 0; to: 1.0; duration: 200; alwaysRunToEnd: true }
    }
    */

    populate: Transition {}

    delegate: Rectangle {
        id: deleg
        property var isCurrent: {
            if (incident == null) return false
            return currentId == incident.id
        }
        implicitHeight: 48
        implicitWidth: incidentsView.width
        color: isCurrent ? ui.colors.black : ui.colors.dark1

        Connections {
            target: incidentsView
            onTimeUpdated: {
                var out = util.incident_time_formatted(incident.timestamp)
                if (out.hours) {
                    timeLabel.font.pixelSize = 16
                    timeLabelSystem.font.pixelSize = 16
                    timeLabel.text = out.formatted_hours
                    timeLabelSystem.text = out.formatted_hours
                } else {
                    timeLabel.font.pixelSize = 20
                    timeLabelSystem.font.pixelSize = 20
                    timeLabel.text = out.formatted_minutes
                    timeLabelSystem.text = out.formatted_minutes
                }
                if (out.seconds > 30) {
                    timeLabel.color = ui.colors.red1
                    timeLabelSystem.color = ui.colors.red1
                } else {
                    timeLabel.color = ui.colors.white
                    timeLabelSystem.color = ui.colors.white
                }
                appCompany.incidents_model.dataChanged_()
                appCompany.incidents_model.update_incident(incident)
            }
            onProcessingFirstClicked: {
                if (index == 0) {
                    mouseAreaClick.clicked(true)
                }
            }
        }

        RowLayout {
            visible: incident && !incident.is_system_incident
            anchors.fill: parent

            spacing: 1

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.maximumWidth: 48
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Image {
                    width: 48
                    height: 48
                    mipmap: true
                    sourceSize.width: 48
                    sourceSize.height: 48
                    anchors.centerIn: parent

                    source: {
                        if (!incident) return ""
                        if (incident.is_in_sleep_mode) {
                            return "qrc:/resources/images/incidents/statuses/incident-status-snoozing.svg"
                        }
                        if (incident.status == "NEW") {
                            return "qrc:/resources/images/incidents/statuses/incident-status-priority.svg"
                        } else if (incident.assigned_rapid_response_teams.length && incident.status == "PROCESSING") {
                            return "qrc:/resources/images/incidents/statuses/incident-status-gbr.svg"
                        } else if (incident.status == "PROCESSING") {
                            return "qrc:/resources/images/incidents/statuses/incident-status-work.svg"
                        } else if (incident.status == "VIEWING") {
                            return "qrc:/resources/images/incidents/statuses/incident-status-look.svg"
                        }
                        return ""
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 80
                Layout.maximumWidth: 80
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    id: timeLabel
                    color: ui.colors.white
                    font.pixelSize: 20
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6

                    Component.onCompleted: {
                        var out = util.incident_time_formatted(incident.timestamp)
                        if (out.seconds > 30) {
                            color = ui.colors.red1
                        } else {
                            color = ui.colors.white
                        }
                        if (out.hours) {
                            font.pixelSize = 16
                            text = out.formatted_hours
                        } else {
                            font.pixelSize = 20
                            text = out.formatted_minutes
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.maximumWidth: 260
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    text: {
                        var hubId = incident && incident.hub_id ? incident.hub_id : ui.empty
                        if (!incident) return hubId
                        if (!incident.facility) return hubId
                        if (!incident.facility.facility_general_info) return hubId
                        if (!incident.facility.facility_general_info.name) return hubId

                        return "<b>" + incident.facility.facility_general_info.registration_number + "</b> <span style='color:gray'>/ " + incident.facility.facility_general_info.name + "</span>"
                    }
                    color: ui.colors.white
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    textFormat: Text.AutoText
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.fillWidth: true
                Layout.preferredHeight: 32
                visible: incidentsView.width > 700

                Custom.FontText {
                    text: {
                        if (!incident) return ui.empty
                        if (!incident.facility) return ui.empty
                        if (!incident.facility.facility_general_info) return ui.empty
                        if (!incident.facility.facility_general_info.address) return ui.empty

                        var cityValue = incident.facility.facility_general_info.address.city ? incident.facility.facility_general_info.address.city + ", " : ""
                        return incident.facility.facility_general_info.address.address_line1 ? cityValue + incident.facility.facility_general_info.address.address_line1 : ""
                    }
                    color: ui.colors.white
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    width: parent.width
                    elide: Text.ElideRight
                    wrapMode: Text.Wrap
                    textFormat: Text.PlainText
                    maximumLineCount: 2
                    rightPadding: 16
                    anchors {
                        left: parent.left
                        leftMargin: 6
                        verticalCenter: parent.verticalCenter
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 110
                Layout.maximumWidth: 110
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignRight
                ListView {
                    id: listView
                    anchors.fill: parent

                    model: incident.mini_events
                    orientation: ListView.Horizontal
                    boundsBehavior: Flickable.StopAtBounds

                    layoutDirection: Qt.RightToLeft

                    add: Transition {
                        ParallelAnimation {
                            NumberAnimation { properties: "x"; from: listView.width; duration: 200; easing.type: Easing.InQuart; alwaysRunToEnd: true }
                            NumberAnimation { properties: "scale"; from: 1.5; to: 1.0; duration: 200; easing.type: Easing.InQuart; alwaysRunToEnd: true }
                        }
                    }

                    addDisplaced: Transition {
                        NumberAnimation { properties: "x"; duration: 200; easing.type: Easing.InQuart }
                    }

                    delegate: Item {
                        width: 36
                        height: 48

                        DS3.Icon {
                            id: srcIcon

                            property var image_with_color: event.system_event ?
                                app.get_system_icon(event.system_event.type) :
                                app.get_notification_icon(event_code)

                            anchors.centerIn: parent

                            source: image_with_color.source
                            color: image_with_color.color
                        }
                    }
                }
            }
        }

        RowLayout {
            visible: incident && incident.is_system_incident
            anchors.fill: parent

            spacing: 1

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.maximumWidth: 48
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Image {
                    width: 48
                    height: 48
                    mipmap: true
                    sourceSize.width: 48
                    sourceSize.height: 48
                    anchors.centerIn: parent

                    source: {
                        if (!incident) return ""
                        if (incident.is_in_sleep_mode) {
                            return "qrc:/resources/images/incidents/statuses/incident-status-snoozing.svg"
                        }
                        if (incident.status == "NEW") {
                            return "qrc:/resources/images/incidents/statuses/incident-status-priority.svg"
                        } else if (incident.assigned_rapid_response_teams.length && incident.status == "PROCESSING") {
                            return "qrc:/resources/images/incidents/statuses/incident-status-gbr.svg"
                        } else if (incident.status == "PROCESSING") {
                            return "qrc:/resources/images/incidents/statuses/incident-status-work.svg"
                        } else if (incident.status == "VIEWING") {
                            return "qrc:/resources/images/incidents/statuses/incident-status-look.svg"
                        }
                        return ""
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 80
                Layout.maximumWidth: 80
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    id: timeLabelSystem
                    color: ui.colors.white
                    font.pixelSize: 20
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    anchors.fill: parent
                    anchors.left: parent.left
                    anchors.leftMargin: 6

                    Component.onCompleted: {
                        var out = util.incident_time_formatted(incident.timestamp)
                        if (out.seconds > 30) {
                            color = ui.colors.red1
                        } else {
                            color = ui.colors.white
                        }
                        if (out.hours) {
                            font.pixelSize = 16
                            text = out.formatted_hours
                        } else {
                            font.pixelSize = 20
                            text = out.formatted_minutes
                        }
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 48
                Layout.maximumWidth: parent.width - 240
                Layout.fillWidth: true
                Layout.preferredHeight: 32

                Custom.FontText {
                    width: parent.width - 16
                    height: parent.height
                    color: ui.colors.light3
                    font.bold: true
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideRight
                    textFormat: Text.PlainText
                    wrapMode: Text.WordWrap
                    maximumLineCount: 2
                    anchors {
                        left: parent.left
                        leftMargin: 6
                        verticalCenter: parent.verticalCenter
                    }

                    text: {
                        if (!incident) return ui.empty
                        if (!incident.system_incident_type) return ui.empty

                        var temp = incident.system_incident_type == "LOST_CONNECTION" ? tr.incident_when_operator_offline : tr.incident_when_unapproved_login
                        return temp
                    }
                }
            }

            Rectangle {
                color: "transparent"
                Layout.minimumWidth: 110
                Layout.maximumWidth: 110
                Layout.fillWidth: true
                Layout.fillHeight: true
                Layout.alignment: Qt.AlignRight

                ListView {
                    id: listViewSystem
                    anchors.fill: parent
                    model: incident.mini_events
                    orientation: ListView.Horizontal
                    boundsBehavior: Flickable.StopAtBounds

                    layoutDirection: Qt.RightToLeft

                    add: Transition {
                        ParallelAnimation {
                            NumberAnimation { properties: "x"; from: listViewSystem.width; duration: 200; easing.type: Easing.InQuart; alwaysRunToEnd: true }
                            NumberAnimation { properties: "scale"; from: 1.5; to: 1.0; duration: 200; easing.type: Easing.InQuart; alwaysRunToEnd: true }
                        }
                    }

                    addDisplaced: Transition {
                        NumberAnimation { properties: "x"; duration: 200; easing.type: Easing.InQuart }
                    }

                    delegate: Item {
                        width: 24
                        height: 24

                        DS3.Icon {
                            id: srcIconSystem

                            property var image_with_color: event.system_event ?
                                app.get_system_icon(event.system_event.type) :
                                app.get_notification_icon(event_code)

                            anchors.centerIn: parent

                            source: image_with_color.source
                            color: image_with_color.color
                        }
                    }
                }
            }
        }

        Connections {
            target: application

            onSelectIncidentWithId: {
                if (!incident || !incident.id) return

                if (incident_id == incident.id && currentId != incident.id) {
                    mouseAreaClick.clicked(true)
                }
            }
        }

        Custom.HandMouseArea {
            id: mouseAreaClick
            anchors.fill: parent
            onClicked: {
                if (!incident || !incident.id) {
                    Popups.text_popup(tr.error, tr.unknown_error)
                    return
                }

                if (currentId == incident.id) {
                    currentId = null
                    return
                }
                application.debug("company -> monitoring -> select incident (" + incident.id + ")", false)
                __ga__.report("activity", "company -> monitoring -> select incident")

                var exists = Incidents.is_incident_exists(incidentPage, incident.id)

                if (!exists) {
                    Incidents.create_incident(incidentPage, incident)
                }

                currentId = incident.id
                if (!incident.viewers.includes(appUser.user_id)) {
                    app.incident_module.start_viewing_incident(incident.id)
                }

                if (!incident.is_activities_stream_present) {
                    app.incident_module.start_incident_activities_stream(incident)
                }

                if (incident.is_system_incident) return

                if (!incident.is_events_stream_present) {
                    app.journal_module.start_log_entries_stream(incident)
                }
                if (!incident.is_responsible_stream_present) {
                    app.responsible_person_module.start_responsible_persons_stream(incident)
                }
                if (!incident.is_response_teams_stream_present) {
                    app.fast_response_team_module.start_rapid_response_teams_stream(incident)
                }
            }
        }
    }

    Timer {
        running: true
        interval: 1000
        triggeredOnStart: true
        repeat: true
        onTriggered: {
            incidentsView.timeUpdated()
            appCompany.incidents_model.update_incidents()
        }
    }
}