import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: startMigration

    property var selectedHub: null

    signal reMigrationErrorsSignal(variant reErrors)

    Component.onCompleted: {
        app.migrationErrorsSignal.connect(reMigrationErrorsSignal)
    }

    Connections {
        target: app

        onActionSuccess: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/HubMigrationProcess.qml")
        }
    }

    onReMigrationErrorsSignal: {
        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/BlockingDataImport.qml", { "errorsModel": reErrors })
    }

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: startMigrationBar

        headerText: tr.hub_migration
        showCloseIcon: false
        showBackArrow: true
        showManualIcon: true
        isRound: false

        onManualAreaClicked: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/data_import_popups/HubMigrationInfoPopup.qml")
        }

        onBackAreaClicked: {
            if (hub.hub_type == "HUB_FIBRA") {
                loader.setSource(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/ReconnectBusesScreen.qml",
                    {selectedHub: selectedHub}
                )
            } else {
                loader.setSource(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/MigrationSettings.qml",
                    {selectedHub: selectedHub}
                )

            }
        }
    }

    DS3.ScrollView {
        width: parent.width
        height: startMigration.height

        anchors {
            fill: undefined
            top: startMigrationBar.bottom
            bottom: startButton.top
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.PlugImageHero {
            source: hub.hub_type == "HUB_FIBRA" ?
                "qrc:/resources/images/Athena/migration/HubImportReadyFibra.svg" :
                "qrc:/resources/images/Athena/migration/HubImportReady.svg"
        }

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            titleComponent.text: tr.get_started_data_import_title
        }

        DS3.Spacing {
            height: 24
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.CommentImportant {
                atomTitle.title: tr.get_started_data_import_one
                imageItem.source: "qrc:/resources/images/Athena/migration/Hub-M.svg"
            }

            DS3.CommentImportant {
                atomTitle.title: tr.get_started_data_import_two
                imageItem.source: "qrc:/resources/images/Athena/migration/Control-M.svg"
            }

            DS3.CommentImportant {
                atomTitle.title: tr.get_started_data_import_three
            }
        }
    }

    DS3.ButtonBar {
        id: startButton

        width: parent.width

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.start_data_import
        hasBackground: true
        hasComment: true
        commentText: tr.ready
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"

        button.onClicked: {
            if (donorHub.has_extender_w_eth && donorHub.firmware_version_dec < 213100) {
                Popups.popupByPath(
                    "qrc:/resources/qml/components/911/DS3/popups/Dialog.qml",
                    {
                        title: tr.rex_ethernet_no_migrate_title,
                        text: tr.rex_ethernet_no_migrate_descr,
                        firstButtonText: tr.ok,
                        firstButtonCallback: () => {
                            app.start_stream_hub_changes(donorHub.id)
                            Popups.please_wait_popup()
                            app.start_migration(donorHub.hub_id, hub.hub_id)
                        }
                    }
                )
            } else {
                app.start_stream_hub_changes(donorHub.id)
                Popups.please_wait_popup()
                app.start_migration(donorHub.hub_id, hub.hub_id)
            }
        }
    }
}