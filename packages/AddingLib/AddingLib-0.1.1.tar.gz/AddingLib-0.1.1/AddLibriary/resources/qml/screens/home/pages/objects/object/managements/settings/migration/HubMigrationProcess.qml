import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


Rectangle {
    id: migrationProcess

    property var sideMargin: 24
    property bool devicesReady

    Connections {
        target: management

        onNewDevicesCame: {
            migrationProcess.devicesReady = true
        }
    }

    Connections {
        target: hub.config_migration

        onDataChanged: {
            if (hub.config_migration.migration_result != "IN_PROGRESS") loader.setSource(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/FinishDataImport.qml"
            )
        }
    }
    
    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: migrationProcessBar

        headerText: tr.hub_migration
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {

        anchors {
            fill: undefined
            top: migrationProcessBar.bottom
            bottom: completeButton.top
            left: parent.left
            right: parent.right
        }

        padding: sideMargin

        DS3.PlugImageHero {
            anchors.horizontalCenter: parent.horizontalCenter

            source: {
                if (hub.hub_type != "HUB_FIBRA") return "qrc:/resources/images/Athena/migration/HubToHubImportInProgress.svg"
                return donorHub.hub_type == "HUB_FIBRA" ?
                    "qrc:/resources/images/Athena/migration/FibraToFibraImportInProgress.svg" :
                    "qrc:/resources/images/Athena/migration/HubToFibraImportInProgress.svg"
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.ProgressBarStatus {
            id: progressBarStatus

            amount: 3 + filteredWithoutButtonsDevices.length + filteredButtonsDevices.length // 3 for data
            current: {
                let counter = 0
                if (hub.config_migration.data_transfer_state == "FINISHED") counter += 3
                counter += devices.buttons_migrated_count
                counter += devices.devices_migrated_count
                return counter
            }
            statusTexts: {
                let status_list = []
                if (hub.config_migration.data_transfer_state == "IN_PROGRESS") return [tr.user_data_copying]
                if (hub.config_migration.data_transfer_state == "FINISHED" && !migrationProcess.devicesReady) {
                    return [tr.user_data_copying]
                }
                if (hub.config_migration.migration_button_devices_state == "FINISHED" && hub.config_migration.migration_button_devices_state == "FINISHED") return tr.almost_ready
                if (filteredWithoutButtonsDevices.length) status_list.push(util.insert(tr.devices_transferred_import_desktop, [devices.devices_migrated_count, filteredWithoutButtonsDevices.length]))
                if (filteredButtonsDevices.length) status_list.push(util.insert(tr.buttons_to_transfer_desktop, [devices.buttons_migrated_count, filteredButtonsDevices.length]))
                return status_list
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.ButtonText {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            text: tr.summary_devices_info
            visible: hub.config_migration.data_transfer_state != "IN_PROGRESS"

            onClicked: {
                Popups.migration_summary_popup()
            }
        }
    }

    DS3.ButtonBar {
        id: completeButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        width: parent.width

        buttonText: tr.complete_now_button
        hasBackground: true
        enabled: {
            if (["SERVER_TIMED_OUT", "FINISHED_OK", "MIGRATION_FAILED"].includes(hub.config_migration.migration_result)) return true
            return (["IN_PROGRESS", "FINISHED"].includes(hub.config_migration.migration_button_devices_state)) || (["IN_PROGRESS", "FINISHED"].includes(hub.config_migration.migration_frame_devices_state))
        }
        button.isOutline: true
        hasComment: true
        commentText: tr.in_progress_now
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"

        button.onClicked: {
            Popups.popupByPath("qrc:/resources/qml/components/911/DS3/popups/Dialog.qml", {
                title: tr.stop_migration_popup,
                text: tr.stop_migration_popup_info,
                isVertical: true,
                firstButtonCallback: () => {
                    completeButton.enabled = false
                    completeButton.commentText = tr.finishing_progress
                    app.stop_migration(hub.hub_id)
                },
                firstButtonText: tr.interrupt_button,
                firstButtonIsOutline: true,
                isFirstButtonRed: true,
                secondButtonText: tr.cancel,
            })
        }
    }
}
