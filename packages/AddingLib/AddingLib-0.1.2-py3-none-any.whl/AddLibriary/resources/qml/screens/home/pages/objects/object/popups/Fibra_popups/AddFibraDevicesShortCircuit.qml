import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3

Rectangle {
    width: 500
    height: 704

    color: ui.backgrounds.base
    radius: 12

    anchors.fill: parent

    DS3.NavBarModal {
        id: navBarModal

        anchors.top: parent.top

        headerText: tr.bus_devices_adding_title

        onClosed: () => {
            app.hub_management_module.scan_fibra_devices("STOP")
            mainFibraPopup.close()
        }
    }

    DS3.InfoContainer {
        id: infoContainer

        anchors {
            top: navBarModal.bottom
            topMargin: 24
            horizontalCenter: parent.horizontalCenter
        }

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/fibra/ShortCircuit-XL.svg"
        titleComponent.text: tr.scanning_interrupted_overcurrent_title
        descComponent.text: tr.scanning_interrupted_overcurrent_descr
    }
}