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

    ScrollView {
        id: scrollView
        clip: true
        height: btnRect.visible && !btn.loading ? parent.height - 72 : parent.height

        anchors {
            top: parent.top
            left: parent.left
            right: parent.right
        }

        ScrollBar.vertical: Custom.ScrollBar {
            parent: scrollView
            anchors {
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }
        }

        ColumnLayout {
            spacing: 2
            anchors.fill: parent

            ObjectInfo { id: objectInfo }

            TabBarInfo {
                id: tabBarInfo

                Layout.maximumHeight: tabBarIsOpened ? scrollView.height - objectInfo.height - 2 : 260
            }

            EventsInfo {
                property var normalHeight: scrollView.height - tabBarInfo.height - objectInfo.height - 4

                Layout.maximumHeight: normalHeight < Layout.minimumHeight ? Layout.minimumHeight : normalHeight
            }
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
