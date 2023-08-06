import QtQuick 2.12
import QtQuick.Controls 2.13
import QtGraphicalEffects 1.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: connections
    color: companyStack.color

    RowLayout {
        anchors.fill: parent
        spacing: 8

        Item {
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                id: connectionsLayout
                anchors.fill: parent
                spacing: 0

                Panel {
                    id: panel
                }

                Header {
                    id: header
                }

                ConnectionsList {
                    id: connectionsList
                }

                Custom.RoundedRect {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.rightMargin: infoConnectionsComponent.visible ? 0 : 8
                    color: ui.colors.dark3

                    Custom.EmptySpaceLogo {
                        visible: connectionsList.connectionsData.model.length == 0
                    }

                    radius: 10
                    topRightCorner: {
                        if (appCompany.filtered_fast_response_teams_model.length == 0 || connectionsList.connectionsData.ownCurrentIndex == -1) return false
                        return appCompany.filtered_fast_response_teams_model.length - 1 == connectionsList.connectionsData.ownCurrentIndex
                    }
                }
            }
        }

        Info {
            id: infoConnectionsComponent
        }
    }
}