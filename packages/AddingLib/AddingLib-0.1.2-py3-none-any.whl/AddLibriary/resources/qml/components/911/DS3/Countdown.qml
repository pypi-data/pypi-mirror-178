import QtQuick 2.12
import QtQuick.Controls 2.13

import "qrc:/resources/qml/components/911/DS3" as DS3
import "qrc:/resources/js/popups.js" as Popups

Item {
    property var endTimestamp
    property var timeLeft: null
    property var timeLeftStr: {
        var hrs = Math.floor(timeLeft / 3600);
        var min = Math.floor((timeLeft - (hrs * 3600)) / 60);
        var sec = timeLeft - (hrs * 3600) - (min * 60);
        return hrs + ":" + min.toString().padStart(2, "0") + ":" + sec.toString().padStart(2, "0")
    }

    width: textTimer.width
    height: textTimer.height

    Timer {
        id: timer

        interval: 200
        repeat: true

        onTriggered: {
            if (endTimestamp < Date.now() / 1000) stop()
            timeLeft = Math.round(endTimestamp - Date.now() / 1000)
        }
    }

    onEndTimestampChanged: {
        timer.stop()
        if (Date.now() / 1000 < endTimestamp) {
            timeLeft = Math.round(endTimestamp - Date.now() / 1000)
            timer.start()
        } else {
            timeLeft = 0
        }
    }

    DS3.Text {
        id: textTimer

        anchors.verticalCenter: parent.verticalCenter

        text: !timeLeft ? tr.no_pro_permissions : timeLeftStr
        style: ui.ds3.text.body.MRegular
        color: ui.colors.red1
    }
}
