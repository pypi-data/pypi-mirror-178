import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsNavigationTitlePrimary {
    title: tr.attenuation_test
    icon: "qrc:/resources/images/Athena/settings_icons/SignalAttenuationSettings-L.svg"
    visible: device.test_signal_lost_available

    onEntered: setChild(
        "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/SignalLostTest.qml"
    )
}