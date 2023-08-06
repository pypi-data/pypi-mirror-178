import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    id: reconnectBusesScreen

    property var sideMargin: 24
    property var selectedHub: null

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: reconnectBusesBar

        headerText: tr.hub_migration
        showCloseIcon: false
        showBackArrow: true
        showManualIcon: true
        isRound: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/MigrationSettings.qml", {selectedHub: selectedHub})
        }

        onManualAreaClicked: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/data_import_popups/HubMigrationInfoPopup.qml")
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: reconnectBusesBar.bottom
            bottom: nextButton.top
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.PlugImageHero {
            source: "qrc:/resources/images/Athena/migration/FibraReconnectBuses.svg"
        }

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            titleComponent.text: tr.reconnect_buses_migration_title
            descComponent.text: util.insert(tr.reconnect_buses_migration_descr, [hub.name])
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

        button.onClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/StartHubMigration.qml", {selectedHub: selectedHub})
        }
    }
}
