import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


Rectangle {
    id: workplaces
    color: companyStack.color

    RowLayout {
        anchors.fill: parent
        spacing: 8

        Item {
            Layout.alignment: Qt.AlignTop | Qt.AlignLeft
            Layout.fillWidth: true
            Layout.fillHeight: true

            ColumnLayout {
                id: workplacesLayout
                anchors.fill: parent
                spacing: 0

                Panel {
                    id: panel
                }

                WorkplacesList {
                    id: workplacesList
                }
            }

            Rectangle {
                anchors.fill: parent
                color: ui.colors.black
                opacity: 0.5
                visible: infoWorkplacesComponent.editMode

                Custom.HandMouseArea {
                    cursorShape: Qt.ArrowCursor
                }
            }
        }

        Info {
            id: infoWorkplacesComponent
        }
    }

    Connections {
        target: app.workplaces_module

        onGetWorkplaces: {
            infoWorkplacesComponent.currentObject = null
        }
    }

    Connections {
        target: appCompany.filtered_workplaces_model

        onRefiltered: {
            infoWorkplacesComponent.currentObject = null
        }
    }
}