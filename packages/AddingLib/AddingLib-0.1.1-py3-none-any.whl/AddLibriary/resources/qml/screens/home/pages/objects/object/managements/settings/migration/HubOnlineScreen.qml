import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    id: hubOnlineScreen

    property var sideMargin: 24
    property var selectedHub: null

    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: hubOnlineBar

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
            top: hubOnlineBar.bottom
            bottom: nextButton.top
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.PlugImageHero {
            source: hub.hub_type == "HUB_FIBRA" ?
                "qrc:/resources/images/Athena/migration/HubImportPreparationFibra.svg" :
                "qrc:/resources/images/Athena/migration/HubImportPreparation.svg"
        }

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            titleComponent.text: util.insert(tr.switch_source_hub_off_title_desltop, [donorHub.name])
            descComponent.text: tr.switch_source_hub_off_descr
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
        hasComment: true
        commentText: donorHub.online ? tr.validating : tr.ready
        commentIcon: "qrc:/resources/images/Athena/common_icons/Info-Grey-S.svg"
        enabled: !donorHub.online

        button.onClicked: {
            hub.hub_type == "HUB_FIBRA" ?
            console.log("Fibra Hub")
            :
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/StartHubMigration.qml", {selectedHub: selectedHub})
        }
    }

    Timer {
        id: requestTimer

        interval: 1000 * 20
        repeat: true

        triggeredOnStart: false
        running: true

        onTriggered: {
            app.get_donor_hub_data(selectedHub)
        }
    }
}
