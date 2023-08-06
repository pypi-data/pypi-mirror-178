import QtQuick 2.7
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    title: tr.beeps

    onEntered: setChild(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/parts/SirenBeepsPopupStep.qml"
    )
}