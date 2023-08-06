import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    title: tr.ethernet_settings

    onEntered: setChild(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/settings/EthernetSettings.qml"
    )
}