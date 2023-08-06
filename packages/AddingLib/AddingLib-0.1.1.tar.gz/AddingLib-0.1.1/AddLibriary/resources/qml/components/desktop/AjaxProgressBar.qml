import QtQuick 2.7
import QtQuick.Controls 2.2

Item {
    id: progressItem

    property int progressStep: 0
    property var totalSteps: {
        if (hub.hub_type == "YAVIR") return 5
        if (hub.hub_type == "YAVIR_PLUS") return 7
        return 10
    }

    Row {
        width: parent.width
        height: parent.height

        spacing: 2

        Repeater {
            id: repeater
            model: totalSteps

            Rectangle {
                width: (parent.width - (totalSteps - 1) * 2) / totalSteps
                height: 4
                color: index < progressStep ? "#60e3ab" : ui.colors.middle1
            }
        }
    }
}
