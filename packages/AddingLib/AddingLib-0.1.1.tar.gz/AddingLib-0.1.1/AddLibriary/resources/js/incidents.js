function create_incident(parent, incident) {
    var incidentPage = incident.is_system_incident ? "qrc:/resources/qml/screens/home/pages/monitoring/SystemIncident.qml" : "qrc:/resources/qml/screens/home/pages/monitoring/Incident.qml"
    var component = Qt.createComponent(incidentPage)
    var err = component.errorString()
    if (err) console.log(err)
    var incident = component.createObject(parent, {"incident": incident})
    return incident
}

function is_incident_exists(parent, incident_id) {
    for(var i=0; i<parent.children.length; i++) {
        if (parent.children[i].incident_id && parent.children[i].incident_id == incident_id) {
            return true
        }
    }
    return false
}

function find_visible_incident(parent, incident_id) {
    for(var i=0; i<parent.children.length; i++) {
        if (parent.children[i].incident && parent.children[i].incident.id == incident_id) {
            if (parent.children[i].visible) {
                return parent.children[i]
            }
        }
    }
    return null
}