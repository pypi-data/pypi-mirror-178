import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/desktop/popups.js" as Popups


DS3.SettingsNavigationTitlePrimary {
    title: tr.start_siren_test
    icon: "qrc:/resources/images/Athena/settings_icons/VolumeSettings-L.svg"
    visible: device.volume_test_available

    onEntered: {
        if (changesChecker.hasChanges) {
            saveButtonClickCallback(false)
        }
        setChild(
            "qrc:/resources/qml/screens/home/pages/objects/object/managements/settings/tests/TestVolumeStep.qml"
        )
    }
}