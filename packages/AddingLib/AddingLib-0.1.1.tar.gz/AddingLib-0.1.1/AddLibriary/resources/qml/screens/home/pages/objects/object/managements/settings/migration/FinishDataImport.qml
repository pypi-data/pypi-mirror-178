import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: migrationSuccess

    property bool isAllDevicesMigrated: {
        for (var i = 0; i < devices.devices_migration_result.length; i++) {
            if (devices.devices_migration_result[i].migration_status == "WARNING") return false
        }
        return true
    }

    property bool isAllButtonsMigrated: {
        for (var i = 0; i < devices.buttons_migration_result.length; i++) {
            if (devices.buttons_migration_result[i].migration_status == "WARNING") return false
        }
        return true
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: migrationSuccessBar

        headerText: tr.hub_migration
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: migrationSuccessBar.bottom
            bottom: closeButton.top
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.PlugImageHero {
            anchors.horizontalCenter: parent.horizontalCenter

            source: {
                if (["SERVER_TIMED_OUT", "MIGRATION_FAILED"].includes(hub.config_migration.migration_result)) {
                    if (hub.hub_type != "HUB_FIBRA") return "qrc:/resources/images/Athena/migration/HubToHubImportPartiallySuccess.svg"
                    return donorHub.hub_type == "HUB_FIBRA" ?
                        "qrc:/resources/images/Athena/migration/FibraToFibraImportPartiallySuccess.svg" :
                        "qrc:/resources/images/Athena/migration/HubToFibraImportPartiallySuccess.svg"
                }
                if (hub.config_migration.migration_result == "FINISHED_OK") {
                    if (hub.hub_type != "HUB_FIBRA") return "qrc:/resources/images/Athena/migration/HubToHubImportSuccess.svg"
                    return donorHub.hub_type == "HUB_FIBRA" ?
                        "qrc:/resources/images/Athena/migration/FibraToFibraImportSuccess.svg" :
                        "qrc:/resources/images/Athena/migration/HubToFibraImportSuccess.svg"
                }
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            anchors.horizontalCenter: parent.horizontalCenter

            titleComponent.text: tr.migration_successed_status
            descComponent.text: tr.post_migration_info
            visible: hub.config_migration.migration_result == "FINISHED_OK"
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            visible: hub.config_migration.migration_result != "FINISHED_OK"

            DS3.InfoStatus {
                width: parent.width

                visible: hub.config_migration.data_transfer_state == "FINISHED"
                atomTitle {
                    title: tr.settings
                    subtitle: tr.transferred_import
                    subtitleColor: ui.ds3.figure.positiveContrast
                }
            }

            DS3.InfoStatus {
                width: parent.width

                visible: isAllDevicesMigrated
                atomTitle {
                    title: tr.devices
                    subtitle: tr.transferred_import
                    subtitleColor: ui.ds3.figure.positiveContrast
                }
            }

            DS3.SettingsNavigationTitlePrimaryStatus {
                title: tr.devices
                subtitle: tr.partially_transferred_import
                subtitleColor: ui.ds3.figure.warningContrast
                visible: !isAllDevicesMigrated

                onEntered: loader.setSource(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/PartiallyTransferredWarning.qml",
                    {"devices_screen": true}
                )
            }

            DS3.InfoStatus {
                width: parent.width

                visible: isAllButtonsMigrated
                atomTitle {
                    title: tr.buttons
                    subtitle: tr.transferred_import
                    subtitleColor: ui.ds3.figure.positiveContrast
                }
            }

            DS3.SettingsNavigationTitlePrimaryStatus {
                title: tr.buttons
                subtitle: tr.partially_transferred_import
                subtitleColor: ui.ds3.figure.warningContrast
                visible: !isAllButtonsMigrated

                onEntered: {
                    loader.setSource(
                        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/PartiallyTransferredWarning.qml",
                        {"devices_screen": false}
                    )
                }
            }
        }
    }

    DS3.ButtonBar {
        id: closeButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.go_to_devices_button
        hasBackground: true

        button.onClicked: {
            popup.close()
        }
    }
}
