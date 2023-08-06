import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom
import "qrc:/resources/qml/screens/home/pages/parts/"


Rectangle {
    id: responsibleTab

    property bool isEditable: facility.editable_sections.includes("RESPONSIBLE_PERSONS")

    color: ui.colors.black

    property var currentResponsibleIndex: -1
    property var currentResponsibleObject: null

    ColumnLayout {
        anchors.fill: parent
        spacing: 1

        Rectangle {
            color: ui.colors.dark3
            Layout.fillWidth: true
            Layout.minimumHeight: 48
            Layout.maximumHeight: 48

            RowLayout {
                width: parent.width
                height: 48
                anchors {
                    bottom: parent.bottom
                    left: parent.left
                    leftMargin: 8
                }

                PanelTab {
                    id: allTab
                    text: tr.scenario_trigger_all
                    selected: true
                    Layout.alignment: Qt.AlignVCenter
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 8

            ResponsibleList {
                Layout.fillWidth: true
                Layout.preferredWidth: 664
                Layout.fillHeight: true
            }

            ResponsibleView {
                Layout.preferredWidth: 328
                Layout.maximumWidth: 450
                Layout.fillHeight: true
                Layout.fillWidth: true
            }
        }
    }

    Component.onCompleted: {
        if (!facility.id) return

        app.responsible_person_module.start_stream_object_responsible_persons(facility.id)
    }
}
