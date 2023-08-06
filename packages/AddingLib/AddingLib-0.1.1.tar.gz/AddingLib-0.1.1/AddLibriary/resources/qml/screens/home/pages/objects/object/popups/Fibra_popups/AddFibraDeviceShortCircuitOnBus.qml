import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.Popup {
    width: 500
    height: Math.min(704, maxPopupHeight)

    header: DS3.NavBarModal {
        headerText: tr.bus_devices_adding_title
    }

    DS3.Spacing {
        height: 24
    }

    DS3.InfoContainer {
        id: infoContainer

        width: parent.width

        anchors.horizontalCenter: parent.horizontalCenter

        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/fibra/ShortCircuit-XL.svg"
        titleComponent.text: tr.power_test_short_circuit_impossible_title
        descComponent.text: tr.scanning_interrupted_overcurrent_descr
    }
}