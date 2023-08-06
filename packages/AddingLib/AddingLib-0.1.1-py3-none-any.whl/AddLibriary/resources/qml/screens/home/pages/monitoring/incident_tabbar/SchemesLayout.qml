import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"


Rectangle {
    color: "transparent"

    Custom.EmptySpaceLogo {
        size: parent.width / 4
        visible: incident.proxy_facility_media ? incident.proxy_facility_media.length == 0 : true
    }

    ColumnLayout {
        spacing: 0
        anchors.fill: parent

        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true

            RowLayout {
                id: tabRow
                spacing: 6
                height: 42
                anchors {
                    top: parent.top
                    left: parent.left
                    leftMargin: 16
                }

                property var currentTab: allTab

                onCurrentTabChanged: {
                    schemesGrid.currentIndex = -1
                }

                PanelTab {
                    id: allTab
                    text: tr.all_photo
                    Layout.minimumHeight: 36
                    Layout.maximumHeight: 36

                    selected: tabRow.currentTab == allTab

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            tabRow.currentTab = allTab
                            incident.proxy_facility_media.set_filter("ALL")
                        }
                    }
                }

                PanelTab {
                    id: roadTab
                    text: tr.a911_driving_directions
                    Layout.minimumHeight: 36
                    Layout.maximumHeight: 36

                    selected: tabRow.currentTab == roadTab

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            tabRow.currentTab = roadTab
                            incident.proxy_facility_media.set_filter("ROAD_MAP")
                        }
                    }
                }

                PanelTab {
                    id: buildingTab
                    text: tr.a911_building_plans
                    Layout.minimumHeight: 36
                    Layout.maximumHeight: 36

                    selected: tabRow.currentTab == buildingTab

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            tabRow.currentTab = buildingTab
                            incident.proxy_facility_media.set_filter("FLOOR_PLAN")
                        }
                    }
                }
            }

            ScrollView {
                clip: true
                width: parent.width
                anchors {
                    top: tabRow.bottom
                    topMargin: 8
                    bottom: parent.bottom
                }

                SchemesGrid {
                    id: schemesGrid
                    anchors.fill: parent
                }
            }
        }

        Rectangle {
            color: ui.colors.dark2
            Layout.fillWidth: true
            Layout.preferredHeight: 32

            Custom.Triangle {
                rotation: tabBarIsOpened ? 180 : 0
                scale: 0.8
                anchors.centerIn: parent
            }

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabBarIsOpened = !tabBarIsOpened
                }
            }
        }
    }
}