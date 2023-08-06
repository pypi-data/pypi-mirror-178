import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12

import "qrc:/resources/qml/components/911/DS3/" as DS3

Rectangle {
    anchors.fill: parent

    color: ui.ds3.bg.base

    DS3.NavBarModal {
        id: navBarModal

        anchors.top: parent.top

        headerText: tr.bus_power_test_title
        isRound: false
        showBackArrow: true
        showCloseIcon: false

        onBackAreaClicked: {
            loader.setSource("qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/wires/WiresSettings.qml")
        }
    }

    DS3.InfoContainer {
        anchors {
            top: navBarModal.bottom
            topMargin: 24
        }

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/fibra/NoDevicesForWireTest.svg"
        titleComponent.text: tr.no_devices_found_title
        descComponent.text: tr.no_devices_bus_test_description
    }
}