import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as DesktopPopups

Rectangle {
    anchors.fill: parent

    color: ui.ds3.bg.base
    radius: 12

    DS3.NavBarModal {
        id: navBarModal

        headerText: tr.bus_devices_adding_title

        onClosed: () => {
            app.hub_management_module.scan_fibra_devices("STOP")
            mainFibraPopup.close()
        }
    }

    DS3.InfoContainer {
        anchors {
            top: navBarModal.bottom
            topMargin: 24
            horizontalCenter: parent.horizontalCenter
        }

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/fibra/NotFound-XL.svg"
        titleComponent.text: tr.no_devices_found_title
        descComponent.text: tr.no_bus_devices_found_description
    }

    DS3.ButtonBar {
        anchors {
            bottom: parent.bottom
            horizontalCenter: parent.horizontalCenter
        }

        buttonText: tr.scanning_interrupted_overcurrent_button
        button.onClicked: {
            mainFibraPopup.isRestartAfterNoDevicesScreen = true
            app.hub_management_module.scan_fibra_devices("STOP")
        }
    }
}