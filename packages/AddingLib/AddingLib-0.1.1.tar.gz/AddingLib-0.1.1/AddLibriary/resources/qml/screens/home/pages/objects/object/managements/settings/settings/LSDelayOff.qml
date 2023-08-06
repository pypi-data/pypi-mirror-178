import QtQuick 2.12
import QtQuick.Controls 2.2

import "qrc:/resources/qml/components/911/DS3" as DS3


DS3.SettingsSwitch {
// comments on lines 20, 36 - debug lines, will be cleaned later
    width: parent.width


//  Initial time
    property var timeStr: null
//  Initial time
    property var time: null
//  Current time left
    property var timeLeft: time

//  Start the timer
    function start() {
        time = timeLeft // = shutoffTimeLightswitch.duration[shutoffTimeLightswitch.currentIndex]
        timer.start()
    }

//  Stop the timer
    function stop() {
        timer.stop()
        timer.timeStart = null
    }

    property var subtitleValue: {
        if (checked) {
            var hours = Math.floor(timeLeft / 3600)
            var min = Math.floor(timeLeft / 60) % 60
            var sec = timeLeft % 60
            return hours.toString().padStart(2, "0") + ":" + min.toString().padStart(2, "0") + ":" + sec.toString().padStart(2, "0")
        } else {
            timeStr  //shutoffTimeLightswitch.model[shutoffTimeLightswitch.currentIndex]
        }
    }

    title: "Button Name Here"
    subtitle: subtitleValue
    subtitleIcon.source: "qrc:/resources/images/Athena/common_icons/Timer-S.svg"
    subtitleIcon.color: ui.ds3.figure.base
    cancelBinding: false

    onSwitched: () => {
        checked = !checked
        checked ? start() : stop()
    }

    Timer {
        id: timer

        property var timeStart: null

        interval: 100
        repeat: true
        triggeredOnStart: true

        onTriggered: {
            if (!timeStart) {
                timeStart = Date.now()
            } else {
                let timeElapsed = (Date.now() - timeStart) / 1000
                if (timeElapsed >= time) {
                    timeLeft = 0
                }
                else {
                    timeLeft = Math.ceil(time - timeElapsed)
                }
            }
        }
    }
}