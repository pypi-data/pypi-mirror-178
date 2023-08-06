import QtQuick 2.7
import QtQuick.Controls 2.1
import QtQuick.Layouts 1.3

import "qrc:/resources/qml/components/911/DS3" as DS3

DS3.InfoTitle {
    atomTitle {
        title: tr.false_alarms_reduction
        subtitle: device.pet_immunity ? tr.on : tr.off
    }

    leftIcon.source: "qrc:/resources/images/Athena/views_icons/CorrelationSignalProcessing-M.svg"
}