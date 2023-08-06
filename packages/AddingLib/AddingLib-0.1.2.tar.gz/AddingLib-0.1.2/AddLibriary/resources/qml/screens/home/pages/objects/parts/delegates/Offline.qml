import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/js/popups.js" as Popups
import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/events/parts"
import "qrc:/resources/qml/screens/home/pages/objects/parts"


Rectangle {
    width: header.width
    color: ui.colors.dark1
    height: 48

    property var header: objectsTable.headerItem

    Rectangle {
        width: parent.width
        height: 1
        color: ui.colors.black
        anchors.bottom: parent.bottom
    }

    ObjectMouseArea {}

    RowLayout {
        spacing: 0
        height: 48

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[0] ? header.headerRow.children[0].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: number ? number : ui.empty
                color: ui.colors.light3
                width: parent.width - 16
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[2] ? header.headerRow.children[2].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: name ? name : ui.empty
                color: ui.colors.light1
                font.pixelSize: 16
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[4] ? header.headerRow.children[4].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: address ? address : ui.empty
                color: ui.colors.middle1
                font.pixelSize: 14
                width: parent.width - 16
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 2
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[6] ? header.headerRow.children[6].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Custom.FontText {
                text: hub_id ? hub_id : ui.empty
                color: ui.colors.light3
                width: parent.width - 16
                font.pixelSize: 14
                wrapMode: Text.WordWrap
                elide: Text.ElideRight
                textFormat: Text.PlainText
                maximumLineCount: 1
                anchors {
                    left: parent.left
                    leftMargin: 12
                    verticalCenter: parent.verticalCenter
                }
            }
        }

        TableDivider { isHeader: false }

        Item {
            clip: true
            Layout.fillHeight: true
            Layout.minimumWidth: header.headerRow.children[8] ? header.headerRow.children[8].width : 0
            Layout.maximumWidth: Layout.minimumWidth

            Image {
                id: incidentStatus
                sourceSize.width: parent.height
                sourceSize.height: parent.height
                anchors.centerIn: parent
                visible: source != ""
                source: {
                    if (!object) return ""
                    if (!object.incident_info) return ""
                    if (!object.incident_info.incident_status) return ""

                    if (object.incident_info.incident_status == "NEW") return "qrc:/resources/images/incidents/statuses/incident-status-priority.svg"
                    if (object.incident_info.incident_status == "CLOSED") return "qrc:/resources/images/incidents/statuses/incident-status-closed.svg"
                    if (object.incident_info.incident_status == "VIEWING") return "qrc:/resources/images/incidents/statuses/incident-status-look.svg"
                    if (object.incident_info.incident_status == "CLOSE_AFTER_SLEEP") return "qrc:/resources/images/incidents/statuses/incident-status-close-after-sleep.svg"
                    if (object.incident_info.incident_status == "PROCESSING") {
                        if (object.sleep_until && object.sleep_until.seconds && (object.sleep_until.seconds > Math.floor(Date.now() / 1000))) {
                            return "qrc:/resources/images/incidents/statuses/incident-status-snoozing.svg"
                        }
                        return "qrc:/resources/images/incidents/statuses/incident-status-work.svg"
                    }

                    return ""
                }

                Custom.HandMouseArea {
                    onClicked: {
                        if (!object) return
                        if (!object.incident_info) return
                        if (!object.incident_info.incident_id) return
                        if (!object.incident_info.incident_status) return

                        if (object.incident_info.incident_status == "CLOSED") {
                            var iconY = mapToItem(home, incidentStatus.x, incidentStatus.y).y

                            function action(activities) {
                                Popups.incidents_logs(activities, parent, incidentStatus.x + 24, incidentStatus.y + 32, iconY)
                                objectsTable.action = null
                            }

                            objectsTable.action = action
                            app.incident_module.get_activities(object.incident_info.incident_id)
                            return
                        }

                        if (!companyAccess.MONITORING) return
                        appCompany.incidents_model.go_to_incident(object.incident_info.incident_id)
                    }
                }
            }
        }
    }
}