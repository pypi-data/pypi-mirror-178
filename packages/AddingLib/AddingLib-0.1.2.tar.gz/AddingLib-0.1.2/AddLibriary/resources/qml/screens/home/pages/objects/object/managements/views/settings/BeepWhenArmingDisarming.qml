import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/screens/home/pages/objects/object/managements/views/parts"

SettingField {
    sourceIcon: "qrc:/resources/images/Athena/views_icons/BeepWhenArmingDisarming-M.svg"
    propertyName: tr.beep_when_arming_disarming
    propertyValue: device.beep_on_arm_disarm_v2.includes("BEEP_ON_ARM") ||
                            device.beep_on_arm_disarm_v2.includes("BEEP_ON_DISARM") ? tr.yes : tr.no
}