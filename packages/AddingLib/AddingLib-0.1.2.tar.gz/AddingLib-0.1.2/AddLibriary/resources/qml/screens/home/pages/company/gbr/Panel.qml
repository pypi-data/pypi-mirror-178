import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"
import "qrc:/resources/js/popups.js" as Popups


Rectangle {
    color: ui.colors.dark3
    Layout.alignment: Qt.AlignTop | Qt.AlignLeft
    Layout.fillWidth: true
    Layout.minimumHeight: 112
    Layout.maximumHeight: 112
    Layout.rightMargin: infoGbrComponent.visible ? 0 : 8

    RowLayout {
        spacing: 24
        width: parent.width - 48
        height: 48
        anchors {
            top: parent.top
            topMargin: 8
            horizontalCenter: parent.horizontalCenter
        }

        Item {
            id: searchItem
            Layout.fillWidth: true
            Layout.minimumHeight: parent.height
            Layout.maximumHeight: parent.height

            Custom.SearchField {
                width: parent.width - 8
                height: 38
                anchors.centerIn: parent
                placeHolderText: tr.a911_search_via_gbr

                onSearchStarted: {
                    appCompany.filtered_fast_response_teams_model.set_filter_text(data)
                }
            }
        }

        Item {
            id: addItem
            Layout.alignment: Qt.AlignTop | Qt.AlignRight
            Layout.minimumHeight: parent.height
            Layout.minimumWidth: 220
            Layout.maximumHeight: parent.height
            Layout.maximumWidth: 220
            visible: companyAccess.RRU_ADJUST

            Item {
                anchors.fill: parent

                Custom.Button {
                    width: parent.width
                    text: tr.a911_add_crew
                    transparent: true
                    color: ui.colors.green1
                    anchors.centerIn: parent

                    onClicked: {
                        application.debug("company -> company info -> rru -> add rru")
                        Popups.add_fast_response_team_popup()
                    }
                }
            }
        }
    }

    RowLayout {
        id: tabRow
        spacing: 12
        height: 42

        anchors {
            bottom: parent.bottom
            bottomMargin: 6
            left: parent.left
            leftMargin: 24
        }

        property var currentTab: allTab

        PanelTab {
            id: allTab
            text: tr.scenario_trigger_all
            selected: tabRow.currentTab == allTab

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = allTab
                    appCompany.filtered_fast_response_teams_model.set_filter_role("")
                }
            }
        }

        PanelTab {
            id: deactivatedTab
            text: tr.a911_deactivated
            selected: tabRow.currentTab == deactivatedTab

            Custom.HandMouseArea {
                anchors.fill: parent
                onClicked: {
                    tabRow.currentTab = deactivatedTab
                    appCompany.filtered_fast_response_teams_model.set_filter_role("UNACTIVE")
                }
            }
        }
    }
}
