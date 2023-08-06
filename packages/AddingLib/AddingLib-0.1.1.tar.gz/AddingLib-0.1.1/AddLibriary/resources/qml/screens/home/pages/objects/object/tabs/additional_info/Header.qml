import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts"

Rectangle {
    id: topLevel

    color: ui.colors.dark3

    RowLayout {
        id: logsTabPanel
        spacing: 12
        height: 42
        anchors {
            left: parent.left
            leftMargin: 8
            verticalCenter: parent.verticalCenter
        }

        property var currentTab: allTab

        PanelTab {
            id: allTab

            text: tr.scenario_trigger_all
            selected: logsTabPanel.currentTab == allTab
            Layout.alignment: Qt.AlignLeft

            Custom.HandMouseArea {
                onClicked: {
                    facility.proxy_events_model.set_filter("ALL")
                    logsTabPanel.currentTab = allTab
                }
            }
        }
    }
}