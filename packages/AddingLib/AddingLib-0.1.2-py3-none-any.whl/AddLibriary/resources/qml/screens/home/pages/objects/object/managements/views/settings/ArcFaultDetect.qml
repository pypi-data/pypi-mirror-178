import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    atomTitle {
        title: tr.arc_spark_protection
        subtitle: device.arc_fault_detect == "ARC_FAULT_DETECT_ENABLED" ? tr.on : tr.off
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/ArcFault-M.svg"
}