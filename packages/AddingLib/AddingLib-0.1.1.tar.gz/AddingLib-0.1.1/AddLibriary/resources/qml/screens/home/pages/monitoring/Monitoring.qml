import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/incidents.js" as Incidents
import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: monitoring
    color: ui.colors.black

    property var manageIncidentsUsesColumn: application.width > 1352 + 340

    RowLayout {
        anchors.fill: parent
        spacing: 0

        ColumnLayout {
            Layout.minimumWidth: 400
            Layout.minimumHeight: parent.height
            Layout.fillWidth: true
            spacing: 1

            IncidentsTable {
                id: incidentsView
                Layout.minimumWidth: 400
                Layout.minimumHeight: incidentsView.contentHeight
                Layout.maximumHeight: parent.parent.height
                Layout.fillWidth: true
            }

            Rectangle {
                Layout.minimumWidth: 400
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: ui.colors.dark4

                Custom.EmptySpaceLogo {
                    visible: incidentsView.model.length == 0
                }
            }
        }

        Item {
            Layout.fillWidth: true
            Layout.minimumWidth: 8
            Layout.maximumWidth: Layout.minimumWidth
        }

        IncidentPage {
            id: incidentPage
            visible: true
            Layout.fillWidth: true
            Layout.minimumWidth: {
                if (currentId == null) {
                      if (appCompany == null) return 0
                      if (home.currentIncidentsModel == appCompany.filtered_processing_incidents_model) {
                          return manageIncidentsUsesColumn ? 880 + 340 : 880
                      }
                      if (home.currentIncidentsModel == appCompany.filtered_snoozing_incidents_model) {
                          return manageIncidentsUsesColumn ? 880 + 340 : 880
                      }
                    return 540
                }
                var incident = Incidents.find_visible_incident(incidentPage, currentId)

                if (appCompany == null) {
                    return 540
                }

                if (incident == null) {
                    return 540
                }

                if (incident.manageVisible) {
                    return manageIncidentsUsesColumn ? 880 + 340 : 880
                }
//                if (["NEW", "VIEWING"].includes(incident.incident.status) && currentIncidentsModel != appCompany.filtered_new_or_viewing_incidents_model) {
//                    return 540
//                }
//                if (["PROCESSING"].includes(incident.incident.status) && currentIncidentsModel != appCompany.filtered_processing_incidents_model) {
//                    return 540
//                }
//                if (["SNOOZING"].includes(incident.incident.status) && currentIncidentsModel != appCompany.filtered_snoozing_incidents_model) {
//                    return 540
//                }


                return 540
            }
            Layout.maximumWidth: Layout.minimumWidth
            Layout.minimumHeight: parent.height
        }

        Item {
            Layout.fillWidth: true
            Layout.minimumWidth: 8
            Layout.maximumWidth: Layout.minimumWidth
        }
    }
}