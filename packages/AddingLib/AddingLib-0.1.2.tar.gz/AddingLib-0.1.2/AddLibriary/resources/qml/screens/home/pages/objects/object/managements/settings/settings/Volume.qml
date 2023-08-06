import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSliderIcon {
    title: tr.volume
    from: 0
    to: 15
    stepSize: 1
    value: device.volume
    sideIcons: [
        "qrc:/resources/images/Athena/common_icons/VolumeLow-M.svg",
        "qrc:/resources/images/Athena/common_icons/Volume-M.svg"
    ]
}