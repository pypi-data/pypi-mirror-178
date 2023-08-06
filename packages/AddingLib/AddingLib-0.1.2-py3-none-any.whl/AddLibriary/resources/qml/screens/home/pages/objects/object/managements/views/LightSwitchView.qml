import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as ViewRows
import "qrc:/resources/qml/components/911/DS3" as DS3


ViewsParts.DeviceView2 { // TODO remove 2 after merge devices_redesign to develop
//  Content of the first part of Light Switch View
    property Component connection: connectionContainer
//  Content of the second button info
    property Component twoGangButton: twoGangButtonContainer
//  Readonly connection Item
    readonly property alias connectionItem: connectionItem.item
//  Readonly twoGangButton Item
    readonly property alias twoGangButtonItem: twoGangButtonItem.item

    Loader {
        id: connectionItem

        anchors {
            left: parent.left
            right: parent.right
        }

        sourceComponent: connection
        z: 2
    }

    Component {
        id: connectionContainer

        DS3.SettingsContainer {
            width: parent.width

            ViewRows.SignalStrength {}
            ViewRows.Connection {}
            ViewRows.RoutedThroughReX {}
        }
    }

    DS3.Spacing {
        height: 24
    }

    DS3.TitleSection {
        isCaps: true
        forceTextToLeft: true
        isBgTransparent: true
        text: device.subtype == "LIGHT_SWITCH_TWO_GANG" ?
            tr.left_button_lightswitch_title :
            tr.button_setings_lightswitch_title
    }

    DS3.SettingsContainer {
        width: parent.width

        ViewRows.ButtonOnOff {
            isOff: !device.channel1_on
            buttonName: device.button1_name
            leftIcon.source: device.subtype == "LIGHT_SWITCH_TWO_GANG" ?
                "qrc:/resources/images/Athena/views_icons/LsFirstButton-M.svg" :
                "qrc:/resources/images/Athena/views_icons/LsButton-M.svg"
        }

        ViewRows.OperatingTime {
            visible: !!device.shut_off_mode_enabled_ch1
            duration_time: device.shut_off_period_channel1_str
        }
    }

    DS3.Spacing {
        height: 24
    }

    Loader {
        id: twoGangButtonItem

        anchors {
            left: parent.left
            right: parent.right
        }

        sourceComponent: twoGangButton
        z: 2
    }

    Component {
        id: twoGangButtonContainer

        Item {}
    }


    DS3.SettingsContainer {
        width: parent.width

        ViewRows.LockSwitchButtons {}
        ViewRows.Backlight {}
        ViewRows.TemporaryDeactivation {}
    }
}