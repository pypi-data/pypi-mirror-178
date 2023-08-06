import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/images.js" as Images


Rectangle {
    id: migrationPartiallySuccess

    property bool devices_screen

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: migrationPartiallySuccessBar

        headerText: devices_screen ? tr.devices_in_migration : tr.buttons_import
        showCloseIcon: false
        showBackArrow: true
        isRound: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/FinishDataImport.qml")
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: migrationPartiallySuccessBar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.SettingsContainer {
            width: parent.width

            DS3.CommentImportant {
                atomTitle.title: tr.not_transferred_import_descr
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            Repeater {
                id: repeater

                width: parent.width

                model: devices_screen ? devices.devices_migration_result : devices.buttons_migration_result

                delegate: DS3.InfoStatus {
                    width: parent.width

                    source: {
                        if (device.obj_type == '1d') {
                            return Images.get_image(modelData.obj_type, "Small", modelData.input_type, modelData.assigned_mtr_object.mtr2_available ? modelData.custom_alarm_S2 : modelData.custom_alarm)
                        }
                        return Images.get_image(modelData.obj_type, "Small", modelData.color, null, modelData.subtype)
                    }
                    atomTitle.title: modelData.name
                    atomTitle.subtitle: modelData.migration_status == "WARNING" ? tr.not_transferred_import : tr.transferred_import
                    atomTitle.subtitleColor: modelData.migration_status == "WARNING" ? ui.ds3.figure.warningContrast : ui.ds3.figure.positiveContrast
                }
            }
        }
    }
}