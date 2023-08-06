import QtQuick 2.7
import QtQuick.Controls 2.1

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    property bool isBad: {
        if (device.backup_cell_charge == "N/A") return false
        return device.backup_cell_charge != 1 || !device.backup_cell_ok
    }

    atomTitle {
        title: tr.backup_battery_charge
        subtitle: {
            if (device.backup_cell_charge == "N/A") { return tr.na }
            if (!device.backup_cell_ok) { return tr.error }
            if (device.backup_cell_charge == 0) { return tr.discharged }
            return "OK"
        }
    }
    leftIcon.source: "qrc:/resources/images/Athena/views_icons/BackupBatteryCharge-M.svg"
    status: isBad ? ui.ds3.status.ATTENTION : ui.ds3.status.DEFAULT
}