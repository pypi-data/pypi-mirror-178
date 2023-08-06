import QtQuick 2.12
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.13

import "qrc:/resources/qml/components/911/" as Custom


ColumnLayout{
    anchors {
        fill: parent
        topMargin: 16
    }

    Rectangle {
        color: "transparent"
        Layout.fillWidth: true
        Layout.preferredHeight: 88

        Custom.Button {
            width: 152
            transparent: true
            text: tr.save_scenario
            anchors {
                right: parent.right
                rightMargin: 16
            }
            onClicked: {
                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/tabs/additional_info/AdditionalView.qml")
                app.save_facility_maintenance_data({"connected_by": connectedBy.valueText.control.text,
                "installed_by": connectedBy2.valueText.control.text,
                "facility_engineer": connectedBy3.valueText.control.text})
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
        Layout.preferredHeight: 80
        Layout.topMargin: 8

        Custom.TextFieldEdit {
            id: connectedBy
            distance: 20
            width: 440
            anchors.centerIn: parent
            key: tr.a911_connected_to_the_remote
            valueText.control.maximumLength: 50
            value: {
                if (!facility.facility_maintenance.data) return ""
                return facility.facility_maintenance.data.connected_by
            }
        }
    }

    Rectangle {
        color: "transparent"
        Layout.fillWidth: true
        Layout.preferredHeight: 80
        Layout.topMargin: 8

        Custom.TextFieldEdit {
            id: connectedBy2
            distance: 20
            width: 440
            anchors.centerIn: parent
            key: tr.a911_assembly
            valueText.control.maximumLength: 50
            value: {
                if (!facility.facility_maintenance.data) return ""
                return facility.facility_maintenance.data.installed_by
            }
        }
    }

    Rectangle {
        color: "transparent"
        Layout.fillWidth: true
        Layout.preferredHeight: 80
        Layout.topMargin: 8

        Custom.TextFieldEdit {
            id: connectedBy3
            distance: 20
            width: 440
            anchors.centerIn: parent
            key: tr.a911_object_ingeneer
            valueText.control.maximumLength: 50
            value: {
                if (!facility.facility_maintenance.data) return ""
                return facility.facility_maintenance.data.facility_engineer
            }
        }
    }

    Item {
        Layout.fillHeight: true
    }

    Component.onCompleted: {
        if (!facility.id) return

        app.start_facility_maintenance_stream()
    }
}