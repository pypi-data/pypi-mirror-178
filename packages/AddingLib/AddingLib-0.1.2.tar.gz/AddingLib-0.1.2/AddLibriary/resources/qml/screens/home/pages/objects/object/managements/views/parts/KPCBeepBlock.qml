import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3/" as DS3

Column {
    width: parent.width

    DS3.TitleSection {
        text: tr.beeps
        forceTextToLeft: true
        isBgTransparent: true
        isCaps: true
    }

    DS3.SettingsContainer {
        width: parent.width

        Settings.BeepOnArmDisarm {}
        Settings.BeepOnArmDisarmNightMode {}
        Settings.BeepOnDelayV1 {}
        Settings.BeepOnDisarmDelay {}
        Settings.BeepOnArmDelay {}
        Settings.BeepOnDisarmDelayNightMode {}
        Settings.BeepOnArmDelayNightMode {}
        Settings.ChimesPlay {}
        Settings.EventVolumeKPC {}
    }
}