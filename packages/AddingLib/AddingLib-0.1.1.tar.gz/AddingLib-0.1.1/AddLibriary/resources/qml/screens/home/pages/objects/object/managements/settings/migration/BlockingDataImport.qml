import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: blockingDataImportScreen

    property var errorsModel: []

    signal reMigrationErrorsSignal(variant reErrors)

    onReMigrationErrorsSignal: {
        blockingDataImportScreen.errorsModel = reErrors
    }

    Component.onCompleted: {
        app.migrationErrorsSignal.connect(reMigrationErrorsSignal)
    }

    Connections {
        target: app

        onActionSuccess: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/HubMigrationProcess.qml")
        }
    }

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: blockingDataImportBar

        headerText: tr.hub_migration
        showCloseIcon: false
        isRound: false
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: blockingDataImportBar.bottom
            bottom: retryButton.top
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.PlugImageHero {
            anchors.horizontalCenter: parent.horizontalCenter

            source: {
                if (hub.hub_type != "HUB_FIBRA") return "qrc:/resources/images/Athena/migration/HubToHubBlockingImport.svg"
                return donorHub.hub_type == "HUB_FIBRA" ?
                    "qrc:/resources/images/Athena/migration/FibraToFibraBlockingImport.svg" :
                    "qrc:/resources/images/Athena/migration/HubToFibraBlockingImport.svg"
            }
        }

        DS3.Spacing {
            height: 24
        }

        DS3.TitleUniversal {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            text: tr.migration_errors
        }

        DS3.Spacing {
            height: 56
        }

        Repeater {
            model: errorsModel

            delegate: Item {
                width: parent.width
                height: errorComment.height + 8

                DS3.SettingsContainer {
                    width: parent.width

                    anchors.horizontalCenter: parent.horizontalCenter

                    DS3.CommentImportant {
                        id: errorComment

                        atomTitle.title: modelData
                        status: DS3.CommentImportant.Status.Attention
                    }
                }

                DS3.Spacing {
                    height: 8
                }
            }
        }
    }

    DS3.ButtonBar {
        id: retryButton

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.try_again_button
        hasBackground: true

        button.onClicked: {
            Popups.please_wait_popup()
            app.start_migration(donorHub.hub_id, hub.hub_id)
        }
    }
}
