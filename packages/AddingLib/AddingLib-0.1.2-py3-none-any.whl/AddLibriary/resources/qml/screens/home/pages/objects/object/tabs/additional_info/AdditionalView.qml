import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


ColumnLayout{
    id: additionalTab

    property bool isEditable: facility.editable_sections.includes("MAINTENANCE_DATA")

    anchors {
        fill: parent
        topMargin: 16
        horizontalCenter: parent.horizontalCenter
    }

    Rectangle {
        color: "transparent"
        Layout.fillWidth: true
        Layout.preferredHeight: 88

        Item {
            width: 152
            height: 40
            anchors {
                right: parent.right
                rightMargin: 16
            }
            visible: additionalTab.isEditable

            Custom.Button {
                width: parent.width
                transparent: true
                text: tr.edit
                onClicked: loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/AdditionalEditInfo.qml")
            }
        }
    }

    Rectangle {
        Layout.preferredWidth: 440 + (parent.width - 440) / 2
        Layout.preferredHeight: 1
        Layout.alignment: Qt.AlignRight
        color: ui.colors.light3
        opacity: 0.1
    }

    Rectangle {
        color: "transparent"
        Layout.fillWidth: true
        Layout.preferredHeight: 56
        Layout.topMargin: 8

        Custom.TextFieldStatic {
            id: connectedBy
            width: 440
            anchors.centerIn: parent
            key: tr.a911_connected_to_the_remote
            value: {
                if (!facility.facility_maintenance.data) return ""
                return facility.facility_maintenance.data.connected_by
            }
        }
    }

    Rectangle {
        Layout.preferredWidth: 440 + (parent.width - 440) / 2
        Layout.preferredHeight: 1
        Layout.alignment: Qt.AlignRight
        color: ui.colors.light3
        opacity: 0.1
    }

    Rectangle {
        color: "transparent"
        Layout.fillWidth: true
        Layout.preferredHeight: 56
        Layout.topMargin: 8

        Custom.TextFieldStatic {
            id: connectedBy2
            width: 440
            anchors.centerIn: parent
            key: tr.a911_assembly
            value: {
                if (!facility.facility_maintenance.data) return ""
                return facility.facility_maintenance.data.installed_by
            }
        }
    }

    Rectangle {
        Layout.preferredWidth: 440 + (parent.width - 440) / 2
        Layout.preferredHeight: 1
        Layout.alignment: Qt.AlignRight
        color: ui.colors.light3
        opacity: 0.1
    }

    Rectangle {
        color: "transparent"
        Layout.fillWidth: true
        Layout.preferredHeight: 56
        Layout.topMargin: 8

        Custom.TextFieldStatic {
            id: connectedBy3
            width: 440
            anchors.centerIn: parent
            key: tr.a911_object_ingeneer
            value: {
                if (!facility.facility_maintenance.data) return ""
                return facility.facility_maintenance.data.facility_engineer
            }
        }
    }

    Rectangle {
        Layout.preferredWidth: 440 + (parent.width - 440) / 2
        Layout.preferredHeight: 1
        Layout.alignment: Qt.AlignRight
        color: ui.colors.light3
        opacity: 0.1
    }

    Item {
        Layout.fillHeight: true
    }

    Component.onCompleted: {
        if (!facility.id) return

        app.start_facility_maintenance_stream()
    }
}