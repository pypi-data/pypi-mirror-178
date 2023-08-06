import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


Rectangle {
    id: migrationSettings

    property var sideMargin: 24
    property var selectedHub: null

    Component.onCompleted: {
        if (hub.config_migration.inited) {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/HubMigrationProcess.qml", {devicesReady: true})
            return
        }
    }

    Connections {
        target: app

        onGetDonorHubDataSuccess: {
            if (donorHub.online) {
                loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/HubOnlineScreen.qml", {selectedHub: selectedHub})
            } else if (hub.hub_type == "HUB_FIBRA") {
                loader.setSource(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/ReconnectBusesScreen.qml",
                    {selectedHub: selectedHub}
                )
            } else {
                loader.setSource(
                    "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/StartHubMigration.qml",
                    {selectedHub: selectedHub}
                )
            }
        }
    }

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: migrationSettingsBar

        headerText: tr.hub_migration
        showCloseIcon: false
        showManualIcon: true
        isRound: false

        onManualAreaClicked: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/data_import_popups/HubMigrationInfoPopup.qml")
        }
    }

    DS3.ScrollView {
        width: parent.width
        height: migrationSettings.height

        anchors {
            fill: undefined
            top: migrationSettingsBar.bottom
            bottom: nextButton.top
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            width: parent.width

            titleComponent.text: util.insert(tr.transfer_data_here_title_desktop, [hub.name])
            descComponent.text: tr.transfer_data_here_descr
        }

        DS3.Spacing {
            height: 24
        }

        DS3.Text {
            width: parent.width

            text: tr.select_data_source_title
            style: ui.ds3.text.special.SectionCaps
            color: ui.ds3.figure.secondary
        }

        DS3.Spacing {
            height: 4
        }

        DS3.SettingsContainer {
            width: parent.width

            anchors.horizontalCenter: parent.horizontalCenter

            DS3.DeviceRegular {
                id: selectedHubComponent

                width: parent.width

                imageSource: selectedHub ? undefined : "qrc:/resources/images/Athena/migration/DeviceImage.svg"
                atomTitle.title: selectedHub ? selectedHub.hub_for_migration.hub.name : tr.select_data_source_button
                atomTitle.subtitle: selectedHub ? selectedHub.hub_for_migration.hub.id : ""
                operator: DS3.DeviceRegular.OperatorType.NavigationArrow
                smallImage: true
                deviceColor: selectedHub ? selectedHub.hub_for_migration.hub.color : undefined
                deviceType: {
                    if (!selectedHub) return
                    if (selectedHub.subtype == "YAVIR") {
                        return "yavir_hub"
                    } else if (selectedHub.subtype == "YAVIR_PLUS" || selectedHub.subtype == "HUB_FIBRA") {
                        return "fibra_hub"
                    }
                    return "21"
                }
                onRightControlClicked: {
                    if (filteredAvailableHubsWithoutCurrent.length || filteredNotAvailableHubsWithoutCurrent.length) {
                        Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/data_import_popups/SelectHubForMigrationPopup.qml")
                    } else {
                        loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/NoHubsForDataExporting.qml")
                    }
                }
            }
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            text: tr.no_network_settings_transfer
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
        }
    }

    DS3.ButtonBar {
        id: nextButton

        width: parent.width

        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.next
        hasBackground: true
        enabled: !!selectedHub

        button.onClicked: {
            Popups.please_wait_popup()
            app.get_donor_hub_data(selectedHub)
        }
    }
}
