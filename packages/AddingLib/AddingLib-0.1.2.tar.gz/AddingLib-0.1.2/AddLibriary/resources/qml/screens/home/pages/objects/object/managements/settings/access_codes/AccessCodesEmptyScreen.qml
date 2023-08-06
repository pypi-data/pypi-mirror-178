import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    property string plugImageSource
    property string textKey

    width: parent.width

    color: ui.ds3.bg.base

    Column {
        anchors.fill: parent

        DS3.Spacing {
            height: 24
        }

        DS3.InfoContainer {
            imageType: DS3.InfoContainer.ImageType.PlugImage
            imageSource: plugImageSource
            descComponent.text: textKey
        }
    }
}