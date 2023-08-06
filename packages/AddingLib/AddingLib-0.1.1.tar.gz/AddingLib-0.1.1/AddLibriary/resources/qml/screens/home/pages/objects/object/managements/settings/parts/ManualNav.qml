import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    title: tr.user_guide
    icon: "qrc:/resources/images/Athena/settings_icons/UserGuideSettings-L.svg"

    onEntered: {
        var link = app.hub_management_module.get_manual_link(device)
        Qt.openUrlExternally(link)
    }
}