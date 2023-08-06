import QtQuick 2.7
import QtQuick.Controls 2.2
import QtGraphicalEffects 1.12


Item {
    id: legs

    width: 16
    height: 16

    visible: false

    Image {
        visible: legs.visible
        source: "qrc:/resources/images/Athena/status_icons/Motion-S.svg"
    }

    Timer {
        id: legsTimer
        interval: 5000
        repeat: false
        running: false
        onTriggered: legs.visible = false
    }

    Connections {
        target: device

        onMotionAlarmSignal: {
            legs.visible = true
            legsTimer.stop()
            legsTimer.start()
        }
    }
}