import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"


Rectangle {
    color: "transparent"

    property alias photosGrid: photosGrid

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

                property var currentTab: newTab

                PanelTab {
                    id: newTab
                    text: tr.a911_by_novelty
                    Layout.minimumHeight: 36
                    Layout.maximumHeight: 36

                    selected: tabRow.currentTab == newTab

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            tabRow.currentTab = newTab
                        }
                    }
                }

                PanelTab {
                    id: roomTab
                    visible: false
                    text: tr.a911_via_rooms
                    Layout.minimumHeight: 36
                    Layout.maximumHeight: 36

                    selected: tabRow.currentTab == roomTab

                    Custom.HandMouseArea {
                        anchors.fill: parent
                        onClicked: {
                            tabRow.currentTab = roomTab
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

                PhotosGrid {
                    id: photosGrid
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