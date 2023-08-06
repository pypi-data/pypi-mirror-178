import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts"

SettingField {
    sourceIcon: "qrc:/resources/images/Athena/views_icons/Jeweller-M.svg"
    propertyName: tr.jeweller_connection_state
    propertyValue: {
        return {
            "-1": tr.na,
            "0": tr.offline,
            "1": tr.online,
        }[device.rf_connection_ok]
    }
    bad: device.rf_connection_ok == 0
}
