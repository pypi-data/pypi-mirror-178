import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/monitoring/incident_tabbar/"


Rectangle {
    id: tabBarInfo
    color: ui.colors.dark3
    Layout.minimumWidth: incidentPage.width
    Layout.maximumWidth: incidentPage.width
    Layout.fillHeight: true
    Layout.minimumHeight: Layout.maximumHeight

    property var currentTab: incident.motion_cam_events.length > 0 ? 3 : 1

    property alias photosGrid: photosLayout.photosGrid

    ColumnLayout {
        id: columnLayout
        width: parent.width
        height: tabBarInfo.height
        spacing: 0

        RowLayout {
            Layout.fillWidth: true
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48

            spacing: 0

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: 48
                Layout.maximumHeight: 48
                color: currentTab == 0 ? "transparent" : ui.colors.black

                Custom.FontText {
                    anchors.centerIn: parent
                    text: tr.a911_notes
                    color: currentTab == 0 ? ui.colors.white : ui.colors.middle1
                }

                Custom.HandMouseArea {
                    anchors.fill: parent
                    onClicked: {
                        currentTab = 0
                        tabBarIsOpened = false
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: 48
                Layout.maximumHeight: 48
                color: currentTab == 1 ? "transparent" : ui.colors.black

                Custom.FontText {
                    anchors.centerIn: parent
                    text: tr.a911_scheme
                    color: currentTab == 1 ? ui.colors.white : ui.colors.middle1
                }

                Custom.HandMouseArea {
                    anchors.fill: parent
                    onClicked: {
                        currentTab = 1
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: 48
                Layout.maximumHeight: 48
                color: currentTab == 2 ? "transparent" : ui.colors.black

                Custom.FontText {
                    anchors.centerIn: parent
                    text: tr.devices
                    color: currentTab == 2 ? ui.colors.white : ui.colors.middle1
                }

                Custom.HandMouseArea {
                    anchors.fill: parent
                    onClicked: {
                        currentTab = 2
                    }
                }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.minimumHeight: 48
                Layout.maximumHeight: 48
                color: currentTab == 3 ? "transparent" : ui.colors.black
                visible: incident.motion_cam_events.length > 0

                Custom.FontText {
                    anchors.centerIn: parent
                    text: "MotionCam"
                    color: currentTab == 3 ? ui.colors.white : ui.colors.middle1
                }

                Rectangle {
                    width: 24
                    height: 24
                    radius: height / 2
                    color: ui.colors.red1

                    visible: incident.motion_cam_events.length > 0

                    anchors {
                        right: parent.right
                        rightMargin: 4
                        top: parent.top
                        topMargin: 4
                    }

                    Custom.FontText {
                        text: incident.motion_cam_events.length
                        font.pixelSize: 12
                        font.weight: Font.Bold
                        anchors.centerIn: parent
                    }
                }

                Custom.HandMouseArea {
                    anchors.fill: parent
                    onClicked: {
                        currentTab = 3
                    }
                }
            }
        }

        StackLayout {
            id: stackLayout
            Layout.fillWidth: true
            Layout.fillHeight: {
                return true
            }
            currentIndex: currentTab

            NotesLayout {
                id: notesLayout
            }
            SchemesLayout {}
            DevicesLayout {}
            PhotosLayout {
                id: photosLayout
            }
        }
    }
}