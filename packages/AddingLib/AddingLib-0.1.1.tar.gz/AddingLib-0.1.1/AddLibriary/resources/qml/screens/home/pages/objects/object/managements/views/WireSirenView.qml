import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/settings/" as Settings
import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts" as ViewsParts
import "qrc:/resources/qml/components/911/DS3/" as DS3


ViewsParts.DeviceViewForRedesign {
    DS3.SettingsContainer {
        Settings.TimeToAct {}
    }

    DS3.Spacing {
        height: 24
    }

    ViewsParts.SirenBeepBlock {}
}
