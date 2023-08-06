import "qrc:/resources/qml/components/911/DS3/" as DS3


DS3.SettingsSwitch {
    title: tr.arc_spark_protection
    checked: device.arc_fault_detect == "ARC_FAULT_DETECT_ENABLED"
}