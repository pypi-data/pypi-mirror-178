import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    title: tr.data_channel_signal_strength_test
    icon: "qrc:/resources/images/Athena/settings_icons/WingsSettings-L.svg"

    onEntered: setChild(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/SignalDataLevelTest.qml",
        {"device": device}
    )
}