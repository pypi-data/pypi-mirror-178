import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/incidents.js" as Incidents

RowLayout {
    id: topLevel
    anchors.fill: parent
    property var incident: null
    property var incident_id: null
    property var manageVisible: {
        if (incident == null) return false
        return (incident.status == "PROCESSING") || incident.is_in_sleep_mode
    }

    visible: {
        if (incident == null) return false
        return incident.id == currentId
    }
    enabled: visible
    opacity: 0

    states: [
        State { when: visible;
            PropertyChanges { target: topLevel; opacity: 1.0 }
        },
        State { when: !visible;
            PropertyChanges { target: topLevel; opacity: 0.0 }
        }
    ]
    transitions: Transition {
        NumberAnimation { property: "opacity"; duration: 300 }
    }

    Component.onCompleted: {
        incident_id = incident.id
    }

    Component.onDestruction: {
        // console.log("incident destroyed!..")
    }

    function check() {
        if (!visible) return
        if (currentIncidentsModel == appCompany.filtered_snoozing_incidents_model) {
            if (!incident.is_in_sleep_mode) {
                currentId = null
                appCompany.filtered_snoozing_incidents_model.refilter()
                appCompany.incidents_model.dataChanged_()
                appCompany.incidents_model.update_incident(incident)
                return
            }
            return
        }
        if (incident.is_in_sleep_mode && (currentIncidentsModel != appCompany.filtered_snoozing_incidents_model)) {
            currentId = null
            return
        }
        if (incident.status == "PROCESSING") {

            let seeingRoles = new Set(["HEAD_OF_OPERATORS", "SENIOR_CMS_ENGINEER", "OWNER"])
            let currentRoles = new Set(appUser.role)
            let intersection = new Set([...seeingRoles].filter(x => currentRoles.has(x)));

            if (incident.assigned_employee != appUser.employee_id && intersection.size === 0) {
                topLevel.destroy()
                // application.debug("TEST -> incident -> currentId (incident) to null")
                currentId = null
            } else {
                // application.debug("TEST -> incident -> before changing currentIncidentsModel is -> " + currentIncidentsModel)
                if (currentIncidentsModel == appCompany.filtered_processing_incidents_model) {
                    // application.debug("TEST -> incident -> currentIncidentsModel needs no changes")
                    return
                }
                currentIncidentsModel = appCompany.filtered_processing_incidents_model
                // application.debug("TEST -> incident -> currentIncidentsModel changed to -> " + currentIncidentsModel)
            }
        }
    }

    Connections {
        target: incidentsView

        onTimeUpdated: {
            check()
        }
    }

    Connections {
        target: incident

        onStatusChanged: {
            check()
        }

        onDeleted: {
            topLevel.destroy()
            if (incident_id == currentId) {
                currentId = null
            }
        }
    }

    BaseInfo {
        id: baseInfo
    }

    ManageIncident {
        id: manageIncident
        enabled: incident.status != "CLOSE_AFTER_SLEEP"
        opacity: enabled ? 1 : 0.4
        visible: manageVisible
    }
}