import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


Rectangle {
    id: usersSettings

    color: ui.ds3.bg.base

    DS3.InfoContainer {
        anchors {
            top: parent.top
            topMargin: 24
            horizontalCenter: parent.horizontalCenter
        }

        imageType: DS3.InfoContainer.ImageType.BigImage
        imageSource: "qrc:/resources/images/Athena/common_icons/NoHubPermissionsImage.svg"
        titleComponent.text: tr.no_hub_access_desktop_title
        descComponent.text: tr.no_hub_access_desktop_descr
    }
}
