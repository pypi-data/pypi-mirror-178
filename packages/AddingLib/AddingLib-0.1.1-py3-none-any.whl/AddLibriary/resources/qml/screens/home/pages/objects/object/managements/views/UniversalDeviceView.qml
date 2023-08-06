import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/qml/components/911/DS3" as DS3


ViewsParts.DeviceViewForRedesign {
    Settings.DataImport {}
    Settings.Temperature {}
    DS3.InfoTitleButtonIcon {
        atomTitle {
            title: "Settings"
            subtitle: device.settingsHex
        }
        leftIcon.source: "qrc:/resources/images/Athena/views_icons/ServiceSettings-M.svg"
        buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"
    }
    DS3.InfoTitleButtonIcon {
        atomTitle {
            title: "Statuses"
            subtitle: device.statusesHex
        }
        leftIcon.source: "qrc:/resources/images/Athena/views_icons/ServiceSettings-M.svg"
        buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"
    }
    DS3.InfoTitleButtonIcon {
        atomTitle {
            title: "Alarms"
            subtitle: device.alarmsHex
        }
        leftIcon.source: "qrc:/resources/images/Athena/views_icons/ServiceSettings-M.svg"
        buttonIcon.source: "qrc:/resources/images/Athena/common_icons/Copy-M.svg"
    }
    Settings.SignalStrength {}
    Settings.Connection {}
    Settings.BatteryCharge {}
    Settings.Tamper {}
    Settings.RoutedThroughReX {}
    Settings.TemporaryDeactivation {}
}