import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3Popups.PopupStep {
    DS3.InfoContainer {
        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/fibra/FibraInfoPopupSecond.svg"
        titleComponent.text: tr.add_bus_device_wizard_title2
        descComponent.text: tr.add_bus_device_wizard_descr2
    }
}