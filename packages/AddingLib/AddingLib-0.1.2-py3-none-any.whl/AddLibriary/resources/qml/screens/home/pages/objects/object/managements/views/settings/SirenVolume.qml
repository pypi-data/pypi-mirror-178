import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.siren_volume
        subtitle: ({
            0: tr.no,
            1: tr.off,
            2: tr.volume_min,
            3: tr.volume_mid,
            4: tr.volume_max,
        }[device.siren_alarm_volume])
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/Volume-M.svg"
}