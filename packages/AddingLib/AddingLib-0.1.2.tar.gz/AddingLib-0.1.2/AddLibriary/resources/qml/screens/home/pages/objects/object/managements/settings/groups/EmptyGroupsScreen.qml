import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoContainer {
    width: parent.width

    imageType: DS3.InfoContainer.ImageType.PlugImage
    titleComponent.text: tr.group_mode_title
    descComponent.text: tr.groups_explanation_desktop
    imageSource: "qrc:/resources/images/Athena/common_icons/Groups-XL.svg"
}
