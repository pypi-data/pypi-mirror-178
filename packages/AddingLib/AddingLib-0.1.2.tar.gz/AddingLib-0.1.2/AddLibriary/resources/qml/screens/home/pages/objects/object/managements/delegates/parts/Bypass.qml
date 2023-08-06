import QtQuick 2.7
import QtQuick.Controls 2.2


Item {
    width: childrenRect.width
    height: childrenRect.height

    Image {
        source: {
            if (device.is_bypassed == 1) return "qrc:/resources/images/Athena/status_icons/TemporaryDeactivationWholeDevice-S.svg"
            if (device.is_bypassed == 2 && !["0b", "0c", "42", "12", "1e", "1f"].includes(device.obj_type)) return "qrc:/resources/images/Athena/status_icons/TemporaryDeactivationTamper-S.svg"
            if (device.is_bypassed == 4 || device.is_bypassed == 6 && !["07", "46"].includes(device.obj_type)) return "qrc:/resources/images/Athena/status_icons/TemporaryDeactivationAlarms-S.svg"
            if (device.is_bypassed == 8 || device.is_bypassed == 10) return "qrc:/resources/images/Athena/status_icons/TemporaryDeactivationTimer-S.svg"
            return ""
        }
    }
}
