import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom

Rectangle {
    color: ui.colors.dark3
    Layout.minimumWidth: manageIncident.width
    Layout.maximumWidth: manageIncident.width
    Layout.fillHeight: true
    Layout.minimumHeight: 240
    Layout.maximumHeight: 240

    Custom.EmptySpaceLogo {
        size: parent.width / 3
        visible: listView.model.length == 0
    }

    ListView {
        id: listView
        snapMode: ListView.SnapOneItem
        highlightRangeMode: ListView.StrictlyEnforceRange
        clip: true
        interactive: !incidentScrollBar.scrollVisible
        orientation: Qt.Horizontal
        highlightMoveDuration: 200
        highlightMoveVelocity: -1

        property var trueIndex: 0

        anchors {
            top: parent.top
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        RowLayout {
            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.top: parent.top
            anchors.topMargin: 12
            spacing: 16
            visible: listView.model.length > 1

            Image {
                source: "qrc:/resources/images/incidents/cards/a-control-left-yellow.svg"
                sourceSize.width: 12
                sourceSize.height: 21
                Custom.HandMouseArea {
                    anchors.fill: parent

                    onPressed: {
                        parent.scale = 1.1
                    }

                    onReleased: {
                        parent.scale = 1.0
                    }

                    onClicked: {
                        if (0 == listView.currentIndex) {
                            listView.currentIndex = incident.filtered_rapid_response_teams.length - 1
                            return
                        }
                        listView.currentIndex -= 1
                    }
                }
            }

            Image {
                source: "qrc:/resources/images/incidents/cards/a-control-right-yellow.svg"
                sourceSize.width: 12
                sourceSize.height: 21
                Custom.HandMouseArea {
                    anchors.fill: parent

                    onPressed: {
                        parent.scale = 1.1
                    }

                    onReleased: {
                        parent.scale = 1.0
                    }

                    onClicked: {
                        if (incident.filtered_rapid_response_teams.length - 1 == listView.currentIndex) {
                            listView.currentIndex = 0
                            return
                        }
                        listView.currentIndex += 1
                    }
                }
            }
        }

        model: {
            if (incident == null) return []
            return incident.filtered_rapid_response_teams
        }

        delegate: GBR {
            width:  ListView.view.width
            height: ListView.view.height
        }
    }
}