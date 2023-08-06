import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/js/desktop/popups.js" as Popups
import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: noHubsScreen

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: noHubsBar

        headerText: tr.hub_migration
        showCloseIcon: false
        showBackArrow: true
        showManualIcon: true
        isRound: false

        onManualAreaClicked: {
            Popups.popupByPath("qrc:/resources/qml/screens/home/pages/objects/object/popups/data_import_popups/HubMigrationInfoPopup.qml")
        }

        onBackAreaClicked: {
            loader.setSource(
                "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/migration/MigrationSettings.qml"
            )
        }
    }

    DS3.ScrollView {
        anchors {
            fill: undefined
            top: noHubsBar.bottom
            bottom: parent.bottom
            left: parent.left
            right: parent.right
        }

        padding: 24

        DS3.Text {
            width: parent.width

            text: tr.all_donors_are_absent_cut
            style: ui.ds3.text.body.MRegular
            color: ui.ds3.figure.secondary
            horizontalAlignment: Text.AlignHCenter
        }

        DS3.Spacing {
            height: 4
        }

        DS3.Text {
            width: parent.width

            horizontalAlignment: Text.AlignHCenter
            style: ui.ds3.text.body.MBold
            text: {
                var locale = tr.get_locale()
                var link = "http://instructionservice.ops.ajax.systems/migration?lang=" + locale

                return util.hyperlink(tr.learn_more, link)
            }
        }
    }
}
