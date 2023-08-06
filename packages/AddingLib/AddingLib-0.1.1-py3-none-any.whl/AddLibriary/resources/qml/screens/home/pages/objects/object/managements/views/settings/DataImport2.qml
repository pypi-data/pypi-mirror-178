import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.InfoTitle {
    visible: device.migration_state == "IN_MIGRATION"
    atomTitle {
        title: tr.hub_migration
        subtitle: tr.device_migration_state_failed
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/DataImport-M.svg"
    status: ui.ds3.status.ATTENTION
}
