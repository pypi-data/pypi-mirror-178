import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/monitoring/incident_tabbar/"


Rectangle {
    id: incidentPage
    color: "transparent"
    border.width: 0
    border.color: "red"
    Layout.minimumWidth: 540
    Layout.maximumWidth: 540
    Layout.minimumHeight: parent.height

    property var tabBarIsOpened: false

    ColumnLayout {

        anchors.fill: parent
        spacing: 8

        WorkplaceInfo {}

        EventsInfo {}

        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 72
            visible: btnRect.visible && !btn.loading
        }
    }

    Rectangle {
        id: btnRect
        width: parent.width
        height: 72
        color: (btn.loading) ? "transparent" : ui.colors.dark3

        anchors.bottom: parent.bottom

        visible: {
            if (incident == null) return false
            return ["NEW", "VIEWING"].includes(incident.status)
        }

        Custom.Button {
            id: btn
            width: parent.width - 32
            height: 40
            text: tr.start_work_monitoring
            anchors.centerIn: parent
            enabledCustom: companyAccess.INCIDENTS_WORKPLACE_PROCESS

            onClicked: {
                application.debug("company -> monitoring -> incident (" + incident.id + ") -> move to 'in progress'", false)
                __ga__.report("activity", "company -> monitoring -> incident -> move to 'in progress'")
                loading = true
                app.incident_module.start_processing_incident(incident.id)
            }

            loading_background_color: ui.colors.dark1

            Connections {
                target: app.incident_module
                onStartProcessingIncidentResult: {
                    if (data.id == incident.id) btn.loading = result
                }
            }
        }
    }
}
