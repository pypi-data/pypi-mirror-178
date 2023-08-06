import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3/popups" as DS3Popups
import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3Popups.PopupStep {
    DS3.InfoContainer {
        imageType: DS3.InfoContainer.ImageType.PlugImage
        imageSource: "qrc:/resources/images/Athena/migration/ButtonImage.svg"
        titleComponent.text: tr.wizard_helper_two_import_title
        descComponent.text: tr.wizard_helper_two_import_descr
    }
}